import pygame
import time

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, damage):
        super().__init__()
        self.image = pygame.Surface((10,5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x,y))
        self.direction = direction
        self.speed = speed
        self.damage = damage

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width():
            self.kill()

class Weapon:
    def __init__(self, name, image_path, damage, cooldown):
        self.name = name
        self.image = pygame.image.load(image_path)
        self.damage = damage
        self.cooldown = cooldown
        self.last_attack_time = 0
        self.projectiles = pygame.sprite.Group()

    def attack(self, player):
        """
        :param player: The player using the weapon.
        """
        current_time = time.time()
        if current_time - self.last_attack_time >= self.cooldown:
            self.last_attack_time = current_time
            direction = 1 if player.facing_right else -1
            projectile = Projectile(
                x=player.rect.centerx,
                y=player.rect.centery,
                direction=direction,
                speed=10,
                damage=self.damage
            )
            self.projectiles.add(projectile)

    def update_projectiles(self, screen, enemy_group):
        """
        Update and draw all projectiles and handle collisions with enemies.
        :param screen: The game screen.
        :param enemy_group: The group of enemies to check for collisions.
        """
        self.projectiles.update()
        for projectile in self.projectiles:
            screen.blit(projectile.image, projectile.rect.topleft)
            hits = pygame.sprite.spritecollide(projectile, enemy_group, False)
            for enemy in hits:
                enemy.take_damage(projectile.damage)
                projectile.kill() #remove projectile when it hits an enemy 
        


class TailWhip(Weapon):
    def __init__(self):
        super().__init__("Tail Whip", "/Users/froztydavie/Documents/sewer-rats/assets/temp_assets/red_knife.png", damage=10, cooldown=0.5)


class Fangs(Weapon):
    def __init__(self):
        super().__init__("Fangs", "/Users/froztydavie/Documents/sewer-rats/assets/temp_assets/spear.png", damage=20, cooldown=0.8)


class Cookbook(Weapon):
    def __init__(self):
        super().__init__("Remey's Cookbook", "/Users/froztydavie/Documents/sewer-rats/assets/temp_assets/staff.png", damage=50, cooldown=1.5)
