import pygame
from game_objects.enemy import Enemy

import pygame

class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y, drop_group, screen_height):
        super().__init__()
        self.surf = pygame.image.load('/Users/froztydavie/Documents/sewer-rats/assets/temp_assets/WhiteCatIdle.png').convert_alpha()  # Load the image
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf = pygame.Surface((50, 50))
        self.drop_group = drop_group
        self.screen_height = screen_height

    def render(self, screen):
        screen.blit(self.surf, self.rect.topleft)

