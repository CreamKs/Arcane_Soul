from pico2d import get_time

import game_framework
import Player
def Gravity_World(o):
    if o.jump == True:
        Player.GRAVITY_TIME += 1
        o.timer = get_time()
        Player.GRAVITY_SPEED_MPS += Player.GRAVITY_ACCELERATION
        Player.GRAVITY_SPEED_PPS = (Player.GRAVITY_SPEED_MPS * Player.PIXEL_PER_METER)
        if(Player.GRAVITY_SPEED_MPS < Player.GRAVITY_SPEED_MAX):
            o.y -= Player.GRAVITY_SPEED_PPS * game_framework.frame_time
        else:
            o.y -= Player.GRAVITY_SPEED_MAX * game_framework.frame_time
    else:
        Player.GRAVITY_TIME = 0
        Player.GRAVITY_SPEED_MPS = Player.GRAVITY_TIME * Player.GRAVITY_ACCELERATION
        Player.GRAVITY_SPEED_PPS = (Player.GRAVITY_SPEED_MPS * Player.PIXEL_PER_METER)
        Player.GRAVITY_SPEED_MAX = 200.0
        o.y = 90
