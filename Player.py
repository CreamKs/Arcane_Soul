# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, draw_rectangle

import Gravity
import game_framework
import game_world
from sdl2 import SDLK_c, SDLK_x, SDLK_a, SDLK_s

import over_mode
from attack import Attack


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

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def attack_down(e):
    return e[0] == 'ATTACK' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

def jump_end(e):
    return e[0] == 'JUMP_END'

hit = lambda e : e[0] == 'HIT'
dead = lambda e : e[0] == 'DEAD'
time_out = lambda e : e[0] == 'TIME_OUT'
next_attack = lambda e : e[0] == 'NEXT_ATTACK'
life_end = lambda  e : e[0] == 'DEAD'
idle_go = lambda  e : e[0] == 'IDLE_GO'
run_go = lambda  e : e[0] == 'RUN_GO'

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
        player.jump_power = 0
        player.wait_time = get_time() # pico2d import 필요

        pass

    @staticmethod
    def exit(player, e):
        if c_down(e):
            player.jump = True
            player.jump_power = -15
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
        player.jump_power = 0

        player.image = load_image('Resource\Character\Walk.png')
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
        if c_down(e):
            player.jump = True
            player.jump_power = -15
            player.y += 10
            pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        if player.x < 50 or player.x > 1870:
            player.x -= player.dir * RUN_SPEED_PPS * game_framework.frame_time

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
        if player.x < 50 or player.x > 1870:
            player.x -= player.dir * RUN_SPEED_PPS * game_framework.frame_time
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
        player.vfx.setting(player.x + player.face_dir * 100, player.y, player.dmg)
        game_world.add_object(player.vfx)
        game_world.add_collision_pair('attack:monster',player.vfx, None)

        player.attack = False
        player.image = load_image('Resource\Character\Attack1.png')

    @staticmethod
    def exit(player, e):
        game_world.remove_object(player.vfx)
        game_world.remove_collision_object(player.vfx)

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4
        if int(player.frame) == 3:
            if player.attack:
                player.state_machine.handle_event(('NEXT_ATTACK', 0))
            else:
                if player.dir == 0:
                    player.state_machine.handle_event(('IDLE_GO', 0))
                else:
                    player.state_machine.handle_event(('RUN_GO', 0))


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
        player.vfx.setting(player.x + player.face_dir * 100, player.y, player.dmg)
        game_world.add_object(player.vfx)
        game_world.add_collision_pair('attack:monster',player.vfx, None)

    @staticmethod
    def exit(player, e):
        game_world.remove_object(player.vfx)
        game_world.remove_collision_object(player.vfx)
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4

        if int(player.frame) == 3:
            if player.attack:
                player.state_machine.handle_event(('NEXT_ATTACK', 0))
            else:
                if player.dir == 0:
                    player.state_machine.handle_event(('IDLE_GO', 0))
                else:
                    player.state_machine.handle_event(('RUN_GO', 0))
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

        player.vfx.setting(player.x + player.face_dir * 100, player.y, player.dmg)
        game_world.add_object(player.vfx)
        game_world.add_collision_pair('attack:monster',player.vfx, None)

    @staticmethod
    def exit(player, e):
        game_world.remove_object(player.vfx)
        game_world.remove_collision_object(player.vfx)
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4
        if int(player.frame > 2):
            player.x += player.face_dir * RUN_SPEED_PPS * game_framework.frame_time * 8
            if player.x < 50:
               player.x = 50
            if player.x > 1870:
                player.x = 1870

        if int(player.frame) == 3:
            if player.attack:
                player.state_machine.handle_event(('NEXT_ATTACK', 0))
            else:
                if player.dir == 0:
                    player.state_machine.handle_event(('IDLE_GO', 0))
                else:
                    player.state_machine.handle_event(('RUN_GO', 0))
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(int(player.frame) * 181, 0, 181, 139, player.x, player.y - (181 - 150))
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 181, 0, 181, 139, 0, 'h', player.x, player.y - (181 - 150), 181, 139)

class Hit:
    @staticmethod
    def enter(player, e):
        if player.hp < 0:
            player.state_machine.handle_event(('DEAD', 0))
        player.image = load_image('Resource\Character\Hit.png')
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0
        player.timer = get_time()
    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if float(get_time() - player.timer) > 0.05:
            if player.dir == 0:
                player.state_machine.handle_event(('IDLE_GO', 0))
            else:
                player.state_machine.handle_event(('RUN_GO', 0))
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(int(player.frame) * 176, 0, 176, 66, player.x, player.y - (181 - 76))
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 176, 0, 176, 66, 0, 'h', player.x, player.y - (181 - 76), 176, 66)
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
            player.image.clip_draw(int(player.frame) * 176, 0, 176, 66, player.x, player.y - (181 - 76))
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 176, 0, 176, 66, 0, 'h', player.x, player.y - (181 - 76), 176, 66)


class JumpAttack:
    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 4
        player.frame = 0
        player.attack = False
        player.image = load_image('Resource\Character\JumpAttack.png')
        player.dir = 0
    @staticmethod
    def exit(player, e):
            pass

    @staticmethod
    def do(player):
        if int(player.frame) < 1:
            player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4
            player.timer = get_time()
        if get_time() - player.timer > 1:
            player.state_machine.handle_event(('TIME_OUT', 0))

        if player.y < 90:
            player.jump = False
            player.state_machine.handle_event(('JUMP_END', 0))
        pass

    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 172, 0, 172, 158, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 172, 0, 172, 158, 0, 'h', player.x, player.y, 172, 158)

class JumpAttackRun:
    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 4
        player.frame = 0
        player.attack = False
        player.image = load_image('Resource\Character\JumpAttack.png')
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = -1, -1, 0

    @staticmethod
    def exit(player, e):
        pass
    @staticmethod
    def do(player):
        if int(player.frame) < 1:
            player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4
            player.timer = get_time()
        if get_time() - player.timer > 1:
            player.state_machine.handle_event(('TIME_OUT', 0))

        if player.y < 90:
            player.jump = False
            player.state_machine.handle_event(('JUMP_END', 0))
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        if player.x < 50 or player.x > 1870:
            player.x -= player.dir * RUN_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(player):
        if player.face_dir == 1:
            player.image.clip_draw(int(player.frame) * 172, 0, 172, 158, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 172, 0, 172, 158, 0, 'h', player.x, player.y, 172, 158)


class Skill1:
    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 4
        player.frame = 0
        player.attack = False
        player.timer = get_time()
        player.image = load_image('Resource\Character\Skill2.png')
        player.dir = 0

        player.vfx.setting(player.x + player.face_dir * 100, player.y, player.dmg * 1.3)
        game_world.add_object(player.vfx)
        game_world.add_collision_pair('attack:monster',player.vfx, None)
    @staticmethod
    def exit(player, e):
        game_world.remove_object(player.vfx)
        game_world.remove_collision_object(player.vfx)
        pass

    @staticmethod
    def do(player):
        if not int(player.frame > 3):
            player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 4
            if int(player.frame) == 0:
                player.x += player.face_dir * RUN_SPEED_PPS * game_framework.frame_time * 20
                if player.x < 50:
                    player.x = 50
                if player.x > 1870:
                    player.x = 1870

        if get_time() - player.timer > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))

        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(int(player.frame) * 183, 0, 183, 125, player.x, player.y - (181 - 150))
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 183, 0, 183, 125, 0, 'h', player.x, player.y - (181 - 150), 183, 125)

class Skill2:
    @staticmethod
    def enter(player, e):
        global FRAMES_PER_ACTION
        FRAMES_PER_ACTION = 6
        player.frame = 0
        player.attack = False
        player.image = load_image('Resource\Character\Skill3.png')


        player.vfx.setting(player.x + player.face_dir * 100, player.y, player.dmg * 1.2)
        game_world.add_object(player.vfx)
        game_world.add_collision_pair('attack:monster',player.vfx, None)
    @staticmethod
    def exit(player, e):
        player.dir = 0
        game_world.remove_object(player.vfx)
        game_world.remove_collision_object(player.vfx)
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * 0.5 / TIME_PER_ATTACK * game_framework.frame_time) % 6
        if player.frame > 5:
            if player.dir == 0:
                player.state_machine.handle_event(('IDLE_GO', 0))
            else:
                player.state_machine.handle_event(('RUN_GO', 0))
        pass

    @staticmethod
    def draw(player):
        if (player.face_dir == 1):
            player.image.clip_draw(int(player.frame) * 189, 0, 189, 198, player.x, player.y)
        if player.face_dir == -1:
            player.image.clip_composite_draw(int(player.frame) * 189, 0, 189, 198, 0, 'h', player.x, player.y , 189, 198)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, c_down: Jump, x_down: Attack1, a_down: Skill1, s_down: Skill2, hit: Hit},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, c_down: JumpRun, x_down: Attack1, a_down: Skill1, s_down: Skill2, hit: Hit},
            Jump: {right_down: JumpRun, left_down: JumpRun, right_up: JumpRun, left_up: JumpRun, jump_end: Idle, x_down: JumpAttack, hit: Hit},
            JumpRun: {right_down: Jump, left_down: Jump, right_up: Jump, left_up: Jump, jump_end: Run, x_down: JumpAttackRun, hit: Hit},
            Attack1: {idle_go: Idle, run_go: Run, next_attack: Attack2},
            Attack2: {idle_go: Idle, run_go: Run, next_attack: Attack3},
            Attack3: {idle_go: Idle, run_go: Run,},
            Hit: {idle_go: Idle, run_go: Run, dead: Dead},
            Dead: {},
            JumpAttack: {right_down: JumpAttackRun, left_down: JumpAttackRun, right_up: JumpAttackRun, left_up: JumpAttackRun, time_out: Jump, jump_end: Idle},
            JumpAttackRun: {right_down: JumpAttack, left_down: JumpAttack, right_up: JumpAttack, left_up: JumpAttack,time_out: JumpRun, jump_end: Run},
            Skill1: {time_out : Idle},
            Skill2: {idle_go: Idle, run_go: Run,}
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
        self.HPbar = load_image("Resource\HP\HPbar.png")
        self.HPbase = load_image("Resource\HP\HPbase.png")

        self.max_hp = 2000
        self.hp = 2000
        self.hp_per = 100
        self.dmg = 0.4
        self.x, self.y = 400, 100
        self.h = 90
        self.timer = 0
        self.frame = 0
        self.dir = 0
        self.face_dir = 1 # 오른쪽 방향
        self.jump = False
        self.jump_power = 0
        self.attack = False
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.vfx = Attack()

    def update(self):
        if self.hp < 0:
            game_framework.change_mode(over_mode)
        self.state_machine.update()

    def handle_event(self, e):
        if e.key == SDLK_x and (self.state_machine.cur_state == Attack1 or self.state_machine.cur_state == Attack2):
            self.state_machine.handle_event(('ATTACK', e))
            self.attack = True
        else:
            self.state_machine.handle_event(('INPUT', e))

    def draw(self):
        self.state_machine.draw()

        self.HPbase.draw(self.x, self.y + 100, 100, 8)
        self.HPbar.draw(self.x - (100 - self.hp_per) / 2, self.y + 100, self.hp_per, 8)

    def get_bb(self):
        return self.x - 60, self.y - 90, self.x + 60, self.y + 90

    def handle_collision(self, group, other):
        match group:
            case 'object:tile':
                self.y += 120
                self.jump = False
                self.state_machine.handle_event(('JUMP_END', 0))
            case 'player:monster':
                pass