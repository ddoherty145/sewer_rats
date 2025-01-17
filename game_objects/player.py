import pygame
from game_objects.game_objects import GameObject

class Player(GameObject):
    def __init__(self, screen_width, screen_height):
        super(Player, self).__init__(93, 93, '/Users/froztydavie/Documents/sewer-rats/assets/temp_assets/player.png')
        self.base_speed = 5  # Base movement speed
        self.speed = self.base_speed
        self.is_slowed = False
        self.slow_end_time = 0
        self.weapon = None  # Default weapon is None
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Health
        self.max_health = 100  # Starting health
        self.current_health = self.max_health

        # Experience Points
        self.xp = 0  # Add experience points attribute

        # Facing Direction
        self.facing_right = True

        # Player stats
        self.score = 0  # Initialize score attribute
        self.xp = 0  # Initialize xp attribute

    def equip_weapon(self, weapon):
        """Equip a weapon and notify the player."""
        self.weapon = weapon
        print(f"Equipped {self.weapon.name}")
    
    def attack(self):
        """Perform an attack if a weapon is equipped."""
        if self.weapon:
            print(f"Attacking with {self.weapon.name} (Damage: {self.weapon.damage})")
        else:
            print("No weapon equipped!")

    def attacks(self, enemy):
        """Check if player attacks the enemy and apply damage."""
        if self.weapon and pygame.sprite.collide_rect(self, enemy):  # Check if colliding with enemy
            print(f"Attacking {enemy.__class__.__name__} with {self.weapon.name}")
            enemy.take_damage(self.weapon.damage)  # Apply damage to the enemy
            return True
        return False

    def move(self, keys):
        """
        Move the player based on key inputs.
        :param keys: Dictionary of pressed keys.
        """
        if self.is_slowed and pygame.time.get_ticks() >= self.slow_end_time:
            self.recover_speed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.facing_right = False  # Player is facing left
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
            self.facing_right = True  # Player is facing right
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

    def reset(self):
        """Reset player to initial position and default speed."""
        self.rect.x = 93
        self.rect.y = 93
        self.speed = self.base_speed
        self.is_slowed = False
        self.current_health = self.max_health  # Reset health

    def apply_slow(self, slow_amount, duration):
        """Apply a slowing effect to the player."""
        if not self.is_slowed:  # Prevent stacking slow effects
            if slow_amount <= 0 or duration <= 0:
                print("Invalid slow effect parameters.")
                return
            self.speed *= slow_amount
            self.is_slowed = True
            self.slow_end_time = pygame.time.get_ticks() + duration

    def recover_speed(self):
        """Recover to base speed after slow effect ends."""
        self.speed = self.base_speed
        self.is_slowed = False

    def take_damage(self, amount):
        """Reduce health when the player takes damage."""
        self.current_health -= amount
        if self.current_health <= 0:
            self.die()

    def die(self):
        """Handle player death (e.g., reset health and position, or end the game)."""
        print("Player has died!")
        self.reset()  # Reset the player or you could end the game here

    def heal(self, amount):
        """Heal the player by a specified amount, ensuring health does not exceed max health."""
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        print(f"Player healed by {amount} points. Current health: {self.current_health}")

    def render(self, screen):
        """Render the player to the screen."""
        screen.blit(self.image, self.rect.topleft)
