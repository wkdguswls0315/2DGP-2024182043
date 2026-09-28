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
    pass

def draw_left():
    print("left")
    pass

def draw_bottom():
    print("bottom")
    pass

def draw_right():
    print("right")
    pass



def draw_rectangle():
    print("rectangle")
    clear_canvas()
    draw_top()
    draw_left()
    draw_bottom()
    draw_right()
    pass

def draw_triangle():
    print("triangle")
    clear_canvas()
    character.draw(400, 300)
    update_canvas()
    pass

running = True
while running:
    draw_circle()
    draw_rectangle()
    draw_triangle() 

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

close_canvas()
