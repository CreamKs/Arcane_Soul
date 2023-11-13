# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import Gravity
import game_framework
import game_world
from sdl2 import SDLK_c, SDLK_x


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

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

def attack_down(e):
    return e[0] == 'ATTACK' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

def jump_end(e):
    return e[0] == 'JUMP_END'


time_out = lambda e : e[0] == 'TIME_OUT'
next_attack = lambda e : e[0] == 'NEXT_ATTACK'


PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Jump Speed

# Gravity

# Boy Action Speed

TIME_PER_ACTION = 0.5
TIME_PER_ATTACK = 0.2

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
            player.jump_power = -10
            player.y += 10
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 99, 0, 99, 197, player.x, player.y, 100, 181)
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 99, 0, 99, 197, 0, 'h', player.x, player.y, 100, 181)



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
            player.jump_power = -10
            player.y += 10
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
        if player.y < 90:
            player.jump = False
            player.state_machine.handle_event(('JUMP_END', 0))
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(0, 0, 86, 180, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(0, 0, 86, 180, 0, 'h', player.x, player.y, 86, 180)


class Attack1:
    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 4
        player.frame = 0
        player.attack = False
        player.image = load_image('Resource\Character\Attack1.png')
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
            pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4
        if int(player.frame) == 3:
            if player.attack:
                player.state_machine.handle_event(('NEXT_ATTACK', 0))
            else:
                player.state_machine.handle_event(('TIME_OUT', 0))

        pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 216, 0, 216, 181, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 216, 0, 216, 181, 0, 'h', player.x, player.y, 216, 181)


class Attack2:
    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 4
        player.attack = False
        player.frame = 0
        player.image = load_image('Resource\Character\Attack2.png')
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
            pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4

        if int(player.frame) == 3:
            if player.attack:
                player.state_machine.handle_event(('NEXT_ATTACK', 0))
            else:
                player.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(int(player.frame) * 215, 0, 215, 165, player.x, player.y- (181 - 175))
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 215, 0, 215, 165, 0, 'h', player.x, player.y - (181 - 175), 215, 165)


class Attack3:
    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 4
        player.frame = 0
        player.attack = False
        player.image = load_image('Resource\Character\Attack3.png')
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
            pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4
        if int(player.frame > 2):
            player.x += player.face_dir * RUN_SPEED_PPS * game_framework.frame_time * 8

        if int(player.frame) == 3:
            if player.attack:
                player.state_machine.handle_event(('NEXT_ATTACK', 0))
            else:
                player.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(int(player.frame) * 181, 0, 181, 139, player.x, player.y - (181 - 150))
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 181, 0, 181, 139, 0, 'h', player.x, player.y - (181 - 150), 181, 139)


class Dead:
    @staticmethod
    def enter(player, e):
        player.image = load_image('Resource\Character\dead.png')
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(int(player.frame) * 181, 0, 181, 139, player.x, player.y - (181 - 150))
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 181, 0, 181, 139, 0, 'h', player.x, player.y - (181 - 150), 181, 139)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, c_down: Jump, x_down: Attack1},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, c_down: JumpRun, x_down: Attack1},
            Jump: {right_down: JumpRun, left_down: JumpRun, right_up: JumpRun, left_up: JumpRun, jump_end: Idle},
            JumpRun: {right_down: Jump, left_down: Jump, right_up: Jump, left_up: Jump, jump_end: Run},
            Attack1: {time_out: Idle, next_attack: Attack2},
            Attack2: {time_out: Idle, next_attack: Attack3},
            Attack3: {time_out: Idle},
            Dead: {},
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
                if not e[0] == 'ATTACK':
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
        self.jump = False
        self.jump_power = 0
        self.attack = False
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, e):
        if e.key == SDLK_x and (self.state_machine.cur_state == Attack1 or self.state_machine.cur_state == Attack2):
            self.state_machine.handle_event(('ATTACK', e))
            self.attack = True
        else:
            self.state_machine.handle_event(('INPUT', e))

    def draw(self):
        self.state_machine.draw()
