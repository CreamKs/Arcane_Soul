from pico2d import get_time

import game_framework
import Player
def Gravity_World(o):
    g = 0.98
    if o.jump == True:
        o.y -= o.jump_power * Player.RUN_SPEED_PPS * g * game_framework.frame_time
        o.jump_power += 0.1
    else:
        o.y = o.h
