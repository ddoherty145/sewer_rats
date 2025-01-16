from game import GameObject

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__(93, 93, 'assets/temp_assets/player.png')
        self.dx = self.rect.x
        self.dy = self.rect.y
        self.pos_x = 1
        self.pos_y = 1

    def left(self):
        if self.pos_x > 0:
            self.pos_x -= 1
            self.update_dx_dy()

    def right(self):
        if self.pos_x < len(lanes) - 1:
            self.pos_x += 1
            self.update_dx_dy()

    def up(self):
        if self.pos_y > 0:
            self.pos_y -= 1
            self.update_dx_dy()

    def down(self):
        if self.pos_y < len(lanes) - 1:
            self.pos_y += 1
            self.update_dx_dy()

    def move(self):
        self.rect.x -= (self.rect.x - self.dx) * 0.25
        self.rect.y -= (self.rect.y - self.dy) * 0.25

    def update_dx_dy(self):
        self.dx = lanes[self.pos_x]
        self.dy = lanes[self.pos_y]