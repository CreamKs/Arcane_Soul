import random
import json
import tomllib
import pickle
import os

from pico2d import *
import game_framework
import game_world
import menu_mode

import play_mode


def init():
    global over
    over = load_image('Resource\Title\Gameover.png')
    hide_cursor()
    hide_lattice()

def finish():
    global over
    over = None

def pause():
    pass

def resume():
    pass


def create_new_world():
    pass

    # fill here


def load_saved_world():
    # fill here
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(menu_mode)

def update():
    pass

def draw():
    clear_canvas()
    over.draw(get_canvas_width()//2, get_canvas_height()//2)
    play_mode.background.font.draw(300, 1010, f'{ play_mode.background.score}', (0, 0, 255))
    update_canvas()






