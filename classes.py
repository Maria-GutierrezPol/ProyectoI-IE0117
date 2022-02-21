#!/usr/bin/python3

import pygame
import random
import os

# CONSTANTES ------------------------------------------------------------------
PLAYER_SIZE = (80, 80)
ENEMY_SIZE = (80, 80)
WIDTH, HEIGHT = 400, 600
BULLET_SIZE = (32, 32)

# IMAGENES --------------------------------------------------------------------

BACKGROUND_BIG = pygame.image.load(os.path.join('Assets', 'wallpaper.jpg'))
BACKGROUND_MAIN = pygame.transform.scale(BACKGROUND_BIG, (WIDTH, HEIGHT))
PLAYER = pygame.image.load(os.path.join('Assets', 'player.png'))

ENEMY_1 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level1.png')), 180)

ENEMY_2 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level2.png')), 180)

ENEMY_3 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level3.png')), 180)

BULLET = pygame.image.load(os.path.join('Assets', 'enemy_bullet.png'))

# DISPLAY ---------------------------------------------------------------------

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# CLASES ----------------------------------------------------------------------


# Clase boton, cuya implementacion se incluye en el menu principal y en los
# sub menues.
class Button:
    def __init__(self, image, position, text_in, font, base_color, sec_color):
        self.image = image
        self.x = position[0]
        self.y = position[1]
        self.font = font
        self.base_color = base_color
        self.sec_color = sec_color
        self.text_in = text_in
        self.text = self.font.render(self.text_in, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    # Funcion para actualizar la pantalla principal
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # Funcion para revisar si el usuario dio algun input
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right):
            if position[1] in range(self.rect.top, self.rect.bottom):
                return True
        return False

    # Funcion para determinar si el usuario se encunetra posicionado sobre
    # algun boton del menu, de ser asi cambia su color.
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right):
            if position[1] in range(self.rect.top, self.rect.bottom):
                self.text = self.font.render(
                            self.text_in, True, self.sec_color)
        else:
            self.text = self.font.render(
                        self.text_in, True, self.base_color)

# Clase pare el movimiento del fondo junto con las naves.
class moving_background:
    def __init__(self):
        self.background = BACKGROUND_MAIN
        self.rect = self.background.get_rect()
        self.x_position = 0
        self.y1_position = 0
        self.y2_position = self.rect.height
        self.speed = 0.1

    def window_update(self):
        self.y1_position -= self.speed
        self.y2_position -= self.speed

        if self.y1_position <= -self.rect.height:
            self.y1_position = self.rect.height

        if self.y2_position <= -self.rect.height:
            self.y2_position = self.rect.height

    def move_background(self):
        WINDOW.blit(self.background, (self.x_position, self.y1_position))
        WINDOW.blit(self.background, (self.x_position, self.y2_position))


# Clase para el jugador.
class player:
    def __init__(self):
        self.player = pygame.transform.scale(PLAYER, (PLAYER_SIZE))
        self.x_position = 200 - 40
        self.y_position = 600 - 80
        self.xb_position = 0
        self.yb_position = 600 - 80
        self.bullet_speed = 1
        self.b_state = "ready"
        self.b_list = []

    def show(self):
        WINDOW.blit(self.player, (self.x_position, self.y_position))

    def x_movement(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RIGHT] and self.x_position < WIDTH - 65:
            self.x_position += 0.2
        elif keys_pressed[pygame.K_LEFT] and self.x_position > -15:
            self.x_position -= 0.2

    def shoot(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE]:
            bullet = pygame.transform.scale(BULLET, (BULLET_SIZE))
            self.b_list.append(bullet)

            if self.b_state == "ready":
                self.b_state = "shoot"
                self.xb_position = self.x_position

        if self.b_state == "shoot":
            for bullet in self.b_list:
                WINDOW.blit(bullet, (self.xb_position + 24,
                            self.yb_position - 32))
            self.yb_position -= self.bullet_speed

        if self.yb_position <= 0:
            self.yb_position = 600 - 80
            self.b_state = "ready"


# Clase para los enemigos
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
