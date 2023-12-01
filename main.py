from pico2d import open_canvas, delay, close_canvas
import game_framework

import menu_mode as start_mode
import play_mode

open_canvas(1920, 1080)
game_framework.run(start_mode)
close_canvas()

