from pico2d import load_image, draw_rectangle, load_font


class BackGround:
    def __init__(self):
        self.image = load_image('Resource\Map\Map1\MAP1.png')
        self.font = load_font('ENCR10B.TTF', 24)
        self.score = 0

    def update(self):
        pass

    def draw(self):
        self.image.draw(1920 // 2, 1080 // 2)
        self.font.draw(1920 // 2, 1000, f'{self.score}', (0, 0, 255))


class Tile:
    def __init__(self, x, y):
        self.image = load_image('Resource\Map\Map1\Tile1.png')
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)


    def get_bb(self):
        return self.x - 40, self.y - 90, self.x + 40, self.y + 20

    def handle_collision(self, group, other):
        match group:
            case 'object:tile':
                pass