import pygame
from math import atan2, cos, sin
from game_objects.exp import generate_random_fruit

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, health, speed, damage, drop_group):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health
        self.speed = speed
        self.damage = damage
        self.drop_group = drop_group  # Accept drop_group as a parameter

    def move_toward_player(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        angle = atan2(dy, dx)
        self.rect.x += int(self.speed * cos(angle))
        self.rect.y += int(self.speed * sin(angle))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            fruit = generate_random_fruit(self.rect.x, self.rect.y)
            self.drop_group.add(fruit)

    def deal_damage(self, player):
        player.take_damage(self.damage)

    def render(self, screen):
        """Render the fruit to the screen."""
        screen.blit(self.image, self.rect.topleft)
