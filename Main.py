from pico2d import *
from Player import Player

# Game object class here
Width = 1920
Height = 1080

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)



def reset_world():
    global running
    global grass
    global team
    global world
    global player

    running = True
    world = []

    # grass = Grass()
    # world.append(grass)

    player = Player()
    world.append(player)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas(Width, Height)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()