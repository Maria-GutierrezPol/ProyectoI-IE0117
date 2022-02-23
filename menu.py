#!/usr/bin/python3

import pygame
import os
import sys
import json
import math

from classes import Button, moving_background, player, enemies

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
pygame.mixer.music.set_volume(0.1)
down_sound = pygame.mixer.Sound(os.path.join('Assets', 'down.mpga'))

# Instancias ------------------------------------------------------------------
background = moving_background(2)
about_background = moving_background(1)
player = player()

# Listas ----------------------------------------------------------------------
enemy_list = []
enemy_bullet = []

# FUNCIONES -------------- ----------------------------------------------------


# Funcion para cambiar el tamano de la tipgrafia
def get_font(size):
    return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)


# Funcion con la tipografia de la seccion "Acerca"
def get_font_about(size):
    return pygame.font.Font(os.path.join('Assets', 'mandalore.ttf'), size)


# Funcion para calcular la distancia
def collision(bullet_x, bullet_y, enemy_x, enemy_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2) +
                         math.pow(enemy_y - bullet_y, 2)))
    if distance < 20:
        return True


# Funcion para mostrar multiples lineas de texto en la pantalla
def multiline_render(render_text):
    position_y = 100
    position_x = 120
    size_line = 18
    pygame.draw.rect(WINDOW, BLACK, pygame.Rect(0, 0, 0, 0))
    for x in range(len(render_text)):
        rendered = get_font_about(size_line).render(render_text[x], 100,
                                                    (YELLOW))
        WINDOW.blit(rendered, (position_x, position_y))
        position_y += 45
        position_x -= 22
        size_line += 2


# Funcion para implementar el juego, recibe la puntuacion inicial del jugador
# (incialmente 0) y el contador de enemigos, el que se encarga de generar olas
# de ataque enemigo, en cada ola se incrementa el numero de naves enemigas.
def play(enemy_count):
    run = True
    score = 50
    lives = 5
    while run:
        clock.tick(FPS)
        player.show()
        player.x_movement()
        player.shoot()

        # Si la lista de enemigos se encuentra vacia se agregan un enemigo mas
        # en la ola anterior.
        if len(enemy_list) == 0:
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

            # Disparo de las nevaes enemigas
            if new_element.y_position > 0:
                new_element.bullet_movement(5)
                new_element.shoot(pygame.transform.scale(BULLET,
                                  (BULLET_SIZE)))

            # COLISION
            # Caso 1: la bala enemiga toca al jugador
            if collision(new_element.xb_position, new_element.by_position,
                         player.x_position, player.y_position) is True:
                score -= 20
                lives -= 1
                down_sound.play()

            # Caso 2: La bala del jugador toca a la nave enemiga
            elif collision(player.xb_position, player.yb_position,
                           new_element.x_position,
                           new_element.y_position) is True:
                score += 20
                down_sound.play()
                enemy_list.remove(new_element)
                player.yb_position = 0

            # Caso 3: la nave llega al final de la pantalla
            elif new_element.y_position > HEIGHT + 10:
                lives -= 1
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


        LIVES = get_font_about(20).render(f"Vidas: {lives}", 1,  YELLOW)
        SCORE = get_font_about(20).render(f"Puntaje: {score}", 1, YELLOW)
        ESC = get_font_about(20).render("esc", True, YELLOW)

        WINDOW.blit(LIVES, (10, 10))
        WINDOW.blit(SCORE, (10, 30))
        WINDOW.blit(ESC, (WIDTH - 30, 10))
        pygame.display.update()
        background.window_update()
        background.move_background()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WINDOW.blit(BACKGROUND_MAIN, (0, 0))

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

        PLAY_BUTTON = Button(None, (WIDTH/2, HEIGHT-180), "JUGAR",
                             get_font(FONT_SIZE_OPTIONS), WHITE, BLUE)
        PLAY_BUTTON.changeColor(PLAY_MOUSE_POS)
        PLAY_BUTTON.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if PLAY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    play(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode(SCREEN)

        pygame.display.update()
        about_background.window_update()
        about_background.move_background()

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
                    play(1)
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
