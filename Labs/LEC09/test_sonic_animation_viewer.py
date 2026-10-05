import unittest

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

    def test_advances_to_next_frame_after_frame_delay(self):
        player = viewer.AnimationPlayer(self.animations)

        player.advance(0.1)

        self.assertEqual(player.frame_index, 1)
        self.assertEqual(player.current_frame, self.animations[0].frames[1])

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


if __name__ == "__main__":
    unittest.main()
