from pico2d import *

import game_world
from Player import Player
from Gravity import Gravity_World

# Game object class here
Width = 1920
Height = 1080

def handle_events():
    global running
    global player

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)



def create_world():
    global running
    global grass
    global team
    global player

    running = True

    player = Player()
    game_world.add_object(player, 1)



def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas(Width, Height)
create_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
