#!/usr/bin/python3

# Creacion del objeto boton, cuya implementacion se incluye en el menu
# principal y en los sub menues.
class Button():
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
