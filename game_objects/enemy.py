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
        """Move the enemy towards the player."""
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        angle = atan2(dy, dx)  # Calculate angle
        self.rect.x += int(self.speed * cos(angle))  # Move towards x
        self.rect.y += int(self.speed * sin(angle))  # Move towards y

        # Ensure enemy doesn't go off-screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > player.screen_width:
            self.rect.right = player.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > player.screen_height:
            self.rect.bottom = player.screen_height

    def take_damage(self, amount):
        """Apply damage to the enemy and check for death."""
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        """Handle enemy death: generate item drop and remove enemy."""
        self.kill()  # Remove the enemy from the sprite group
        # Drop a random fruit at the enemy's position
        fruit = generate_random_fruit(self.rect.x, self.rect.y)
        self.drop_group.add(fruit)

    def deal_damage(self, player):
        """Deal damage to the player."""
        player.take_damage(self.damage)

    def render(self, screen):
        """Render the enemy on the screen."""
        screen.blit(self.image, self.rect.topleft)
