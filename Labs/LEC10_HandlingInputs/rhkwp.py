from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
CHARACTER_WIDTH, CHARACTER_HEIGHT = 100, 100

open_canvas(TUK_WIDTH, TUK_HEIGHT)

tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')


def handle_events():
    global running

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            else:
                keys_down.add(event.key)

        elif event.type == SDL_KEYUP:
            keys_down.discard(event.key)


def move_character():
    global x, y, facing_right, moving
    previous_x, previous_y = x, y

    if SDLK_LEFT in keys_down and SDLK_RIGHT not in keys_down:
        x -= 10
        facing_right = False
    elif SDLK_RIGHT in keys_down and SDLK_LEFT not in keys_down:
        x += 10
        facing_right = True

    if SDLK_UP in keys_down and SDLK_DOWN not in keys_down:
        y += 10
    elif SDLK_DOWN in keys_down and SDLK_UP not in keys_down:
        y -= 10

    x = max(CHARACTER_WIDTH // 2, min(x, TUK_WIDTH - CHARACTER_WIDTH // 2))
    y = max(CHARACTER_HEIGHT // 2, min(y, TUK_HEIGHT - CHARACTER_HEIGHT // 2))
    moving = x != previous_x or y != previous_y


running = True
frame = 0
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
facing_right = True
moving = False
keys_down = set()

while running:
    clear_canvas()

    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    character.clip_draw(
        frame * 100,
        (100 if moving else 300) if facing_right else (0 if moving else 200),
        CHARACTER_WIDTH,
        CHARACTER_HEIGHT,
        x,
        y
    )

    update_canvas()

    handle_events()
    move_character()

    frame = (frame + 1) % 8
    delay(0.05)


close_canvas()