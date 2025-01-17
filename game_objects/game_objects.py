import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.width = width
        self.rect.height = height
