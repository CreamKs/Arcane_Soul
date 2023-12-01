import random

from pico2d import *

import Monster
import game_framework

import game_world
import menu_mode
from Player import Player

from slime1 import Slime1
from Map import BackGround, Tile
from slime2 import Slime2


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            finish()
            game_framework.change_mode(menu_mode)


        else:
            player.handle_event(event)




def init():
    global zen_timer
    global player

    zen_timer = get_time()

    player = Player()
    game_world.add_object(player, 2)
    game_world.add_collision_pair('object:tile', player, None)
    game_world.add_collision_pair('player:monster', player, None)

    Monster.Respawn()

    background = BackGround()
    game_world.add_object(background, 0)

    tiles = [Tile(i * 60 + 30, 80) for i in range(37)]
    game_world.add_objects(tiles, 0)
    for tile in tiles:
        game_world.add_collision_pair('object:tile', None, tile)

def finish():
    game_world.clear()
    pass


def update():
    global zen_timer

    if zen_timer - get_time() > 30:
        Monster.Respawn()
        zen_timer = get_time()

    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

