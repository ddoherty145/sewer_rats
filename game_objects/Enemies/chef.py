import pygame
from game_objects.enemy import Enemy


class Chef(Enemy):
    def __init__(self, x, y, drop_group, screen_height):
        # Initialize the Enemy class with Chef-specific parameters
        super().__init__(
            x=x,
            y=y,
            image_path='/Users/froztydavie/Documents/sewer-rats/assets/Spritesheets/ChefSheet.png',
            health=50,  # Example health value for Chef
            speed=5,    # Example speed value for Chef
            damage=15,  # Example damage value for Chef
            drop_group=drop_group
        )
        self.screen_height = screen_height  # Specific attribute for Chef

    def move(self):
        """Chef's movement logic."""
        self.rect.y += self.speed  # Move the Chef downward

    def render(self, screen):
        """Render the Chef sprite to the screen."""
        screen.blit(self.image, self.rect.topleft)