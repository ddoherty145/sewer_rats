import pygame
from game_objects.enemy import Enemy

import pygame

class Cat(Enemy):
    def __init__(self, x, y, drop_group, screen_height):
        # Initialize the Enemy class with Cat-specific parameters
        super().__init__(
            x=x,
            y=y,
            image_path='/Users/froztydavie/Documents/sewer-rats/assets/temp_assets/WhiteCatIdle.png',
            health=30,  # Example health value for a Cat
            speed=2,    # Example speed value for a Cat
            damage=10,  # Example damage value for a Cat
            drop_group=drop_group
        )
        self.screen_height = screen_height  # Specific attribute for Cat

    def render(self, screen):
        """Render the Cat sprite to the screen."""
        screen.blit(self.image, self.rect.topleft)

