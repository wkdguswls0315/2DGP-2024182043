from pico2d import *
from math import *

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

angle = 0

while True:

    x = 400 + 150 * cos(angle)
    y = 300 + 150 * sin(angle)

    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)

    update_canvas()

    angle += 0.02

    if angle > 2 * pi:
        angle = 0

    delay(0.01)