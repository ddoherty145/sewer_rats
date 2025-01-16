from game import GameObject

class Weapon(GameObject):
    def __init__(self, x, y, image, speed=10):
        super().__init__(x, y, image)
        self.speed = speed

    def move(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()