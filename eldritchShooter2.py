# Imports
import pygame
import math
import random

# Load Images
player0 = pygame.image.load("assets/images/player_rotate_testsprite0.png")
player270 = pygame.image.load("assets/images/player_rotate_testsprite90.png")
player180 = pygame.image.load("assets/images/player_rotate_testsprite180.png")
player90 = pygame.image.load("assets/images/player_rotate_testsprite270.png")

test_bull = pygame.image.load("assets/images/test_bullet.png")

enemy_testsprite = pygame.image.load("assets/images/enemy_testsprite.png")

# Initialize game engine
pygame.init()

# Window
SIZE = (800, 600)
TITLE = "My Awesome Picture"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 125, 0)

# Game Classes

## Enemies

class BasicEnemy(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 3
        self.firecooldown = 0

    def get_vector(self):
        player_pos = (shuttle.rect.x+25, shuttle.rect.y+25)

        # Get Hypotenus

        xdirr = self.rect.centerx - player_pos[0]
        ydirr = self.rect.centery - player_pos[1]

        hyp = math.sqrt(xdirr ** 2 + ydirr ** 2)

        try:
            xvector = (xdirr / hyp) * 2
            yvector = (ydirr / hyp) * 2

            return [xvector, yvector]

        except ZeroDivisionError:
            return [0, 0]




    def update(self):
        # Find the player and determine direction to travel in

        # Move instances
        self.rect.x -= self.get_vector()[0]
        self.rect.y -= self.get_vector()[1]

        # Will be killed if instances of playerbullets collide with instances
        hit_list = pygame.sprite.spritecollide(self, playerbullets, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.kill()

class DriftingEnemy(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 3
        self.firecooldown = 0

        self.velocityx = 0
        self.velocityy = 0

    def get_vector(self):
        player_pos = (shuttle.rect.x, shuttle.rect.y)

        # Get Hypotenus

        xdirr = self.rect.centerx - player_pos[0]
        ydirr = self.rect.centery - player_pos[1]

        hyp = math.sqrt(xdirr ** 2 + ydirr ** 2)

        xvector = (xdirr / hyp) * .3
        yvector = (ydirr / hyp) * .3

        return [xvector, yvector]

    def update(self):
        # Find the player and determine direction to travel in
        self.velocityx -= self.get_vector()[0]
        self.velocityy -= self.get_vector()[1]

        # Move instances
        self.rect.x += self.velocityx

        self.rect.y += self.velocityy

        # Will be killed if instances of playerbullets collide with instances
        hit_list = pygame.sprite.spritecollide(self, playerbullets, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.kill()
## Bullet Classes

class PlayerBullet(pygame.sprite.Sprite):

    def __init__(self, x, y, velocityx, velocityy, duration=True):
        super().__init__()

        self.image = test_bull

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocityx = velocityx
        self.velocityy = velocityy

        self.duration = duration


    def update(self):
        ### Move Bullet

        self.rect.x += self.velocityx
        self.rect.y += self.velocityy

        ### Kill instance at screen edge
        if self.rect.right > SIZE[0] or self.rect.left < 0:
            self.kill()

        if self.rect.bottom > SIZE[1] or self.rect.top < 0:
            self.kill()

## Main Player Class

class Shuttle(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 3
        self.firecooldown = 0

        self.velocityx = 0
        self.velocityy = 0

    def get_angle(self):
        mouse_pos = pygame.mouse.get_pos()
        vectorx = mouse_pos[0] - self.rect.x
        vectory = self.rect.y - mouse_pos[1]

        return ((math.atan2(vectory, vectorx)) * (180/math.pi))

    def get_vector(self):
        mouse_pos = pygame.mouse.get_pos()

        # Get Hypotenus

        xdirr = self.rect.centerx - mouse_pos[0]
        ydirr = self.rect.centery - mouse_pos[1]

        hyp = math.sqrt(xdirr ** 2 + ydirr ** 2)

        xvector = (xdirr / hyp) * 10
        yvector = (ydirr / hyp) * 10

        return [xvector, yvector]

    def fire(self):
        vector = self.get_vector()

        if 135 > self.get_angle() > 45:
            bullet = PlayerBullet(self.rect.centerx - 10, self.rect.top, -vector[0], -vector[1])
        elif 180 > self.get_angle() > 135 or -180 < self.get_angle() < -135:
            bullet = PlayerBullet(self.rect.left, self.rect.centery - 10, -vector[0], -vector[1])
        elif -135 < self.get_angle() < -45:
            bullet = PlayerBullet(self.rect.centerx - 10, self.rect.bottom, -vector[0], -vector[1])
        elif 45 > self.get_angle() > -45:
            bullet = PlayerBullet(self.rect.right, self.rect.centery - 10, -vector[0], -vector[1])
        else:
            bullet = PlayerBullet(self.rect.centerx, self.rect.centery - 10, -vector[0], -vector[1])

        #bullet = PlayerBullet(self.rect.centerx, self.rect.centery, -vector[0], -vector[1])

        playerbullets.add(bullet)
        self.firecooldown = 15

    def set_image(self):
        if 135 > self.get_angle() > 45:
            self.image = player0
        elif 180 > self.get_angle() > 135 or -180 < self.get_angle() < -135:
            self.image = player90
        elif -135 < self.get_angle() < -45:
            self.image = player180
        elif 45 > self.get_angle() > -45:
            self.image = player270

    def update(self):
        ### Move Shuttle

        self.rect.x += self.velocityx
        self.rect.y += self.velocityy

        ## Reduce fire cooldown
        if self.firecooldown > 0:
            self.firecooldown -= 1

        ### Keep within screen boundries
        if self.rect.right > SIZE[0] or self.rect.left < 0:
            self.rect.x -= self.velocityx

        if self.rect.bottom > SIZE[1] or self.rect.top < 0:
            self.rect.y -= self.velocityy

        ### Set it's image based on previous events
        self.set_image()

# Functions

## Helper Functions

def status():
    print(str(shuttle.velocityx) + " " + str(shuttle.velocityy))

## Core Functions

def setup():
    global shuttle, player, enemies, playerbullets

    # Creates and adds a instance of Shuttle

    shuttle = Shuttle(400, 300, player0)

    player = pygame.sprite.GroupSingle()
    player.add(shuttle)

    # Create Enemies and adds them to a sprite group

    enemylist = [
        BasicEnemy(100, 100, enemy_testsprite),
        DriftingEnemy(200, 200, enemy_testsprite),
        BasicEnemy(300, 300, enemy_testsprite)
    ]
    enemies = pygame.sprite.Group()

    for enemy in enemylist:
        enemies.add(enemy)


    # Stores instances of PlayerBullet
    playerbullets = pygame.sprite.Group()

# Game loop
done = False

setup()
while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True



    # Game logic (Check for collisions, update points, etc.)

    ## Player fires

    leftmouse_click = (1, 0, 0)

    if pygame.mouse.get_pressed() == leftmouse_click and shuttle.firecooldown == 0:
        shuttle.fire()

    ## Player controls the ship here
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a] and shuttle.velocityx >= -6:
        shuttle.velocityx -= 2
    elif pressed[pygame.K_d] and shuttle.velocityx <= 6:
        shuttle.velocityx += 2
    else:

        if shuttle.velocityx > 0:
            shuttle.velocityx -= 2
        elif shuttle.velocityx < 0:
            shuttle.velocityx += 2


    if pressed[pygame.K_w] and shuttle.velocityy >= -6:
        shuttle.velocityy -= 2
    elif pressed[pygame.K_s] and shuttle.velocityy <= 6:
        shuttle.velocityy += 2
    else:

        if shuttle.velocityy > 0:
            shuttle.velocityy -= 2
        elif shuttle.velocityy < 0:
            shuttle.velocityy += 2

    ## All game objects are updated here
    shuttle.update()
    playerbullets.update()
    enemies.update()

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(WHITE)
    player.draw(screen)
    playerbullets.draw(screen)
    enemies.draw(screen)


    # Update screen (Actually drasaw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()