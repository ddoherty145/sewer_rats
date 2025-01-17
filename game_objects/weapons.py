import pygame

class Weapon:
    def __init__(self, name, image_path, damage):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.damage = damage

    def attack(self, player, enemy):
        """
        Check for a collision between the player and an enemy, and apply damage.
        :param player: The player who is attacking.
        :param enemy: The enemy being attacked.
        """
        if player.rect.colliderect(enemy.rect):  # Check if player and enemy are in contact
            enemy.take_damage(self.damage)  # Apply weapon damage to the enemy
            print(f"{self.name} hit {enemy} for {self.damage} damage!")
            return True
        return False


class TailWhip(Weapon):
    def __init__(self):
        super().__init__("Tail Whip", "assets/temp_assets/red_knife.png", damage=10)


class Fangs(Weapon):
    def __init__(self):
        super().__init__("Fangs", "assets/temp_assets/spear.png", damage=20)


class Cookbook(Weapon):
    def __init__(self):
        super().__init__("Remey's Cookbook", "assets/temp_assets/staff.png", damage=50)
