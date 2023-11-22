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

    def setting(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 60, self.y - 10, self.x + 60, self.y + 10

    def handle_collision(self, group, other):
        match group:
            case 'boy:ball':
                game_world.remove_object(self)
            case 'zombie:ball':
                game_world.remove_object(self)