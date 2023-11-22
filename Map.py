from pico2d import load_image

class Ground:
    def __init__(self):
        self.image = load_image('Resource\2.배경\background43.png')
        self.imgx = 250
        self.imgy = 500

    def update(self):
        pass

    def draw(self):
        self.image.draw(1280 // 2, 1024 // 2)

