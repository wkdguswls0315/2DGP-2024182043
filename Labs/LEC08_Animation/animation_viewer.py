from pathlib import Path

from pico2d import *


WALK_FRAME_COUNT = 8
WALK_FRAME_WIDTH = 81
WALK_FRAME_HEIGHT = 80
WALK_FRAME_LEFT = 91
WALK_FRAME_BOTTOM = 313
FRAME_DELAY = 0.08
CHARACTER_X_MIN = 80
CHARACTER_X_MAX = 720
CHARACTER_Y = 300
CHARACTER_WIDTH = 162
CHARACTER_HEIGHT = 160
MOVEMENT_STEP = 8

open_canvas(800, 600)
sprite_sheet = load_image(str(Path(__file__).resolve().with_name("sprite_sheet.jpg")))

frame = 0
character_x = CHARACTER_X_MIN
direction = 1
running = True
while running:
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    if running:
        clear_canvas()
        sprite_sheet.clip_draw(0, 0, 40, 40, 400, 300, 800, 600)
        if direction > 0:
            sprite_sheet.clip_draw(
                WALK_FRAME_LEFT + frame * WALK_FRAME_WIDTH,
                WALK_FRAME_BOTTOM,
                WALK_FRAME_WIDTH,
                WALK_FRAME_HEIGHT,
                character_x,
                CHARACTER_Y,
                CHARACTER_WIDTH,
                CHARACTER_HEIGHT,
            )
        else:
            sprite_sheet.clip_composite_draw(
                WALK_FRAME_LEFT + frame * WALK_FRAME_WIDTH,
                WALK_FRAME_BOTTOM,
                WALK_FRAME_WIDTH,
                WALK_FRAME_HEIGHT,
                0,
                "h",
                character_x,
                CHARACTER_Y,
                CHARACTER_WIDTH,
                CHARACTER_HEIGHT,
            )
        update_canvas()
        frame = (frame + 1) % WALK_FRAME_COUNT
        character_x += direction * MOVEMENT_STEP
        if character_x >= CHARACTER_X_MAX or character_x <= CHARACTER_X_MIN:
            direction *= -1
        delay(FRAME_DELAY)

close_canvas()