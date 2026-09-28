# AI가 별도로 작성한 운동 구현
import math
from collections.abc import Iterable, Iterator

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
LEFT = 50
RIGHT = 750
TOP = 550
BOTTOM = 50
MOVE_STEP = 5
FRAME_DELAY = 0.02

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
character = load_image("character.png")


def draw_character(x: float, y: float) -> None:
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)


def play_path(points: Iterable[tuple[float, float]]) -> None:
    for x, y in points:
        draw_character(x, y)


def rectangle_path() -> Iterator[tuple[int, int]]:
    for x in range(LEFT, RIGHT + 1, MOVE_STEP):
        yield x, TOP
    for y in range(TOP, BOTTOM - 1, -MOVE_STEP):
        yield RIGHT, y
    for x in range(RIGHT, LEFT - 1, -MOVE_STEP):
        yield x, BOTTOM
    for y in range(BOTTOM, TOP + 1, MOVE_STEP):
        yield LEFT, y


def circle_path() -> Iterator[tuple[float, float]]:
    center_x = CANVAS_WIDTH / 2
    center_y = CANVAS_HEIGHT / 2
    radius = 100
    angle_step = 10

    for degrees in range(0, 360, angle_step):
        radians = math.radians(degrees)
        yield (
            center_x + radius * math.cos(radians),
            center_y + radius * math.sin(radians),
        )


def triangle_path() -> Iterator[tuple[int, int]]:
    for step_index in range(101):
        yield 400 + step_index * 3, TOP - step_index * 5
    for x in range(700, 99, -MOVE_STEP):
        yield x, BOTTOM
    for step_index in range(101):
        yield 100 + step_index * 3, BOTTOM + step_index * 5


def run_exercise() -> None:
    is_running = True
    while is_running:
        print("Circle")
        play_path(circle_path())
        print("Rectangle")
        play_path(rectangle_path())
        print("Triangle")
        play_path(triangle_path())

        for event in get_events():
            if event.type == SDL_QUIT:
                is_running = False
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                is_running = False

    close_canvas()


run_exercise()