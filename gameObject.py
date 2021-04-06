#!/usr/bin/env python
# la siguiente línea no es necesaria en python 3
# -*- coding: utf-8 -*-

# Módulos
import os
import sys
import pygame
from pygame.locals import *

# Constantes
WIDTH = 640
HEIGHT = 480

# Clases
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pruebas Pygame")
    while True:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                pygame.quit()
                sys.exit(0)
    return 0


if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    main()
