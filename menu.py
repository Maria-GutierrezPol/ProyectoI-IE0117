#!/usr/bin/python3

import pygame
import os
import sys

from button_class import Button

pygame.init()

WIDTH, HEIGHT = 350, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
FONT_SIZE_MENU = 40
FONT_SIZE_OPTIONS = 10
FONT_SIZE_BACK = 20

# Carcateristicas del display principal
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Texto
about_text = """Tetris es un videojuego de lógica originalmente diseñado
y programado por Alekséi Pázhitnov en la Unión Soviética.
Fue lanzado el 6 de junio de 1984, ​ mientras trabajaba para
el Centro de Computación Dorodnitsyn de la Academia de Ciencias
de la Unión Soviética en Moscú, RSFS de Rusia."""

# Imagenes
BACKGROUND_BIG = pygame.image.load(os.path.join('Assets', 'wallpaper.jpg'))
BACKGROUND_MAIN = pygame.transform.scale(BACKGROUND_BIG, (WIDTH, HEIGHT))

BUTTON_BIG = pygame.image.load(os.path.join("Assets", "button_rect.png"))
BUTTON_RECT = pygame.transform.scale(BUTTON_BIG, (BUTTON_WIDTH, BUTTON_HEIGHT))

#PLAY_BIG = pygame.image.load(os.path.join("Assets", "Play Rect.png"))
#PLAY_RECT = pygame.transform.scale(PLAY_BIG, (BUTTON_WIDTH, BUTTON_HEIGHT))

#OPREC_BIG = pygame.image.load(os.path.join("assets", "Options Rect.png"))
#OPTIONS_RECT = pygame.transform.scale(OPREC_BIG, (BUTTON_WIDTH, BUTTON_HEIGHT))

#ABOUT_BIG = pygame.image.load(os.path.join("Assets", "About Rect.png"))
#QUIT_RECT = pygame.transform.scale(ABOUT_BIG, (BUTTON_WIDTH, BUTTON_HEIGHT))

#QUIT_BIG = pygame.image.load(os.path.join("Assets", "Quit Rect.png"))
#QUIT_RECT = pygame.transform.scale(QUIT_BIG, (BUTTON_WIDTH, BUTTON_HEIGHT))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Funcion para cambiar el tamano de la tipgrafia
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(os.path.join('Assets', 'font.ttf'), size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        WINDOW.fill(BLACK)

        PLAY_TEXT = get_font(FONT_SIZE_OPTIONS).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(WIDTH/2, HEIGHT/4))
        WINDOW.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(None, (WIDTH/2, HEIGHT - 100), "VOLVER", get_font(FONT_SIZE_BACK), WHITE, "Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WINDOW.fill("white")

        OPTIONS_TEXT = get_font(FONT_SIZE_OPTIONS).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2))
        WINDOW.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(None, (WIDTH/2, HEIGHT - 100), "VOLVER", get_font(FONT_SIZE_BACK), "Black", "Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


# Funcion para mostar uan breve explicacion acerca del juego
def about():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        WINDOW.fill(BLACK)

        PLAY_TEXT = get_font(FONT_SIZE_OPTIONS).render(about_text, True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(WIDTH/2, HEIGHT/4))
        WINDOW.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(None, (WIDTH/2, HEIGHT-100), "VOLVER", get_font(FONT_SIZE_BACK), WHITE, "Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        WINDOW.blit(BACKGROUND_MAIN, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(FONT_SIZE_MENU).render("TETRIS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, HEIGHT/5))

        PLAY_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3), "PLAY", get_font(FONT_SIZE_OPTIONS), "#d7fcd4", WHITE)
        OPTIONS_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 100), "OPTIONS", get_font(FONT_SIZE_OPTIONS), "#d7fcd4", WHITE)
        ABOUT_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 200), "ABOUT", get_font(FONT_SIZE_OPTIONS), "#d7fcd4", WHITE)
        QUIT_BUTTON = Button(BUTTON_RECT, (WIDTH/2, HEIGHT/3 + 300), "QUIT", get_font(FONT_SIZE_OPTIONS), "#d7fcd4", WHITE)

        WINDOW.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WINDOW)

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

        pygame.display.update()


main_menu()
