#!/usr/bin/python3

import pygame
import os
import sys
import json
import random

from classes import Button, moving_background, player, enemies, bullet

pygame.init()

# Constantes ------------------------------------------------------------------
SCREEN = WIDTH, HEIGHT = 400, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
FONT_SIZE_MENU = 50
FONT_SIZE_OPTIONS = 16
FONT_SIZE_BACK = 20
ENEMY_SIZE = (80, 80)
BULLET_SIZE = (30, 30)
FPS = 60

# Carcateristicas del display principal ---------------------------------------
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACESHIP SHOOTER")
clock = pygame.time.Clock()

# Imagenes --------------------------------------------------------------------
BACKGROUND_BIG = pygame.image.load(os.path.join('Assets', 'wallpaper.jpg'))
BACKGROUND_MAIN = pygame.transform.scale(BACKGROUND_BIG, (WIDTH, HEIGHT))

BUTTON_BIG = pygame.image.load(os.path.join("Assets", "button_rect.png"))
BUTTON_RECT = pygame.transform.scale(BUTTON_BIG, (BUTTON_WIDTH, BUTTON_HEIGHT))

ENEMY_1 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level1.png')), 180)

ENEMY_2 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level2.png')), 180)

ENEMY_3 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level3.png')), 180)

BULLET = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'player_bullet.png')), 90)

# Colores ---------------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 198, 51)
GRAY = (150, 150, 150)
BLUE = (30, 144, 255)

# Sonido del juego ------------------------------------------------------------
pygame.mixer.music.load(os.path.join("Assets", "dragonball.mpga"))
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0)

# Instancias ------------------------------------------------------------------
background = moving_background()
player = player()

# Listas ----------------------------------------------------------------------
enemy_list = []
enemy_bullet = []

# FUNCIONES -------------- ----------------------------------------------------


# Funcion para cambiar el tamano de la tipgrafia
def get_font(size):
    return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)


# Funcion para mostrar multiples lineas de texto en la pantalla
def multiline_render(render_text):
    position = 50
    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(0, 0, 0, 0))
    for x in range(len(render_text)):
        rendered = get_font(30).render(render_text[x], 100, (WHITE))
        WINDOW.blit(rendered, (20, position))
        position += 40


# Funcion para implementar el juego, recibe la puntuacion inicial del jugador
# (incialmente 0) y el contador de enemigos, el que se encarga de generar olas
# de ataque enemigo, en cada ola se incrementa el numero de naves enemigas.
def play(score, enemy_count):
    run = True
    while run:
        clock.tick(FPS)

        # Si la lista de enemigos se encuentra vacia se agregan un enemigo mas
        # en la ola anterior.
        if len(enemy_list) == 0:
            score += 100
            enemy_count += 1
            for number in range(enemy_count):
                new_element = enemies(pygame.transform.scale(ENEMY_1,
                                      (ENEMY_SIZE)))
                enemy_list.append(new_element)

        # Por cada elemento en la lista, es decir, por cada enemigo creado se
        # dibuja en pantalla y se le aplica movimiento.
        for new_element in enemy_list:
            new_element.show(pygame.transform.scale(ENEMY_1, (ENEMY_SIZE)))
            new_element.movement()

            if random.randrange(0, 120) == 1:
                new_element.shoot(pygame.transform.scale(BULLET,
                                  (BULLET_SIZE)))
                new_element.bullet_movement(50)

            # Si la nave llega al final de la pantalla, se elimina de la Lista
            # y se disminuye el puntaje del jugador.
            if new_element.y_position > HEIGHT + 10:
                score -= 20
                enemy_list.remove(new_element)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Si el jugador presiona la tecla "esc" se pausa el juego y se vuelve
        # al menu principal.
        esc_pressed = pygame.key.get_pressed()
        if esc_pressed[pygame.K_ESCAPE]:
            main_menu()
            run = False

        pygame.display.update()

        background.window_update()
        background.move_background()
        player.show()
        player.x_movement()
        player.shoot()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WINDOW.fill(BLACK)

        OPTIONS_TEXT = get_font(FONT_SIZE_OPTIONS).render("OPCIONES",
                                                          True, BLUE)

        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH/2, HEIGHT/6))
        WINDOW.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(BUTTON_RECT, (WIDTH/2, HEIGHT - 100), "VOLVER",
                              get_font(FONT_SIZE_OPTIONS), WHITE, YELLOW)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WINDOW)

        OPTIONS_sonidoA = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/2),
                                 "Activar sonido", get_font(FONT_SIZE_OPTIONS),
                                 WHITE, YELLOW)
        OPTIONS_sonidoA.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_sonidoA.update(WINDOW)
        # sound_on = True
        OPTIONS_sonidoD = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3),
                                 "Desactivar sonido",
                                 get_font(FONT_SIZE_OPTIONS), WHITE, YELLOW)
        OPTIONS_sonidoD.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_sonidoD.update(WINDOW)

        OPTIONS_fs = Button(BUTTON_RECT, (WIDTH/2, HEIGHT-200),
                            "Pantalla completa",
                            get_font(FONT_SIZE_OPTIONS), WHITE, YELLOW)
        OPTIONS_fs.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_fs.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_sonidoA.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.music.play(loops=-1)
                if OPTIONS_sonidoD.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.mixer.music.stop()
                if OPTIONS_fs.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.display.set_mode(SCREEN,
                                            pygame.SCALED | pygame.FULLSCREEN)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode(SCREEN)

        pygame.display.update()


# Funcion para mostar uan breve explicacion acerca del juego
def about():
    WINDOW.blit(BACKGROUND_MAIN, (0, 0))
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        with open(os.path.join('Assets', 'about.json')) as show:
            multiline_render(json.load(show))

        PLAY_BACK = Button(None, (WIDTH/2, HEIGHT-100), "VOLVER",
                           get_font(FONT_SIZE_BACK), WHITE, YELLOW)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode(SCREEN)

        pygame.display.update()


def main_menu():
    while True:
        WINDOW.blit(BACKGROUND_MAIN, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT_1 = get_font(FONT_SIZE_MENU).render("SPACESHIP",
                                                      True, YELLOW)

        MENU_TEXT_2 = get_font(FONT_SIZE_MENU - 10).render("SHOOTER",
                                                           True, YELLOW)

        MENU_RECT_1 = MENU_TEXT_1.get_rect(center=(WIDTH/2, HEIGHT/8))
        MENU_RECT_2 = MENU_TEXT_2.get_rect(center=(WIDTH/2, HEIGHT/5))

        PLAY_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3), "JUGAR",
                             get_font(FONT_SIZE_OPTIONS), WHITE, GRAY)

        OPTIONS_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 100),
                                "OPCIONES", get_font(FONT_SIZE_OPTIONS),
                                WHITE, GRAY)

        ABOUT_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 200), "ACERCA",
                              get_font(FONT_SIZE_OPTIONS), WHITE, GRAY)

        QUIT_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 300), "SALIR",
                             get_font(FONT_SIZE_OPTIONS), WHITE, GRAY)

        WINDOW.blit(MENU_TEXT_1, MENU_RECT_1)
        WINDOW.blit(MENU_TEXT_2, MENU_RECT_2)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(0, 1)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    about()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode(SCREEN)

        pygame.display.update()


main_menu()
