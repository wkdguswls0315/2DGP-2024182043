from pathlib import Path

from pico2d import *


ANIMATIONS = (
    ("IDLE", 6),
    ("WALK", 8),
    ("RUN", 6),
    ("RUN+ATTACK", 4),
    ("ATTACK 1", 4),
)


def print_frame_ranges():
    first_sheet_frame = 1

    print("Animation frame ranges (local / whole sheet):")
    for name, frame_count in ANIMATIONS:
        last_sheet_frame = first_sheet_frame + frame_count - 1
        print(
            f"{name}: 1-{frame_count} "
            f"(whole sheet: {first_sheet_frame}-{last_sheet_frame})"
        )
        first_sheet_frame = last_sheet_frame + 1


print_frame_ranges()

open_canvas(800, 600)
sprite_sheet = load_image(str(Path(__file__).resolve().with_name("sprite_sheet.jpg")))

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
        sprite_sheet.draw(400, 300)
        update_canvas()
        delay(0.01)

close_canvas()