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

# Carcaterísticas del display principal ---------------------------------------
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACESHIP SHOOTER")
clock = pygame.time.Clock()

# Imágenes --------------------------------------------------------------------
BACKGROUND_BIG = pygame.image.load(os.path.join('Assets', 'wallpaper.jpg'))
BACKGROUND_MAIN = pygame.transform.scale(BACKGROUND_BIG, (WIDTH, HEIGHT))

BUTTON_BIG = pygame.image.load(os.path.join("Assets", "button_rect.png"))
BUTTON_RECT = pygame.transform.scale(BUTTON_BIG, (BUTTON_WIDTH, BUTTON_HEIGHT))

ENEMY_1 = pygame.transform.rotate(pygame.image.load(
          os.path.join('Assets', 'enemy_level1.png')), 180)

PLAYER = pygame.transform.rotate(pygame.image.load(
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
enemy_sound = pygame.mixer.Sound(os.path.join('Assets', 'down_enemy.mpga'))
bullet_sound = pygame.mixer.Sound(os.path.join('Assets', 'blaster.mpga'))

# Instancias ------------------------------------------------------------------
background = moving_background(2)
about_background = moving_background(1)
player = player()

# Listas ----------------------------------------------------------------------
enemy_list = []
enemy_bullet = []

# FUNCIONES -------------- ----------------------------------------------------


# Función para cambiar el tamano de la tipografía
def get_font(size):
    return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)


# Función con la tipografia de la sección "Acerca"
def get_font_about(size):
    return pygame.font.Font(os.path.join('Assets', 'mandalore.ttf'), size)


# Función para calcular la distancia
def collision(bullet_x, bullet_y, enemy_x, enemy_y):
    # Fórmula para la ditancia entre dos puntos
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2) +
                         math.pow(enemy_y - bullet_y, 2)))

    # Si la distancia entre las ballas y las naves es menor a 20 pixeles se
    # considera como una colisión
    if distance < 25:
        return True


# Función para mostrar multiples líneas de texto en la pantalla
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


def show_scores(score):
    # Mensajes a imprimir en pantalla
    GAME = get_font_about(20).render("SPACESHIP SHOOTER", 1, YELLOW)
    SCORE = get_font_about(20).render(f"Puntaje: {score}", 1, YELLOW)
    ESC = get_font_about(20).render("esc", True, YELLOW)

    # Mostrar en pantalla las vidas y el puntaje del jugador, además se
    # indica que con la tecla escape es posible salir del juego.
    WINDOW.blit(GAME, (10, 10))
    WINDOW.blit(SCORE, (10, 30))
    WINDOW.blit(ESC, (WIDTH - 30, 10))
    pygame.display.update()


# Función para implementar el juego, recibe la puntuación inicial del jugador
# (incialmente 50) y el contador de enemigos, el que se encarga de generar olas
# de ataque, en cada ola se incrementa el numero de naves enemigas.
def play():
    enemy_count = 1
    run = True
    lost = False
    lost_count = 0
    score = 50
    while run:
        clock.tick(FPS)

        # Movilidad del jugador
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
                enemy_sound.play()

        # Por cada elemento en la lista, es decir, por cada enemigo creado se
        # dibuja en pantalla y se le aplica movimiento.
        for new_element in enemy_list:
            new_element.show(pygame.transform.scale(ENEMY_1, (ENEMY_SIZE)))
            new_element.movement()

            # Disparo de las naves enemigas
            if new_element.y_position > 0:
                new_element.bullet_movement(5)
                new_element.shoot(pygame.transform.scale(BULLET,
                                  (BULLET_SIZE)))

            # COLISIONES
            # Caso 1: la bala enemiga toca al jugador
            if collision(new_element.xb_position, new_element.by_position,
                         player.x_position, player.y_position) is True:
                lost = True

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
                score -= 20
                enemy_list.remove(new_element)

            # Si el jugador presiona la tecla "esc" se pausa el juego y se
            # vuelve al menú principal.
            esc_pressed = pygame.key.get_pressed()
            if esc_pressed[pygame.K_ESCAPE]:
                enemy_count = 0
                for new_element in enemy_list:
                    enemy_list.remove(new_element)
                main_menu()

        # Mostrar mensaje final y salir del juego debido a que el usuario
        # perdió la partida.
        if lost is True:
            SCORE = get_font_about(30).render("Juego finalizado", True, YELLOW)
            WINDOW.blit(SCORE, (WIDTH/2 - SCORE.get_width()/2, HEIGHT/2))
            pygame.display.update()
            pygame.time.wait(1500)
            run = False

        # Salir del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        show_scores(score)
        pygame.display.update()
        background.window_update()
        background.move_background()


# Opciones del juego: activar y desactivar música de fondo y pantalla grande.
def options():
    while True:

        # Posición del mouse en pantalla
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Mostrar la imagen de fondo
        WINDOW.blit(BACKGROUND_MAIN, (0, 0))

        # Creación del botón "OPCIONES"
        # Tipografía y mensaje
        OPTIONS_TEXT = get_font(FONT_SIZE_OPTIONS).render("OPCIONES",
                                                          True, BLUE)

        # Rectángulo y posicionamiento
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH/2, HEIGHT/6))

        # Mostrar boton en pantalla
        WINDOW.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Creación del botón "VOLVER"
        # Tipografía y mensaje
        OPTIONS_BACK = Button(BUTTON_RECT, (WIDTH/2, HEIGHT - 100), "VOLVER",
                              get_font(FONT_SIZE_OPTIONS), WHITE, YELLOW)

        # Cambio de color al poscionar el mouse en el botón, además se
        # actualiza la pantalla para mostrar este cambio.
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WINDOW)

        # Opción de activar sonido
        OPTIONS_sonidoA = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/2),
                                 "Activar sonido", get_font(FONT_SIZE_OPTIONS),
                                 WHITE, YELLOW)
        OPTIONS_sonidoA.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_sonidoA.update(WINDOW)

        # Opción de apagar el sonido
        OPTIONS_sonidoD = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3),
                                 "Desactivar sonido",
                                 get_font(FONT_SIZE_OPTIONS), WHITE, YELLOW)
        OPTIONS_sonidoD.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_sonidoD.update(WINDOW)

        # Opción pantalla completa
        OPTIONS_fs = Button(BUTTON_RECT, (WIDTH/2, HEIGHT-200),
                            "Pantalla completa",
                            get_font(FONT_SIZE_OPTIONS), WHITE, YELLOW)
        OPTIONS_fs.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_fs.update(WINDOW)

        # Asignación de las tareas a realizar al presionar cada botón.
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


# Función para mostar una breve explicacion acerca del juego
def about():
    WINDOW.blit(BACKGROUND_MAIN, (0, 0))
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Mostrar el contenido del about.json
        with open(os.path.join('Assets', 'about.json')) as show:
            multiline_render(json.load(show))

        #  Botón para volver al menú principal
        PLAY_BACK = Button(None, (WIDTH/2, HEIGHT-100), "VOLVER",
                           get_font(FONT_SIZE_BACK), WHITE, YELLOW)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(WINDOW)

        # Botón para iniciar el juego
        PLAY_BUTTON = Button(None, (WIDTH/2, HEIGHT-180), "JUGAR",
                             get_font(FONT_SIZE_OPTIONS), WHITE, BLUE)
        PLAY_BUTTON.changeColor(PLAY_MOUSE_POS)
        PLAY_BUTTON.update(WINDOW)

        # Asignación detareas a realizar con los botones "VOLVER" y "JUGAR"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if PLAY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode(SCREEN)

        # Fondo de pantalla
        pygame.display.update()
        about_background.window_update()
        about_background.move_background()


def main_menu():
    while True:
        # Mostrar fondo de pantalla
        WINDOW.blit(BACKGROUND_MAIN, (0, 0))

        # Obtener la posicion del mouse en pantalla
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Título del juego.
        # Asignación del nombre a utilizar
        MENU_TEXT_1 = get_font(FONT_SIZE_MENU).render("SPACESHIP",
                                                      True, YELLOW)

        MENU_TEXT_2 = get_font(FONT_SIZE_MENU - 10).render("SHOOTER",
                                                           True, YELLOW)

        # Ubicación del titulo del juego
        MENU_RECT_1 = MENU_TEXT_1.get_rect(center=(WIDTH/2, HEIGHT/8))
        MENU_RECT_2 = MENU_TEXT_2.get_rect(center=(WIDTH/2, HEIGHT/5))

        # Creación de los botones del menu principal
        # Botón de juego
        PLAY_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3), "JUGAR",
                             get_font(FONT_SIZE_OPTIONS), WHITE, GRAY)

        # Botón de opciones
        OPTIONS_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 100),
                                "OPCIONES", get_font(FONT_SIZE_OPTIONS),
                                WHITE, GRAY)

        # Botón de acerca
        ABOUT_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 200), "ACERCA",
                              get_font(FONT_SIZE_OPTIONS), WHITE, GRAY)

        # Botón para abandonar el programa
        QUIT_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 300), "SALIR",
                             get_font(FONT_SIZE_OPTIONS), WHITE, GRAY)

        # Mostrar el nombre del juego en pantalla
        WINDOW.blit(MENU_TEXT_1, MENU_RECT_1)
        WINDOW.blit(MENU_TEXT_2, MENU_RECT_2)

        # Cambiar color del botón al posicionarse sobre este
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WINDOW)

        # Asiganción de las tareas a realizar con cada botón
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
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
