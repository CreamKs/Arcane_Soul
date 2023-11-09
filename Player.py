# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import Gravity
import game_framework
import game_world
from sdl2 import SDLK_c


# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def c_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c

def jump_end(e):
    return e[0] == 'JUMP_END'

# time_out = lambda e : e[0] == 'TIME_OUT'

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Jump Speed

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
JUMP_SPEED_MPS = 0
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

# Gravity

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
GRAVITY_ACCELERATION = 9.8
GRAVITY_TIME = 0
GRAVITY_SPEED_MPS = GRAVITY_TIME * GRAVITY_ACCELERATION
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)
GRAVITY_SPEED_MAX = 200.0

# Boy Action Speed
# fill here

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8




class Idle:

    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION

        FRAMES_PER_ACTION = 11
        player.image = load_image('Resource\Character\Idle.png')
        player.dir = 0
        player.frame = 0
        player.plus_frame = 0
        player.wait_time = get_time() # pico2d import 필요

        pass

    @staticmethod
    def exit(player, e):
        if c_down(e):
            player.jump = True
            player.jump_power = 20
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 99, 0, 99, 197, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 99, 0, 99, 197, 0, 'h', player.x, player.y, 99, 197)



class Run:

    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION

        FRAMES_PER_ACTION = 8

        player.image = load_image('Resource\Character\Walk.png')
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
        if c_down(e):
            player.jump = True
            player.y += 10
            player.jump_power = 100
            pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time

        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(int(player.frame) * 101, 0, 101, 177, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 101, 0, 101, 177, 0, 'h', player.x, player.y, 101, 177)


class Jump:
    @staticmethod
    def enter(player, e):
        global JUMP_SPEED_KMPH
        global JUMP_SPEED_MPM
        global JUMP_SPEED_MPS
        global JUMP_SPEED_PPS
        JUMP_SPEED_MPS = player.jump_power
        JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)
        player.image = load_image('Resource\Character\Jump.png')
        if player.face_dir == -1:
            player.action = 2
        elif player.face_dir == 1:
            player.action = 3
        player.dir = 0
        player.frame = 0
        player.timer = get_time()
        pass

    @staticmethod
    def exit(player, e):
        player.jump_power = 0
        pass
    @staticmethod
    def do(player):
        player.y += JUMP_SPEED_PPS * game_framework.frame_time


        if player.y < 90:
            player.jump = False
            player.state_machine.handle_event(('JUMP_END', 0))


    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(0, 0, 86, 180, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(0, 0, 86, 180, 0, 'h', player.x, player.y, 86, 180)


class JumpRun:
    @staticmethod
    def enter(player, e):
        player.image = load_image('Resource\Character\Jump.png')
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if player.jump == False:
            player.state_machine.handle_event(('JUMP_END', 0))
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(0, 0, 86, 180, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(0, 0, 86, 180, 0, 'h', player.x, player.y, 86, 180)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Jump
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, c_down: Jump},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, c_down: JumpRun},
            Jump: {right_down: JumpRun, left_down: JumpRun, right_up: JumpRun, left_up: JumpRun, jump_end: Idle},
            JumpRun: {right_down: Jump, left_down: Jump, right_up: Jump, left_up: Jump, jump_end: Run},
            # Attack1: {},
            # Attack2: {},
            # Attack3: {},
            # Dead: {},
            # Skill1: {},
            # Skill2: {}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)
        Gravity.Gravity_World(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)





class Player:
    def __init__(self):
        self.x, self.y = 400, 100
        self.timer = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1 # 오른쪽 방향
        self.jump = True
        self.jump_power = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
