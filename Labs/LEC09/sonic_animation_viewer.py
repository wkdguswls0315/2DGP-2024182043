import math
import time
from dataclasses import dataclass
from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SPRITE_SHEET_WIDTH = 399
SPRITE_SHEET_HEIGHT = 525
SPRITE_CENTER_X = CANVAS_WIDTH // 2
SPRITE_CENTER_Y = CANVAS_HEIGHT // 2
SPRITE_MAX_WIDTH = 420
SPRITE_MAX_HEIGHT = 420
ANIMATION_REPEAT_COUNT = 5
ACTION_PAUSE = 1.0
TIME_EPSILON = 1e-9


@dataclass(frozen=True)
class SpriteFrame:
    left: int
    top: int
    width: int
    height: int

    @property
    def bottom(self) -> int:
        return SPRITE_SHEET_HEIGHT - self.top - self.height


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[SpriteFrame, ...]
    frame_delay: float


def make_frames(
    boxes: tuple[tuple[int, int, int, int], ...],
) -> tuple[SpriteFrame, ...]:
    return tuple(SpriteFrame(*box) for box in boxes)


ANIMATIONS = (
    Animation(
        "Sonic run (row 1)",
        make_frames(
            (
                (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
                (86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38),
                (182, 40, 29, 38), (211, 39, 29, 38), (240, 39, 29, 38),
                (270, 45, 24, 32), (302, 51, 29, 26),
            )
        ),
        0.09,
    ),
    Animation(
        "Sonic run (row 2)",
        make_frames(
            (
                (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
                (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
                (206, 79, 26, 38), (238, 80, 24, 37), (263, 80, 30, 37),
                (295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
            )
        ),
        0.09,
    ),
    Animation(
        "Sonic action (row 3)",
        make_frames(
            (
                (1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
                (130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 41),
            )
        ),
        0.11,
    ),
    Animation(
        "Sonic spin (row 4)",
        make_frames(
            (
                (1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29),
                (98, 169, 31, 30), (131, 168, 29, 30), (162, 168, 29, 31),
                (193, 170, 30, 29), (230, 170, 31, 29), (268, 168, 30, 32),
            )
        ),
        0.08,
    ),
    Animation(
        "Sonic rolling ball (row 5)",
        make_frames(
            (
                (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
                (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
            )
        ),
        0.08,
    ),
    Animation(
        "Sonic action (row 6)",
        make_frames(
            (
                (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
                (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
            )
        ),
        0.1,
    ),
    Animation(
        "Sonic attack (row 7)",
        make_frames(
            (
                (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
                (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
            )
        ),
        0.1,
    ),
    Animation(
        "Sonic movement (row 8)",
        make_frames(
            (
                (1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
                (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44),
                (184, 341, 40, 28), (232, 341, 39, 27),
            )
        ),
        0.1,
    ),
    Animation(
        "Sonic run (row 9)",
        make_frames(
            (
                (1, 379, 27, 38), (31, 379, 31, 36), (64, 379, 31, 36),
                (99, 377, 33, 38), (136, 379, 32, 36), (176, 379, 33, 37),
                (217, 379, 33, 37), (254, 378, 33, 36),
            )
        ),
        0.09,
    ),
    Animation(
        "Sonic attack (row 10)",
        make_frames(
            (
                (6, 429, 34, 40), (49, 426, 34, 43), (96, 427, 23, 39),
                (125, 427, 23, 39),
            )
        ),
        0.12,
    ),
)

MAX_FRAME_WIDTH = max(
    frame.width for animation in ANIMATIONS for frame in animation.frames
)
MAX_FRAME_HEIGHT = max(
    frame.height for animation in ANIMATIONS for frame in animation.frames
)


def validate_animations(animations: tuple[Animation, ...]) -> None:
    if not animations:
        raise ValueError("At least one animation must be configured.")

    for animation in animations:
        if not animation.frames:
            raise ValueError(f"Animation {animation.name!r} has no frames.")
        if not math.isfinite(animation.frame_delay) or animation.frame_delay <= 0:
            raise ValueError(
                f"Animation {animation.name!r} must have a finite, "
                "positive frame delay."
            )

        for frame in animation.frames:
            if (
                frame.left < 0
                or frame.top < 0
                or frame.width <= 0
                or frame.height <= 0
                or frame.left + frame.width > SPRITE_SHEET_WIDTH
                or frame.top + frame.height > SPRITE_SHEET_HEIGHT
            ):
                raise ValueError(
                    f"Frame {frame!r} in animation {animation.name!r} "
                    f"is outside the {SPRITE_SHEET_WIDTH}x{SPRITE_SHEET_HEIGHT} "
                    "sprite sheet."
                )


class AnimationPlayer:
    def __init__(self, animations: tuple[Animation, ...]) -> None:
        validate_animations(animations)
        self.animations = animations
        self.animation_index = 0
        self.frame_index = 0
        self.completed_cycles = 0
        self.frame_elapsed = 0.0
        self.pause_remaining = 0.0

    @property
    def current_animation(self) -> Animation:
        return self.animations[self.animation_index]

    @property
    def current_frame(self) -> SpriteFrame:
        return self.current_animation.frames[self.frame_index]

    def advance(self, elapsed: float) -> None:
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError("Elapsed time must be finite and non-negative.")

        while elapsed > 0:
            if self.pause_remaining > 0:
                consumed = min(elapsed, self.pause_remaining)
                elapsed -= consumed
                self.pause_remaining -= consumed
                if self.pause_remaining <= TIME_EPSILON:
                    self.pause_remaining = 0.0
                    self.animation_index = (
                        self.animation_index + 1
                    ) % len(self.animations)
                    self.frame_index = 0
                    self.completed_cycles = 0
                    self.frame_elapsed = 0.0
                continue

            frame_delay = self.current_animation.frame_delay
            consumed = min(elapsed, frame_delay - self.frame_elapsed)
            elapsed -= consumed
            self.frame_elapsed += consumed

            if self.frame_elapsed >= frame_delay - TIME_EPSILON:
                self.frame_elapsed = 0.0
                self.frame_index += 1
                if self.frame_index == len(self.current_animation.frames):
                    self.frame_index = 0
                    self.completed_cycles += 1
                    if self.completed_cycles == ANIMATION_REPEAT_COUNT:
                        self.pause_remaining = ACTION_PAUSE


def draw_frame(sprite_sheet, frame: SpriteFrame) -> None:
    scale = min(
        SPRITE_MAX_WIDTH / MAX_FRAME_WIDTH,
        SPRITE_MAX_HEIGHT / MAX_FRAME_HEIGHT,
    )
    sprite_sheet.clip_draw(
        frame.left,
        frame.bottom,
        frame.width,
        frame.height,
        SPRITE_CENTER_X,
        SPRITE_CENTER_Y,
        frame.width * scale,
        frame.height * scale,
    )


def get_sprite_sheet_path() -> Path:
    return Path(__file__).resolve().with_name("sonic-sprite.png")


def main() -> None:
    validate_animations(ANIMATIONS)
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite_sheet = load_image(str(get_sprite_sheet_path()))
        player = AnimationPlayer(ANIMATIONS)
        previous_time = time.monotonic()
        print(f"재생 시작: {player.current_animation.name}")

        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT or (
                    event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                ):
                    running = False

            now = time.monotonic()
            previous_animation_index = player.animation_index
            player.advance(now - previous_time)
            previous_time = now
            if player.animation_index != previous_animation_index:
                print(f"재생 시작: {player.current_animation.name}")

            clear_canvas()
            draw_frame(sprite_sheet, player.current_frame)
            update_canvas()
            delay(1 / 60)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
