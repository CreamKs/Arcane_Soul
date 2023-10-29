# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

import Gravity
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



class Idle:

    @staticmethod
    def enter(player, e):
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
            player.g = -1
            player.y += 5
        pass

    @staticmethod
    def do(player):
        if player.plus_frame % 10 == 0:
            player.frame += 1
            if player.frame == 11:
                player.frame = 0
        player.plus_frame += 1
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(player.frame * 99, 0, 99, 197, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(player.frame * 99, 0, 99, 197, 0, 'h', player.x, player.y, 99, 197)



class Run:

    @staticmethod
    def enter(player, e):
        player.image = load_image('Resource\Character\Walk.png')
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
        if c_down(e):
            player.jump = True
            player.g = -1
            player.y += 5
        pass

    @staticmethod
    def do(player):
        if player.plus_frame % 8 == 0:
            player.frame += 1
            if player.frame == 8:
                player.frame = 0
        player.plus_frame += 1
        player.x += player.dir * 5
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(player.frame * 101, 0, 101, 177, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(player.frame * 101, 0, 101, 177, 0, 'h', player.x, player.y, 101, 177)


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
        pass

    @staticmethod
    def exit(player, e):
        pass
    @staticmethod
    def do(player):
        if player.jump == False:
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
        player.x += player.dir * 5
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
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, c_down: Jump},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, c_down: JumpRun},
            Jump: {right_down: JumpRun, left_down: JumpRun, right_up: JumpRun, left_up: JumpRun, jump_end: Idle},
            JumpRun: {right_down: Jump, left_down: Jump, right_up: Jump, left_up: Jump, jump_end: Run},
            # Attack1: {},
            # Attack2: {},
            # Attack3: {},
            # ShowBow: {},
            # JumpShowBow: {},
            # Dead: {},
            # Skill1: {},
            # Skill2: {},
            # Skill3: {}
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
        self.x, self.y = 400, 90
        self.frame = 0
        self.plus_frame = 0
        self.dir = 0
        self.g = 0
        self.face_dir = 1 # 오른쪽 방향
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
