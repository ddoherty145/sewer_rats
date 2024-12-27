from random import randint, choice
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

    def left(self):
        if self.pos_x > 0:
            self.pos_x -= 1
            self.update_dx_dy()

    def right(self):
        if self.pos_x < len(lanes) - 1:
            self.pos_x += 1
            self.update_dx_dy()

    def up(self):
        if self.pos_y > 0:
            self.pos_y -= 1
            self.update_dx_dy()

    def down(self):
        if self.pos_y < len(lanes) - 1:
            self.pos_y += 1
            self.update_dx_dy()

    def move(self):
        self.rect.x -= (self.rect.x - self.dx) * 0.25
        self.rect.y -= (self.rect.y - self.dy) * 0.25

    def update_dx_dy(self):
        self.dx = lanes[self.pos_x]
        self.dy = lanes[self.pos_y]

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

all_sprites.add(player, apple, strawberry, bomb)
fruit_sprites.add(apple, strawberry)

score = 0
pygame.font.init()
font = pygame.font.SysFont(None, 32)

def display_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

lives = 3
heart_image = pygame.image.load('assets/temp_assets/player.png')

def display_lives():
    for i in range(lives):
        screen.blit(heart_image, (10 + i * 40, 40))

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
        fruit.reset()

    if pygame.sprite.collide_rect(player, bomb):
        lives -= 1
        if lives <= 0:
            running = False
        else:
            player.reset()

    display_score()
    display_lives()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
