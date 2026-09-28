# 실습 과제 진행
from pico2d import *
import math
# 맨 처음 해야할 일은.
open_canvas(800, 600)
character = load_image('character.png')


def draw_circle():
    print("circle")
    for degree in range(0, 360, 10):
        theta = math.radians(degree)
        x = 400 + 100 * math.cos(theta)
        y = 300 + 100 * math.sin(theta)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)


def draw_top():
    print("top")
    for x in range(50, 751, 5):
        draw_character(x, 550)

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)

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



def draw_rectangle():
    print("rectangle")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()

def draw_triangle():
    print("triangle")
    clear_canvas()
    character.draw(400, 300)
    update_canvas()
    pass

running = True
while running:
    # 필요한 부분만 실행하려면 아래 함수 호출의 주석을 바꾸세요.
    draw_circle()
    draw_rectangle()
    # draw_triangle()

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

close_canvas()
