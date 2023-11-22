from pico2d import *

import random
import math

import Gravity
import game_framework
import game_world
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

animation_names = ['Walk', 'Idle']

class Idle:

    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION

        FRAMES_PER_ACTION = 11
        player.image = load_image('Resource\Character\Idle.png')

        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
       pass

    @staticmethod
    def draw(slime1):
        if math.cos(slime1.dir) < 0:
            Slime1.image.clip_composite_draw(int(slime1.frame) * slime1.imgx, 0, slime1.imgx, slime1.imgy, 0, 'h', slime1.x1,
                                             slime1.y, 100, 100)
        else:
            Slime1.image.clip_draw(int(slime1.frame) * slime1.imgx, 0, slime1.imgx, slime1.imgy, slime1.x, slime1.y, 100, 100)

class Idle:

    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION

        FRAMES_PER_ACTION = 8
        player.image = load_image('Resource\Monster\walk1.png')
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(slime1):
        slime1.frame = (slime1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    pass

    @staticmethod
    def draw(slime1):
        if math.cos(slime1.dir) < 0:
            Slime1.image.clip_composite_draw(int(slime1.frame) * slime1.imgx, 0, slime1.imgx, slime1.imgy, 0, 'h', slime1.x1,
                                             slime1.y, 100, 100)
        else:
            Slime1.image.clip_draw(int(slime1.frame) * slime1.imgx, 0, slime1.imgx, slime1.imgy, slime1.x, slime1.y, 100, 100)
class Run:

    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION

        FRAMES_PER_ACTION = 8
        player.image = load_image('Resource\Monster\walk1.png')

        pass

    @staticmethod
    def exit(slime1, e):
        pass

    @staticmethod
    def do(slime1):
        slime1.frame = (slime1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        slime1.x += slime1.dir * RUN_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(slime1):
        if math.cos(slime1.dir) < 0:
            Slime1.image.clip_composite_draw(int(slime1.frame) * slime1.imgx, 0, slime1.imgx, slime1.imgy, 0, 'h', slime1.x1,
                                             slime1.y, 100, 100)
        else:
            Slime1.image.clip_draw(int(slime1.frame) * slime1.imgx, 0, slime1.imgx, slime1.imgy, slime1.x, slime1.y, 100, 100)


class Attack:
    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION

        FRAMES_PER_ACTION = 8
        player.image = load_image('Resource\Monster\walk1.png')

        pass

    @staticmethod
    def exit(slime1, e):
        pass

    @staticmethod
    def do(slime1):
        slime1.frame = (slime1.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        slime1.x += slime1.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(slime1):
        if math.cos(slime1.dir) < 0:
            Slime1.image.clip_composite_draw(int(slime1.frame) * slime1.imgx, 0, slime1.imgx, slime1.imgy, 0, 'h',
                                             slime1.x1, slime1.y, 100, 100)
        else:
            Slime1.image.clip_draw(int(slime1.frame) * slime1.imgx, 0, slime1.imgx, slime1.imgy, slime1.x, slime1.y,
                                   100, 100)


class StateMachine:
    def __init__(self, slime1):
        self.slime1 = slime1
        self.cur_state = Idle
        self.transitions = {
            Idle,
            Run
        }

    def start(self):
        self.cur_state.enter(self.slime1, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.slime1)
        Gravity.Gravity_World(self.slime1)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            self.cur_state.exit(self.slime1, e)
            self.cur_state = next_state
            self.cur_state.enter(self.slime1, e)
            return True

        return False

    def draw(self):
        self.cur_state.draw(self.slime1)



class Slime1:

    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = 75
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 7)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        Slime1.image = None
        self.jump = False
        self.jump_power = 0
        self.imgx = 113
        self.imgy = 125
        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # fill here
        self.bt.run()

    def draw(self):
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass


    def distance_less_than(self, x1, x2, r):
        distance2 = (x1 - x2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2
        pass

    def move_slightly_to(self, tx):
        self.dir = math.atan2(0, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        pass


    def is_player_nearby(self, r):
        if self.distance_less_than(play_mode.player.x, self.x, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_player(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.player.x)
        if self.distance_less_than(play_mode.player.x, self.x, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('플레이어가 근처에 있는가?', self.is_player_nearby, 7)
        a1 = Action('플레이어에게 접근', self.move_to_player)
        root = SEQ_chase_player = Sequence('플레이어 추적', c1, a1)

        root = SEL_near_or_not = Selector('소년이 주변에 존재 또는 비존재', SEQ_chase_player)

        self.bt = BehaviorTree(root)
        pass
