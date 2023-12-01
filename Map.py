from pico2d import load_image, draw_rectangle


class BackGround:
    def __init__(self):
        self.image = load_image('Resource\Map\Map1\MAP1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1920 // 2, 1080 // 2)


class Tile:
    def __init__(self, x, y):
        self.image = load_image('Resource\Map\Map1\Tile1.png')
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        return self.x - 40, self.y - 90, self.x + 40, self.y + 20

    def handle_collision(self, group, other):
        match group:
            case 'object:tile':
                pass