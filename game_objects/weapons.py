
import pygame

class Weapon:
    def __init__(self, name, image_path, damage):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.damage = damage

class TailWhip(Weapon):
    def __init__(self):
        super().__init__("Tail Whip", "assets/temp_assets/red_knife.png", damage=10)

class Fangs(Weapon):
    def __init__(self):
        super().__init__("Fangs", "assets/temp_assets/spear.png", damage=20)

class Cookbook(Weapon):
    def __init__(self):
        super().__init__("Remey's Cookbook", "assets/temp_assets/staff.png", damage=50)
