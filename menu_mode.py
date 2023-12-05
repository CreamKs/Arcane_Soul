import random
import json
import tomllib
import pickle
import os

from pico2d import *
import game_framework
import game_world
import guide_mode

import play_mode


def init():
    global menu
    menu = load_image('Resource\Title\Title.png')
    hide_cursor()
    hide_lattice()

def finish():
    global menu
    menu = None

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
                game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            create_new_world()
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_g:
            game_framework.change_mode(guide_mode)

def update():
    pass

def draw():
    clear_canvas()
    menu.draw(get_canvas_width()//2, get_canvas_height()//2)
    update_canvas()






