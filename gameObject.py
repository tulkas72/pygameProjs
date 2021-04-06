#!/usr/bin/env python
# la siguiente línea no es necesaria en python 3
# -*- coding: utf-8 -*-

# Módulos
import os
import sys
import pygame
from pygame.locals import *  # para QUIT, teclas etc.

# Constantes
WIDTH = 640
HEIGHT = 480

# Clases
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------


def load_image(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, pygame.RLEACCEL)
    return image
# ---------------------------------------------------------------------


def main():
    # establecer el modo de la pantalla de juego
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pruebas Pygame")  # crear y abrir la ventana
    background_image = load_image('images/fondo4.jpg')  # cargar imagen
    while True:  # bucle de juego Game Loop
        for eventos in pygame.event.get():  # manejo de eventos
            if eventos.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit(0)

        # ponerla en la ventana, en la posición x=0,y=0
        screen.blit(background_image, (0, 0))
        pygame.display.flip()  # actualiza la pantalla para que se muestre la imagen
    return 0


if __name__ == '__main__':
    # establecer variable de entorno para centrar la venta Linux, ¿Windows?
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()  # habla por sí sola
    main()
