from pathlib import Path
import time

from pico2d import *


IDLE_FRAME_COUNT = 6
IDLE_FRAME_LEFT = 91
IDLE_FRAME_BOTTOM = 414
IDLE_FRAME_WIDTH = 81
IDLE_FRAME_HEIGHT = 80
IDLE_FRAME_DELAY = 0.12
WALK_FRAME_COUNT = 8
WALK_FRAME_LEFT = 91
WALK_FRAME_BOTTOM = 313
WALK_FRAME_WIDTH = 81
WALK_FRAME_HEIGHT = 80
WALK_FRAME_DELAY = 0.075
WALK_MOVEMENT_STEP = 20
RUN_FRAME_COUNT = 6
RUN_FRAME_LEFT = 91
RUN_FRAME_BOTTOM = 225
RUN_FRAME_WIDTH = 81
RUN_FRAME_HEIGHT = 80
RUN_FRAME_DELAY = 0.05
RUN_MOVEMENT_STEP = 16
RUN_ATTACK_FRAME_COUNT = 4
RUN_ATTACK_FRAME_LEFT = 91
RUN_ATTACK_FRAME_BOTTOM = 135
RUN_ATTACK_FRAME_WIDTH = 81
RUN_ATTACK_FRAME_HEIGHT = 80
RUN_ATTACK_FRAME_DELAY = 0.08
RUN_ATTACK_MOVEMENT_STEP = 13
ATTACK_1_FRAME_LEFTS = (91, 172, 280, 400)
ATTACK_1_FRAME_BOTTOM = 45
ATTACK_1_FRAME_WIDTH = 81
ATTACK_1_FRAME_HEIGHT = 80
ATTACK_1_FRAME_DELAY = 0.12
ATTACK_1_MOVEMENT_STEP = 13
CHARACTER_X_MIN = 134
CHARACTER_X_MAX = 666
CHARACTER_Y = 300
CHARACTER_WIDTH = 267
CHARACTER_HEIGHT = 264
ACTION_SEQUENCE = ("walk", "run", "run_attack", "attack1")
TRAVERSALS_PER_ACTION = 5
SEQUENCE_PAUSE = 1.0

open_canvas(800, 600)
sprite_sheet = load_image(str(Path(__file__).resolve().with_name("sprite_sheet.jpg")))

frame = 0
idle_frame = 0
character_x = CHARACTER_X_MIN
direction = 1
action = "walk"
action_index = 0
traversal_count = 0
action_change_pending = False
pause_until = 0.0
running = True
while running:
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    if running:
        now = time.monotonic()
        if pause_until and now >= pause_until:
            if action_change_pending:
                action_index = (action_index + 1) % len(ACTION_SEQUENCE)
                action = ACTION_SEQUENCE[action_index]
                traversal_count = 0
                action_change_pending = False
                frame = 0
            pause_until = 0.0
        paused = now < pause_until
        if action == "walk":
            frame_count = WALK_FRAME_COUNT
            frame_left = WALK_FRAME_LEFT
            frame_bottom = WALK_FRAME_BOTTOM
            frame_width = WALK_FRAME_WIDTH
            frame_height = WALK_FRAME_HEIGHT
            frame_delay = WALK_FRAME_DELAY
            movement_step = WALK_MOVEMENT_STEP
        elif action == "run":
            frame_count = RUN_FRAME_COUNT
            frame_left = RUN_FRAME_LEFT
            frame_bottom = RUN_FRAME_BOTTOM
            frame_width = RUN_FRAME_WIDTH
            frame_height = RUN_FRAME_HEIGHT
            frame_delay = RUN_FRAME_DELAY
            movement_step = RUN_MOVEMENT_STEP
        elif action == "run_attack":
            frame_count = RUN_ATTACK_FRAME_COUNT
            frame_left = RUN_ATTACK_FRAME_LEFT
            frame_bottom = RUN_ATTACK_FRAME_BOTTOM
            frame_width = RUN_ATTACK_FRAME_WIDTH
            frame_height = RUN_ATTACK_FRAME_HEIGHT
            frame_delay = RUN_ATTACK_FRAME_DELAY
            movement_step = RUN_ATTACK_MOVEMENT_STEP
        else:
            frame_count = len(ATTACK_1_FRAME_LEFTS)
            frame_left = 0
            frame_bottom = ATTACK_1_FRAME_BOTTOM
            frame_width = ATTACK_1_FRAME_WIDTH
            frame_height = ATTACK_1_FRAME_HEIGHT
            frame_delay = ATTACK_1_FRAME_DELAY
            movement_step = ATTACK_1_MOVEMENT_STEP

        if paused:
            frame_x = IDLE_FRAME_LEFT + idle_frame * IDLE_FRAME_WIDTH
            frame_bottom = IDLE_FRAME_BOTTOM
            frame_width = IDLE_FRAME_WIDTH
            frame_height = IDLE_FRAME_HEIGHT
        elif action == "attack1":
            frame_x = ATTACK_1_FRAME_LEFTS[frame]
        else:
            frame_x = frame_left + frame * frame_width

        clear_canvas()
        sprite_sheet.clip_draw(0, 0, 40, 40, 400, 300, 800, 600)
        if direction > 0:
            sprite_sheet.clip_draw(
                frame_x,
                frame_bottom,
                frame_width,
                frame_height,
                character_x,
                CHARACTER_Y,
                CHARACTER_WIDTH,
                CHARACTER_HEIGHT,
            )
        else:
            sprite_sheet.clip_composite_draw(
                frame_x,
                frame_bottom,
                frame_width,
                frame_height,
                0,
                "h",
                character_x,
                CHARACTER_Y,
                CHARACTER_WIDTH,
                CHARACTER_HEIGHT,
            )
        update_canvas()

        if paused:
            idle_frame = (idle_frame + 1) % IDLE_FRAME_COUNT
            delay(IDLE_FRAME_DELAY)
            continue

        frame = (frame + 1) % frame_count
        character_x += direction * movement_step
        if character_x >= CHARACTER_X_MAX or character_x <= CHARACTER_X_MIN:
            character_x = min(max(character_x, CHARACTER_X_MIN), CHARACTER_X_MAX)
            direction *= -1
            pause_until = time.monotonic() + SEQUENCE_PAUSE
            idle_frame = 0
            traversal_count += 1
            if traversal_count == TRAVERSALS_PER_ACTION:
                action_change_pending = True

        delay(frame_delay)

close_canvas()