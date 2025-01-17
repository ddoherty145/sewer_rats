import pygame
from random import choice

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.surf = pygame.image.load(image)
        self.rect = self.surf.get_rect(topleft=(x, y))

    def reset_position(self):
        """Reset fruit to a random position."""
        self.rect.x = choice(range(50, 750))  # Adjust to your screen width
        self.rect.y = -64  # Start off-screen, just above the visible screen

    def move(self):
        """Move the fruit down the screen."""
        self.rect.y += 4  # Adjust speed as needed

    def render(self, screen):
        """Render the fruit to the screen."""
        screen.blit(self.surf, self.rect.topleft)


class Strawberry(Fruit):
    def __init__(self, x, y):
        super().__init__(x, y, '/Users/froztydavie/Documents/sewer-rats/assets/FreePixelFood/Assets/FreePixelFood/Sprite/Food/Cheese.png')

    def apply_effect(self, player):
        """Define the effect of collecting the strawberry."""
        player.score += 5  # Example: Add to the player's score
        player.xp += 5
        player.heal(1)  # Heal the player by 1 health point

class Apple(Fruit):
    def __init__(self, x, y):
        super().__init__(x, y, '/Users/froztydavie/Documents/sewer-rats/assets/Ghostpixxells_pixelfood/81_pizza.png')

    def apply_effect(self, player):
        """Define the effect of collecting the apple."""
        player.heal(1)  # Heal the player by 1 health point
        player.xp += 1
        player.score += 10





# Factory method to generate random fruits
def generate_random_fruit(x, y):
    return choice([Strawberry(x, y), Apple(x, y)])
