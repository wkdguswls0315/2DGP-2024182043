# 실습 과제 진행
from pico2d import *
import math
# 맨 처음 해야할 일은.
open_canvas(800, 600)
character = load_image('character.png')


def draw_circle():
    print("circle")
    center_x = 400
    center_y = 300
    radius = 100
    angle_step = 10
    for degree in range(0, 360, angle_step):
        theta = math.radians(degree)
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.02)


def draw_top():
    print("top")
    for x in range(50, 751, 5):
        draw_character(x, 550)

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.02)

def draw_right():
    print("right")
    for y in range(550, 49, -5):
        draw_character(750, y)

def draw_bottom():
    print("bottom")
    for x in range(750, 49, -5):
        draw_character(x, 50)

def draw_left():
    print("left")
    for y in range(50, 551, 5):
        draw_character(50, y)

def draw_triangle():
    print("triangle")
    for step in range(101):
        x = 400 + step * 3
        y = 550 - step * 5
        draw_character(x, y)

def draw_triangle_bottom():
    print("triangle bottom")
    for x in range(700, 99, -5):
        draw_character(x, 50)

def draw_triangle_left():
    print("triangle left")
    for step in range(101):
        x = 100 + step * 3
        y = 50 + step * 5
        draw_character(x, y)


def draw_rectangle():
    print("rectangle")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()

running = True
while running:
    draw_circle()
    draw_rectangle()
    draw_triangle()
    draw_triangle_bottom()
    draw_triangle_left()

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

close_canvas()
