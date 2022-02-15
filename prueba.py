#!/usr/bin/python3

import pygame
import os

pygame.init()

BLACK = (0, 0, 0)
WIDTH, HEIGHT = 400, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_BIG = pygame.image.load(os.path.join('Assets', 'wallpaper.jpg'))
BACKGROUND_MAIN = pygame.transform.scale(BACKGROUND_BIG, (WIDTH, HEIGHT))

run = True
y_position = 0

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    WINDOW.fill(BLACK)
    WINDOW.blit(BACKGROUND_MAIN, [0, y_position])
    WINDOW.blit(BACKGROUND_MAIN, [0, -HEIGHT + y_position])

    if y_position == HEIGHT:
        y_position = 0
    y_position += 1

    pygame.display.update()
