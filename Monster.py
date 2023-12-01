import random

import game_world
import slime1
import slime2

class Monster:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = random.randint(1, 2)
        if self.type == 1:
            self.monster = slime1.Slime1()
        if self.type == 2:
            self.monster = slime2.Slime2()

    def get_bb(self):
        return self.x - 60, self.y - 90, self.x + 60, self.y + 90


    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass


def Respawn():
    for i in range(10):
        monster = Monster()
        game_world.add_object(monster.monster, 2)
        game_world.add_collision_pair('object:tile', monster.monster, None)
        game_world.add_collision_pair('player:monster', None, monster.monster)
        game_world.add_collision_pair('attack:monster', None, monster.monster)
    pass