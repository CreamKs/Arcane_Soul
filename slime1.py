from pico2d import *

import random
import math

import Gravity
import game_framework
import game_world
import Monster
from Player import TIME_PER_ATTACK, time_out
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode


# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8.0

animation_names = ['walk', 'attack']

attack = lambda e : e[0] == 'ATTACK'

class Run:
    @staticmethod
    def enter(slime1, e):
        global FRAMES_PER_ACTION

        FRAMES_PER_ACTION = 8
        slime1.frame = 0
        slime1.state = 'walk'

    @staticmethod
    def exit(slime1, e):
        pass

    @staticmethod
    def do(slime1):
        if(slime1.x < play_mode.player.x):
            slime1.dir = 1
        if(slime1.x > play_mode.player.x):
            slime1.dir = -1
        slime1.frame = (slime1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        slime1.x += slime1.dir * RUN_SPEED_PPS * game_framework.frame_time
        if slime1.x < 50 or slime1.x > 1870:
            slime1.x -= slime1.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(slime1):
        pass


class Attack1:
    @staticmethod
    def enter(slime1, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 4
        slime1.state = 'attack'
        slime1.frame = 0

    @staticmethod
    def exit(slime1, e):
        pass


    @staticmethod
    def do(slime1):
        slime1.frame = (slime1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if int(slime1.frame) == 4:
            slime1.state_machine.handle_event(('TIME_OUT', 0))
            play_mode.player.hp -= 10
            play_mode.player.hp_per = int(play_mode.player.hp / play_mode.player.max_hp * 100)
            play_mode.player.state_machine.handle_event(("HIT", 0))

        pass

    @staticmethod
    def draw(slime1):
        pass



class StateMachine:
    def __init__(self, slime1):
        self.slime1 = slime1
        self.cur_state = Run
        self.transitions = {
            Run: {attack:Attack1},
            Attack1: {time_out: Run}
        }

    def start(self):
        self.cur_state.enter(self.slime1, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.slime1)
        Gravity.Gravity_World(self.slime1)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.slime1, e)
                self.cur_state = next_state
                self.cur_state.enter(self.slime1, e)
        return False

    def draw(self):
        self.cur_state.draw(self.slime1)



class Slime1:
    images = None
    def load_images(self):
        if Slime1.images == None:
            Slime1.images = {}
            for name in animation_names:
                Slime1.images[name] = load_image("Resource/Monster/slime/" + name + "1.png")

    def __init__(self):
        self.HPbar = load_image("Resource\HP\HPbar.png")
        self.HPbase = load_image("Resource\HP\HPbase.png")

        self.max_hp = 300
        self.hp = 300
        self.hp_per = 100
        self.dmg = 10
        self.x = random.randint(0, 1920)
        self.y = 0
        self.h = 50
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 7)
        self.load_images()
        self.jump = False
        self.jump_power = 0
        self.state = 'walk'
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.imgx = 113
        self.imgy = 125

    def get_bb(self):
        return self.x - (self.imgx / 2), self.y - (self.imgy / 2), self.x + (self.imgx / 2), self.y + (self.imgy / 2)


    def update(self):
        self.state_machine.update()
        if self.hp < 0:
            play_mode.background.score += 200
            game_world.remove_object(self)
            game_world.remove_collision_object(self)

    def draw(self):
        if self.dir == 1:
            Slime1.images[self.state].clip_draw(int(self.frame) * self.imgx, 0, self.imgx, self.imgy, self.x, self.y)
        if self.dir == -1:
            Slime1.images[self.state].clip_composite_draw(int(self.frame) * self.imgx, 0, self.imgx, self.imgy, 0, 'h', self.x, self.y, self.imgx, self.imgy)
        self.state_machine.draw()
        self.HPbase.draw(self.x, self.y + 100, 100, 8)
        self.HPbar.draw(self.x - (100 - self.hp_per) / 2, self.y + 100, self.hp_per, 8)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        match group:
            case 'object:tile':
                self.y += 120
                self.jump = False
            case 'player:monster':
                self.state_machine.handle_event(('ATTACK', 0))
