from pico2d import load_image

import Gravity


class StateMachine:
    def __init__(self, monster):
        self.player = monster
        self.cur_state = 0
        self.transitions = {
            #Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, c_down: Jump, x_down: Attack1, a_down: Skill1, s_down: Skill2},

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

animation_names = ['Walk']

class Monster:
    images = None
    def load_images(self):
        if Monster.images == None:
            Monster.images = {}
            for name in animation_names:

                Monster.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]
    def __init__(self, stage):
        self.x, self.y = 400, 100
        self.alive = True
        self.stage = stage
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
        self.state_machine.handle_event(('INPUT', e))

    def draw(self):
        self.state_machine.draw()
