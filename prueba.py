#!/usr/bin/python3

import pygame
import os
import random
import time

from classes import moving_background
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 400, 600
ENEMY_SIZE = (80, 80)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_BIG = pygame.image.load(os.path.join('Assets', 'wallpaper.jpg'))
BACKGROUND_MAIN = pygame.transform.scale(BACKGROUND_BIG, (WIDTH, HEIGHT))

ENEMY_1 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level1.png')), 180)

ENEMY_2 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level2.png')), 180)

ENEMY_3 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level3.png')), 180)

ayuda = moving_background()


class enemies:
    def __init__(self):
        self.enemy_ship_1 = pygame.transform.scale(ENEMY_1, (ENEMY_SIZE))
        self.enemy_ship_2 = pygame.transform.scale(ENEMY_2, (ENEMY_SIZE))
        self.enemy_ship_3 = pygame.transform.scale(ENEMY_3, (ENEMY_SIZE))
        self.x_position = random.randint(0, WIDTH - 100)
        self.y_position = 0
        self.change_x = 0.1
        self.change_y = 0.1

    def show(self):
        WINDOW.blit(self.enemy_ship_1, (self.x_position, self.y_position))

    def x_movement(self):
        self.x_position += self.change_x
        self.y_position += self.change_y

        # Evitar que el enemigo salga de la pantalla
        if self.x_position <= 0:
            self.change_x += 0.1
        elif self.x_position > WIDTH - 100:
            self.change_x -= 0.1

        if self.y_position <= 0:
            self.change_y += 0.0001


ru = True
enemy = enemies()
while ru:
    WINDOW.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ru = False

    ayuda.window_update()
    ayuda.move_background()
    enemy.show()
    enemy.x_movement()
    pygame.display.update()
