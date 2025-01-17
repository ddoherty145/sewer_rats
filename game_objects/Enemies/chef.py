import pygame
from game_objects.enemy import Enemy


class Chef(pygame.sprite.Sprite):
    def __init__(self, x, y, drop_group):
        super().__init__()
        self.surf = pygame.Surface((50, 50))  # Example surface for the Chef
        self.surf.fill((0, 255, 0))  # Green color for the placeholder
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.drop_group = drop_group
        
        # Define the speed here, not in self.rect
        self.speed = 5  # Example speed value for movement

    def move(self):
        # Use self.speed here, not self.rect.speed
        self.rect.y += self.speed

    def render(self, screen):
        screen.blit(self.surf, self.rect.topleft)