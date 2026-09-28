# 실습 과제 진행
import math

from pico2d import *


open_canvas(800, 600)
character = load_image('character.png')

left = 50
right = 750
top = 550
bottom = 50
speed = 5


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.02)


# 원운동
def draw_circle():
    center_x = 400
    center_y = 300
    radius = 100
    angle_step = 10

    for degree in range(0, 360, angle_step):
        theta = math.radians(degree)
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)
        draw_character(x, y)


# 사각운동
def draw_top():
    for x in range(left, right + 1, speed):
        draw_character(x, top)


# 사각운동
def draw_right():
    for y in range(top, bottom - 1, -speed):
        draw_character(right, y)


# 사각운동
def draw_bottom():
    for x in range(right, left - 1, -speed):
        draw_character(x, bottom)


# 사각운동
def draw_left():
    for y in range(bottom, top + 1, speed):
        draw_character(left, y)


# 사각운동
def draw_rectangle():
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()


# 삼각운동
def draw_triangle():
    for step in range(101):
        x = 400 + step * 3
        y = 550 - step * 5
        draw_character(x, y)


# 삼각운동
def draw_triangle_bottom():
    for x in range(700, 99, -speed):
        draw_character(x, bottom)


# 삼각운동
def draw_triangle_left():
    for step in range(101):
        x = 100 + step * 3
        y = bottom + step * 5
        draw_character(x, y)


running = True
while running:
    draw_circle()
    draw_rectangle()
    draw_triangle()
    draw_triangle_bottom()
    draw_triangle_left()

    for event in get_events():
        if event.type == SDL_QUIT or (
            event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
        ):
            running = False

close_canvas()
