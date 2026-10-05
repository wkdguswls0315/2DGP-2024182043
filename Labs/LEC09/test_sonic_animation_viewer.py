import math
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import sonic_animation_viewer as viewer


class AnimationMetadataTests(unittest.TestCase):
    def test_catalog_contains_all_configured_frames(self):
        self.assertEqual(len(viewer.ANIMATIONS), 10)
        self.assertEqual(
            sum(len(animation.frames) for animation in viewer.ANIMATIONS),
            76,
        )

    def test_configured_frames_fit_the_sprite_sheet(self):
        viewer.validate_animations(viewer.ANIMATIONS)

    def test_rejects_empty_animation_catalog(self):
        with self.assertRaises(ValueError):
            viewer.validate_animations(())

    def test_rejects_animation_without_frames(self):
        empty_animation = viewer.Animation("empty", (), 0.1)

        with self.assertRaises(ValueError):
            viewer.validate_animations((empty_animation,))

    def test_rejects_frame_outside_the_sprite_sheet(self):
        frame = viewer.SpriteFrame(390, 0, 20, 10)
        animation = viewer.Animation("invalid", (frame,), 0.1)

        with self.assertRaises(ValueError):
            viewer.validate_animations((animation,))

    def test_rejects_non_positive_frame_delay(self):
        frame = viewer.SpriteFrame(0, 0, 1, 1)
        animation = viewer.Animation("invalid", (frame,), 0.0)

        with self.assertRaises(ValueError):
            viewer.validate_animations((animation,))

    def test_rejects_non_finite_frame_delay(self):
        frame = viewer.SpriteFrame(0, 0, 1, 1)
        animation = viewer.Animation("invalid", (frame,), math.nan)

        with self.assertRaises(ValueError):
            viewer.validate_animations((animation,))

    def test_rejects_negative_movement_speed(self):
        frame = viewer.SpriteFrame(0, 0, 1, 1)
        animation = viewer.Animation("invalid", (frame,), 0.1, -1.0)

        with self.assertRaisesRegex(ValueError, "movement speed"):
            viewer.validate_animations((animation,))

    def test_sprite_sheet_path_is_relative_to_viewer_file(self):
        path = viewer.get_sprite_sheet_path()

        self.assertEqual(path.name, "sonic-sprite.png")
        self.assertTrue(path.is_file())


class AnimationPlayerTests(unittest.TestCase):
    def setUp(self):
        frames = (
            viewer.SpriteFrame(0, 0, 1, 1),
            viewer.SpriteFrame(1, 0, 1, 1),
        )
        self.animations = (
            viewer.Animation("first", frames, 0.1),
            viewer.Animation("second", frames[:1], 0.1),
        )

    def test_starts_at_first_frame_of_first_animation(self):
        player = viewer.AnimationPlayer(self.animations)

        self.assertEqual(player.animation_index, 0)
        self.assertEqual(player.frame_index, 0)
        self.assertEqual(player.current_animation.name, "first")
        self.assertEqual(player.current_frame, self.animations[0].frames[0])

    def test_rejects_empty_catalog_when_creating_player(self):
        with self.assertRaisesRegex(ValueError, "At least one animation"):
            viewer.AnimationPlayer(())

    def test_advances_to_next_frame_after_frame_delay(self):
        player = viewer.AnimationPlayer(self.animations)

        player.advance(0.1)

        self.assertEqual(player.frame_index, 1)
        self.assertEqual(player.current_frame, self.animations[0].frames[1])

    def test_rejects_invalid_elapsed_time(self):
        player = viewer.AnimationPlayer(self.animations)

        for elapsed in (-0.1, math.nan, math.inf):
            with self.subTest(elapsed=elapsed):
                with self.assertRaisesRegex(ValueError, "Elapsed time"):
                    player.advance(elapsed)

    def test_counts_a_cycle_when_last_frame_finishes(self):
        player = viewer.AnimationPlayer(self.animations)

        player.advance(0.2)

        self.assertEqual(player.frame_index, 0)
        self.assertEqual(player.completed_cycles, 1)
        self.assertEqual(player.pause_remaining, 0.0)

    def test_requires_five_complete_cycles_before_pausing(self):
        player = viewer.AnimationPlayer(self.animations)

        player.advance(0.99)

        self.assertEqual(player.completed_cycles, 4)
        self.assertEqual(player.pause_remaining, 0.0)

        player.advance(0.01)

        self.assertEqual(player.completed_cycles, 5)
        self.assertAlmostEqual(player.pause_remaining, viewer.ACTION_PAUSE)

    def test_keeps_current_animation_during_inter_action_pause(self):
        player = viewer.AnimationPlayer(self.animations)

        player.advance(1.0)
        player.advance(0.4)

        self.assertEqual(player.animation_index, 0)
        self.assertAlmostEqual(player.pause_remaining, 0.6)

    def test_starts_next_animation_with_reset_progress(self):
        player = viewer.AnimationPlayer(self.animations)

        player.advance(2.0)

        self.assertEqual(player.animation_index, 1)
        self.assertEqual(player.frame_index, 0)
        self.assertEqual(player.completed_cycles, 0)
        self.assertEqual(player.frame_elapsed, 0.0)

    def test_wraps_from_last_animation_to_first(self):
        player = viewer.AnimationPlayer(self.animations)

        player.advance(3.5)

        self.assertEqual(player.animation_index, 0)
        self.assertEqual(player.frame_index, 0)
        self.assertEqual(player.completed_cycles, 0)

    def test_moving_animation_updates_screen_position_over_time(self):
        moving_animation = viewer.Animation(
            "run",
            self.animations[0].frames[:1],
            0.1,
            movement_speed=100.0,
        )
        player = viewer.AnimationPlayer((moving_animation,))

        player.advance(0.05)

        self.assertAlmostEqual(
            player.position_x,
            viewer.SPRITE_CENTER_X + 5.0,
        )

    def test_stationary_animation_does_not_change_screen_position(self):
        player = viewer.AnimationPlayer(self.animations)

        player.advance(0.05)

        self.assertEqual(player.position_x, viewer.SPRITE_CENTER_X)

    def test_position_reverses_at_screen_boundary(self):
        position_x, direction = viewer.advance_horizontal_position(
            viewer.MOVEMENT_MAX_X - 5,
            1,
            10,
        )

        self.assertEqual(position_x, viewer.MOVEMENT_MAX_X - 5)
        self.assertEqual(direction, -1)


class ViewerLifecycleTests(unittest.TestCase):
    def test_draws_frame_with_bottom_origin_and_preserved_aspect_ratio(self):
        sprite_sheet = MagicMock()
        frame = viewer.SpriteFrame(7, 11, 20, 10)
        scale = min(
            viewer.SPRITE_MAX_WIDTH / viewer.MAX_FRAME_WIDTH,
            viewer.SPRITE_MAX_HEIGHT / viewer.MAX_FRAME_HEIGHT,
        )

        viewer.draw_frame(sprite_sheet, frame)

        sprite_sheet.clip_draw.assert_called_once_with(
            frame.left,
            viewer.SPRITE_SHEET_HEIGHT - frame.top - frame.height,
            frame.width,
            frame.height,
            viewer.SPRITE_CENTER_X,
            viewer.SPRITE_CENTER_Y,
            frame.width * scale,
            frame.height * scale,
        )

    def test_draws_leftward_motion_with_horizontal_flip(self):
        sprite_sheet = MagicMock()
        frame = viewer.SpriteFrame(7, 11, 20, 10)

        viewer.draw_frame(sprite_sheet, frame, position_x=300, direction=-1)

        sprite_sheet.clip_composite_draw.assert_called_once()
        self.assertEqual(
            sprite_sheet.clip_composite_draw.call_args.args[4:8],
            (0, "h", 300, viewer.SPRITE_CENTER_Y),
        )
        sprite_sheet.clip_draw.assert_not_called()

    def test_closes_canvas_when_asset_loading_fails(self):
        with (
            patch.object(viewer, "open_canvas") as open_canvas,
            patch.object(
                viewer, "load_image", side_effect=OSError("asset unavailable")
            ),
            patch.object(viewer, "close_canvas") as close_canvas,
        ):
            with self.assertRaisesRegex(OSError, "asset unavailable"):
                viewer.main()

        open_canvas.assert_called_once_with(
            viewer.CANVAS_WIDTH,
            viewer.CANVAS_HEIGHT,
        )
        close_canvas.assert_called_once_with()

    def test_closes_canvas_after_window_close_event(self):
        close_event = SimpleNamespace(type=viewer.SDL_QUIT)
        with (
            patch.object(viewer, "open_canvas"),
            patch.object(viewer, "load_image", return_value=MagicMock()),
            patch.object(viewer, "get_events", return_value=[close_event]),
            patch.object(viewer, "clear_canvas"),
            patch.object(viewer, "draw_frame"),
            patch.object(viewer, "update_canvas"),
            patch.object(viewer, "delay"),
            patch.object(viewer, "close_canvas") as close_canvas,
        ):
            viewer.main()

        close_canvas.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
