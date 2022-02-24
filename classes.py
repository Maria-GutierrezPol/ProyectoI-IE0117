#!/usr/bin/python3

import pygame
import random
import os

pygame.init()

# CONSTANTES ------------------------------------------------------------------
PLAYER_SIZE = (80, 80)
ENEMY_SIZE = (80, 80)
WIDTH, HEIGHT = 400, 600
BULLET_SIZE = (30, 30)

# IMAGENES --------------------------------------------------------------------

BACKGROUND_BIG = pygame.image.load(os.path.join('Assets', 'wallpaper.jpg'))
BACKGROUND_MAIN = pygame.transform.scale(BACKGROUND_BIG, (WIDTH, HEIGHT))

ENEMY_1 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level1.png')), 180)

PLAYER = pygame.image.load(os.path.join('Assets', 'enemy_level3.png'))

BULLET = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'player_bullet.png')), 90)

RED_BULLET = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'red_bullet.png')), 90)

# DISPLAY ---------------------------------------------------------------------

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Sonido del disparo del jugador.
bullet_sound = pygame.mixer.Sound(os.path.join('Assets', 'blaster.mpga'))

# CLASES ----------------------------------------------------------------------


# Clase botón, cuya implementacion se incluye en el menu principal y en los
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

    # Función para actualizar la pantalla principal
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # Función para revisar si el usuario dio algun input
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right):
            if position[1] in range(self.rect.top, self.rect.bottom):
                return True
        return False

    # Función para determinar si el usuario se encuentra posicionado sobre
    # algun botón del menu, de ser asi cambia su color.
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
    def __init__(self, velocity):
        self.background = BACKGROUND_MAIN
        self.rect = self.background.get_rect()
        self.x_position = 0
        self.y1_position = 0
        self.y2_position = self.rect.height
        self.speed = velocity

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
        self.bullet = pygame.transform.scale(BULLET, (BULLET_SIZE))
        self.x_position = 200 - 40
        self.y_position = 600 - 80
        self.xb_position = 0
        self.yb_position = 600 - 80
        self.bullet_speed = 8
        self.b_state = "ready"

    # Dibujar al jugador en pantalla.
    def show(self):
        WINDOW.blit(self.player, (self.x_position, self.y_position))

    # Movimiento del jugador, unicamente se da en la coordenada x.
    def x_movement(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RIGHT] and self.x_position < WIDTH - 65:
            self.x_position += 1.5
        elif keys_pressed[pygame.K_LEFT] and self.x_position > -15:
            self.x_position -= 1.5

    # Disparo del jugador, se da al presionar la tecla espaciaora.
    def shoot(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE]:
            if self.b_state == "ready":
                bullet_sound.play()
                self.b_state = "shoot"
                self.xb_position = self.x_position

        if self.b_state == "shoot":
            WINDOW.blit(self.bullet, (self.xb_position + 24,
                        self.yb_position - 32))
            self.yb_position -= self.bullet_speed

        if self.yb_position <= 0:
            self.yb_position = 600 - 80
            self.b_state = "ready"

    # Reestablecer la nave del jugador al terminar el juego.
    def restart(self):
        self.x_position = 200 - 40
        self.y_position = 600 - 80
        self.xb_position = 0
        self.yb_position = 600 - 80
        self.b_state = "ready"


# Clase bala, se utiliza únicamnete para crear una bala, ya que no presenta
# métodos
class bullet:
    def __init__(self, bullet_image, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
        self.bullet_image = bullet_image


# Clase para los enemigos
class enemies:
    def __init__(self, enemy_ship):
        self.x_position = random.randint(0, WIDTH - 100)
        self.y_position = random.randint(-30, -10)
        self.by_position = self.y_position
        self.xb_position = self.x_position + 15
        self.change_x = 0.5
        self.change_y = 1
        self.enemy_bullets = []

    # Mostrar enemigos en pantalla
    def show(self, enemy_ship):
        WINDOW.blit(enemy_ship, (self.x_position, self.y_position))
        for bullet in self.enemy_bullets:
            WINDOW.blit(pygame.transform.scale(RED_BULLET, (BULLET_SIZE)),
                        (self.xb_position + 30, self.by_position + 50))

    # Movimiento de los enemigos
    def movement(self):
        self.x_position += self.change_x
        self.y_position += self.change_y

        # Evitar que el enemigo salga de la pantalla.
        if self.x_position <= 0:
            self.change_x += 0.005
        elif self.x_position > WIDTH - 100:
            self.change_x -= 0.005

        if self.y_position <= 0:
            self.change_y += 0.005

    # Movimiento de las balas enemigas
    def bullet_movement(self, velocity):
        self.by_position += velocity

    # Crear nueva bala
    def shoot(self, red_bullet):
        new_enemy_bullet = bullet(red_bullet, self.xb_position,
                                  self.by_position)
        self.enemy_bullets.append(new_enemy_bullet)

    # Resetear la lista de balas para poder jugar varias veces
    def restart(self):
        self.x_position = random.randint(0, WIDTH - 100)
        self.y_position = random.randint(-30, -10)
        for new_enemy_bullet in self.enemy_bullets:
            self.enemy_bullets.remove(new_enemy_bullet)
