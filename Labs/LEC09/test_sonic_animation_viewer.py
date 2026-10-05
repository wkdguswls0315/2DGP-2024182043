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


if __name__ == "__main__":
    unittest.main()
