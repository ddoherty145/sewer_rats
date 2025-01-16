from random import randint, choice
# from game_objects.player import Player
from game_objects.weapons import TailWhip, Fangs, Cookbook
import pygame
pygame.init()

# Background
background_image_path = 'assets/temp_assets/firey_dungeon.png'
background = pygame.image.load(background_image_path)

image_width, image_height = background.get_size()
screen = pygame.display.set_mode([image_width, image_height])
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
fruit_sprites = pygame.sprite.Group()
lanes = [93, 218, 343]

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(GameObject, self).__init__()
        self.surf = pygame.image.load(image)
        self.rect = self.surf.get_rect(topleft=(x, y))

    def render(self, screen):
        screen.blit(self.surf, self.rect.topleft)

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__(93, 93, 'assets/temp_assets/player.png')
        self.dx = self.rect.x
        self.dy = self.rect.y
        self.pos_x = 1
        self.pos_y = 1
        self.weapon = None  # Default weapon is None

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

    def left(self):
        """Move the player left if within bounds."""
        if self.pos_x > 0:
            self.pos_x -= 1
            self.update_dx_dy()

    def right(self):
        """Move the player right if within bounds."""
        if self.pos_x < len(lanes) - 1:
            self.pos_x += 1
            self.update_dx_dy()

    def up(self):
        """Move the player up if within bounds."""
        if self.pos_y > 0:
            self.pos_y -= 1
            self.update_dx_dy()

    def down(self):
        """Move the player down if within bounds."""
        if self.pos_y < len(lanes) - 1:
            self.pos_y += 1
            self.update_dx_dy()

    def move(self):
        """Smoothly move the player toward its target position."""
        self.rect.x -= (self.rect.x - self.dx) * 0.25
        self.rect.y -= (self.rect.y - self.dy) * 0.25

    def update_dx_dy(self):
        """Update target coordinates based on the player's current lane position."""
        self.dx = lanes[self.pos_x]
        self.dy = lanes[self.pos_y]

    def reset(self):
        """Reset the player's position to the starting point."""
        self.rect.x, self.rect.y = 93, 93  # Reset to initial position
        self.dx, self.dy = self.rect.x, self.rect.y
        self.pos_x, self.pos_y = 1, 1
        print("Player position reset!")

class Fruit(GameObject):
    def reset_position(self):
        self.rect.x = choice(lanes)
        self.rect.y = -64

class Strawberry(Fruit):
    def __init__(self):
        super(Strawberry, self).__init__(0, 0, 'assets/temp_assets/strawberry.png')
        self.reset()

    def move(self):
        self.rect.y += 5
        if self.rect.y > image_height:
            self.reset()

    def reset(self):
        self.reset_position()

class Apple(Fruit):
    def __init__(self):
        super(Apple, self).__init__(0, 0, 'assets/temp_assets/apple.png')
        self.reset()

    def move(self):
        self.rect.y += 4
        if self.rect.y > image_height:
            self.reset()

    def reset(self):
        self.reset_position()


class Bomb(GameObject):
    def __init__(self):
        super(Bomb, self).__init__(0, 0, 'assets/temp_assets/bomb.png')
        self.reset()

    def move(self):
        self.rect.y += 3
        if self.rect.y > image_height:
            self.reset()

    def reset(self):
        self.rect.x = choice(lanes)
        self.rect.y = -64


player = Player()
strawberry = Strawberry()
apple = Apple()
bomb = Bomb()
xp = 0 
level = 1
xp_to_next_level = 10

all_sprites.add(player, apple, strawberry, bomb)
fruit_sprites.add(apple, strawberry)

score = 0
pygame.font.init()
font = pygame.font.SysFont(None, 32)

def display_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def display_xp_and_level():
    level_text = font.render(f"Level: {level}", True, (0,0,0))
    xp_text = font.render(f"XP: {xp}/{xp_to_next_level}", True, (0,0,0))
    screen.blit(level_text, (10, 70))
    screen.blit(xp_text, (10, 100))

def display_level_up_message():
    level_up_text = font.render("Level Up!", True, (255, 255, 0))
    screen.blit(level_up_text, (image_width// 2 - 50, image_height// 2 - 10))

lives = 3
heart_image = pygame.image.load('assets/temp_assets/player.png')

def display_lives():
    for i in range(lives):
        screen.blit(heart_image, (10 + i * 40, 40))

def level_up_menu():
    global selected_weapon
    menu_running = True
    weapons = [TailWhip(), Fangs(), Cookbook()]

    while menu_running:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 48)
        title = font.render("Choose Your Weapon!", True, (255, 255, 255))
        screen.blit(title, (image_width // 2 - title.get_width() // 2, 50))

        for i, weapon in enumerate(weapons):
            weapon_text = font.render(f"{i + 1}: {weapon.name}", True, (255, 255, 255))
            screen.blit(weapon_text, (50, 150 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    selected_weapon = weapons[event.key - pygame.K_1]
                    menu_running = False




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()

    screen.blit(background, (0, 0))

    for entity in all_sprites:
        entity.move()
        entity.render(screen)

    fruit = pygame.sprite.spritecollideany(player, fruit_sprites)
    if fruit:
        score += 1
        xp += 1 #add xp for collecting a fruit
        fruit.reset()

        #check for level up
        if xp >= xp_to_next_level:
            level += 1
            xp -= xp_to_next_level  # Carry over excess XP
            xp_to_next_level = int(xp_to_next_level * 1.5)  # Increase XP needed for next level

            display_level_up_message()
            pygame.display.flip()
            pygame.time.wait(1000)

            level_up_menu()

            if selected_weapon:
                player.equip_weapon(selected_weapon)  # Equip the selected weapon

    if pygame.sprite.collide_rect(player, bomb):
        lives -= 1
        if lives <= 0:
            running = False
        else:
            player.reset()

    display_score()
    display_lives()
    display_xp_and_level()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
