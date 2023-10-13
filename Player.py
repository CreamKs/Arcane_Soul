# 이것은 각 상태들을 객체로 구현한 것임.
import math

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_a


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def time_out(e):
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def FramePlus(player, frame):
    if player.count % 10 == 0:
        player.frame += 1
        if player.frame > frame - 1:
            player.frame = 0
    player.count += 1


class Idle:
    @staticmethod
    def enter(player, e):
        player.image = load_image('Resource/Character/Idle.png')
        player.count = 0
        player.frame = 0
        player.start_time = get_time()

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        FramePlus(player, 11)

    @staticmethod
    def draw(player):
        if (player.dir > 0):
            player.image.clip_draw(player.frame * 99, 0, 99, 180, player.x, player.y)
        elif (player.dir < 0):
            player.image.clip_composite_draw(player.frame * 99, 0, 99, 180, 0, 'h', player.x, player.y, 99, 180)


class Run:
    @staticmethod
    def enter(player, e):
        player.image = load_image('Resource/Character/Walk.png')
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir = -1
    @staticmethod
    def exit(player, e):
        pass
    @staticmethod
    def do(player):
        FramePlus(player, 8)
        player.x += player.dir * 5
        pass
    @staticmethod
    def draw(player):
        if(player.dir > 0):
            player.image.clip_draw(player.frame * 101, 0, 101, 177, player.x, player.y)
        elif(player.dir < 0):
            player.image.clip_composite_draw(player.frame * 101, 0, 101, 177,0, 'h', player.x, player.y, 101, 177)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
        }
    def start(self):
        self.cur_state.enter(self.player, ('START', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, event):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(event):
                self.cur_state.exit(self.player, event)
                self.cur_state = next_state
                self.cur_state.enter(self.player, event)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.dir = 1
        self.count = 0
        self.frame = 0
        self.start_time = 0
        self.image = load_image('Resource/Character/Idle.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
