import pygame
from random import randint
from game_objects.player import Player
from game_objects.enemy import Enemy
from game_objects.Enemies.chef import Chef
from game_objects.Enemies.cat import Cat
from game_objects.weapons import TailWhip, Fangs, Cookbook
from game_objects.exp import generate_random_fruit, Strawberry, Apple

pygame.init()


# Constants
background_image_path = '/Users/froztydavie/Documents/sewer-rats/images/kitchen_floor.png'
background = pygame.image.load(background_image_path)
image_width, image_height = background.get_size()
screen = pygame.display.set_mode([image_width, image_height])
clock = pygame.time.Clock()

# Groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
fruit_sprites = pygame.sprite.Group()
drop_group = pygame.sprite.Group()

# Initialize Objects
player = Player(screen_width=image_width, screen_height=image_height)

# Enemy Initialization
cat = Cat(randint(0, image_width - 50), -100, drop_group, screen_height=image_height)
chef = Chef(randint(0, image_width - 50), -150, drop_group, screen_height=image_height)

# Items
strawberry = Strawberry(x=randint(0, image_width - 50), y=randint(-image_height, 0))
apple = Apple(x=randint(0, image_width - 50), y=randint(-image_height, 0))

# Starting Weapon
tail_whip = TailWhip()
player.equip_weapon(tail_whip)

# Game State
score = 0
xp = 0
level = 1
xp_to_next_level = 10
lives = 3
selected_weapon = None

# UI Elements
pygame.font.init()
font = pygame.font.SysFont(None, 32)
large_font = pygame.font.SysFont(None, 48)

# Add to groups
all_sprites.add(player, apple, strawberry, cat, chef)
fruit_sprites.add(apple, strawberry)
enemy_sprites.add(cat, chef)

# Functions
def display_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def display_xp_and_level():
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    xp_text = font.render(f"XP: {xp}/{xp_to_next_level}", True, (0, 0, 0))
    screen.blit(level_text, (10, 50))
    screen.blit(xp_text, (10, 80))

def display_level_up_message():
    level_up_text = large_font.render("Level Up!", True, (255, 255, 0))
    screen.blit(level_up_text, (image_width // 2 - 100, image_height // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(1000)

def respawn_enemy(enemy, screen_width, screen_height):
    """Respawn an enemy if it's off-screen or dead."""
    if enemy.rect.bottom <= 0 or enemy.health <= 0:  # Enemy is off-screen or dead
        # Ensure a valid random spawn position
        if screen_width > enemy.rect.width:  # Only try to spawn if the screen is wide enough
            spawn_x = randint(0, screen_width - enemy.rect.width)
        else:
            spawn_x = 0  # If screen is smaller than the enemy, spawn at the left edge
        
        enemy.rect.x = spawn_x
        enemy.rect.y = -50  # Spawn just above the screen
        enemy.health = 100  # Reset enemy health
        enemy_sprites.add(enemy)  # Re-add to the enemy group


def level_up_menu():
    global selected_weapon
    menu_running = True
    weapons = [TailWhip(), Fangs(), Cookbook()]

    while menu_running:
        screen.fill((0, 0, 0))
        title = large_font.render("Choose Your Weapon!", True, (255, 255, 255))
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
background_y = 0
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background Scrolling
    background_y = (background_y + player.speed // 2) % image_height
    screen.blit(background, (0, background_y - image_height))
    screen.blit(background, (0, background_y))

    # Player Movement
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Player Auto-Attack
    player.attack()

    # Collision Handling
    fruit = pygame.sprite.spritecollideany(player, fruit_sprites)
    if fruit:
        score += 1
        xp += 1
        fruit.reset_position()

        if xp >= xp_to_next_level:
            level += 1
            xp -= xp_to_next_level
            xp_to_next_level = int(xp_to_next_level * 1.5)
            display_level_up_message()
            level_up_menu()
            if selected_weapon:
                player.equip_weapon(selected_weapon)

    # Enemy Collision
    for enemy in enemy_sprites:
        if player.attacks(enemy):  # Call player's attack method
            if player.weapon:
                player.weapon.attack(player)
                enemy.take_damage(player.weapon.damage)
                player.weapon.update_projectiles(screen, enemy_sprites)
        
        # Respawn enemy if it's off-screen or dead
        respawn_enemy(enemy, image_width, image_height)

    # Player and Cat Collision
    if pygame.sprite.collide_rect(player, cat):
        lives -= 1
        if lives <= 0:
            running = False
        else:
            player.reset()

    # Handle Items Dropped from Enemies
    for item in drop_group:
        item.move()
        screen.blit(item.surf, item.rect.topleft)

    collected_item = pygame.sprite.spritecollideany(player, drop_group)
    if collected_item:
        collected_item.apply_effect(player)
        collected_item.kill()

    # Check Lives
    if lives <= 0:
        game_over_font = large_font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_font, (image_width // 2 - game_over_font.get_width() // 2, image_height // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(2000)
        break


    # Update and Render Entities
    for entity in all_sprites:
        if isinstance(entity, Player):
            entity.move(keys)
        elif hasattr(entity, 'move'):
            entity.move()
        entity.render(screen)

    # Display UI
    display_score()
    display_xp_and_level()

    # Update Screen
    player.render(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
