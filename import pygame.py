import pygame
import random
import time
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    KEYDOWN,
    K_ESCAPE,
    QUIT,
    K_h,
    MOUSEBUTTONDOWN
)

class WhiteBloodCell:
    def __init__(self):
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.position = [0, 0]
        self.health = 100

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.position[0] -= 25
        if pressed_keys[K_RIGHT]:
            self.position[0] += 25
        if pressed_keys[K_UP]:
            self.position[1] -= 25
        if pressed_keys[K_DOWN]:
            self.position[1] += 25
        
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[1] <= 0:
            self.position[1] = 0
        if self.position[0] > SCREEN_WIDTH:
            self.position[0] = SCREEN_WIDTH
        if self.position[1] > (SCREEN_HEIGHT - 25):
            self.position[1] = SCREEN_HEIGHT - 25

    def remove_health(self, change):
        self.health -= change

class Virus:
    def __init__(self):
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect()
        self.position = self.new_position()
    
    def new_position(self):
        return [SCREEN_WIDTH - 25, int(random.randint(0, (SCREEN_HEIGHT - 25)/25)*25)]

    def update(self, player):
        if player.position == self.position:
            self.position = self.new_position()
        if self.position[0] < 0:
            self.position = self.new_position()
            player.remove_health(5)
        else:
            self.position[0] -= 25
        if player.position == self.position:
            self.position = self.new_position()
            
class RedBloodCell:
    def __init__(self):
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.position = self.new_position()
    
    def new_position(self):
        return [SCREEN_WIDTH - 25, int(random.randint(0, (SCREEN_HEIGHT - 25)/25)*25)]

    def update(self, player):
        if player.position == self.position:
            self.position = self.new_position()
            player.remove_health(5)
        if self.position[0] < 0:
            self.position = self.new_position()
        else:
            self.position[0] -= 25
        if player.position == self.position:
            self.position = self.new_position()
            player.remove_health(5)

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
entity_count = 1
runngin = True
font = pygame.font.SysFont("Comic Sans MS", 30)
title = font.render("Lifeline", False, (255, 255, 255))
titlerect = title.get_rect()
titlerect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
screen.fill((0, 0, 0))
screen.blit(title, titlerect)
pygame.display.flip()
while runngin:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
            if event.key == K_h:
                runngin = False
                entity_count = 5
        if event.type == QUIT:
            quit()
        if event.type == MOUSEBUTTONDOWN:
            runngin = False

runngin = True
player = WhiteBloodCell()
viruses = [Virus() for n in range(entity_count)]
for i in range(entity_count):
    viruses[i].position[0] -= (i * 50)
red_blood_cells = [RedBloodCell() for n in range(entity_count)]
for i in range(entity_count):
    red_blood_cells[i].position[0] -= (i * 50)
clock = pygame.time.Clock()
timer = time.time()

while runngin:
    screen.fill((255, 92, 103))
    clock.tick(5)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    for virus in viruses:
        virus.update(player)
        screen.blit(virus.surf, tuple(virus.position))
    for red_blood_cell in red_blood_cells:
        red_blood_cell.update(player)
        screen.blit(red_blood_cell.surf, tuple(red_blood_cell.position))
    screen.blit(player.surf, tuple(player.position))
    screen.blit(font.render("Health: " + str(player.health), False, (0, 0, 0)), (0, 0))
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
        if event.type == QUIT:
            quit()
    pygame.display.flip()
    if player.health == 0:
        runngin = False

runngin = True

gameover = font.render("Game Over", False, (255, 255, 255))
gameoverrect = gameover.get_rect()
gameoverrect.center = (((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2))
seconds = font.render("Time Survived: " + str(round(time.time() - timer, 3)) + " s", False, (255, 255, 255))
secondsrect = seconds.get_rect()
secondsrect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT + 55) // 2)
screen.fill((0, 0, 0))
screen.blit(gameover, gameoverrect)
screen.blit(seconds, secondsrect)
pygame.display.flip()

while runngin:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()
        if event.type == QUIT:
            quit()  