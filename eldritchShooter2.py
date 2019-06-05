# Imports
import pygame
import math
import random

# Load Images
player0 = pygame.image.load("assets/images/player_rotate_testsprite0.png")
player270 = pygame.image.load("assets/images/player_rotate_testsprite90.png")
player180 = pygame.image.load("assets/images/player_rotate_testsprite180.png")
player90 = pygame.image.load("assets/images/player_rotate_testsprite270.png")

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

## Main Player Class

class Shuttle(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.health = 3

        self.velocityx = 0
        self.velocityy = 0

    def get_angle(self):
        mouse_pos = pygame.mouse.get_pos()
        vectorx = mouse_pos[0] - self.rect.x
        vectory = self.rect.y - mouse_pos[1]

        return ((math.atan2(vectory, vectorx)) * (180/math.pi))

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

        ### Set it's image based on previous events
        self.set_image()

        ### Keep within screen boundries
        if self.rect.right > SIZE[0] or self.rect.left < 0:
            self.rect.x -= self.velocityx

        if self.rect.bottom > SIZE[1] or self.rect.top < 0:
            self.rect.y -= self.velocityy

# Functions

## Helper Functions

def status():
    print(str(shuttle.velocityx) + " " + str(shuttle.velocityy))

## Core Functions

def setup():
    global shuttle, player

    shuttle = Shuttle(400, 300, player0)

    player = pygame.sprite.GroupSingle()
    player.add(shuttle)

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

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(WHITE)
    player.draw(screen)

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()