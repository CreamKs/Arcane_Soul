from pico2d import *
import game_world
import game_framework
import random

class Attack:
    image = None

    def __init__(self, x = None, y = None):
        if Attack.image == None:
            Attack.image = load_image('Resource\eff_slash_line_w_spr_0.png')
        self.x = x
        self.y = y

    def setting(self, x, y, dmg = None):
        self.x = x
        self.y = y
        self.dmg = dmg

    def draw(self):
        pass

    def update(self):
        pass

    def get_bb(self):
        return self.x - 60, self.y - 60, self.x + 60, self.y + 60

    def handle_collision(self, group, other):
        match group:
            case 'attack:monster':
                other.hp -= self.dmg
                other.hp_per = int(other.hp / other.max_hp * 100)
                pass