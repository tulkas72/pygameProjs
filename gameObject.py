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

class Bola(pygame.sprite.Sprite):
    """
    La línea 1 crea la clase Bola que hereda los métodos de la clase pygame.sprite.Sprite, esto es muy importante
    debido a que contiene métodos necesarios para el manejo de Sprites.

    La línea 2 crea el método __init__ que inicializa la clase.

    La línea 3 invoca al método init de la clase heredada, muy importante también y difícil de explicar para comenzar.

    La línea 4 ya nos suena más y lo que hace es cargar con nuestra función load_image() la imagen de la pelota,
    como vemos tenemos puesto True porque la pelota si tiene zonas transparentes.

    La línea 5 es de las cosas más útiles de pygame la función self.image.get_rect() obtiene un rectangulo con las
    dimensiones y posición de la imagen (en este caso self.image) y se lo asignamos a self.rect

    Aquí hago un inciso para comentar que get_rect() tiene unos parámetros muy útiles que podemos modificar para
    posicionar y redimensionar nuestra imagen, son los siguientes:

        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        center, centerx, centery
        size, width, height
        w, h

    Así que podemos acceder a los diferentes valores como self.rect.centerx que nos devuelve la posición central de
    la pelota respecto al ancho de la pantalla, y así con todos es cuestión de probarlos, pero más o menos se
    entiende lo que devuelve cada uno. Lo mejor de todos ellos es que si cambias el valor de alguno el resto se
    actualiza. Aquí lo tenéis mejor expliado.

    En la línea 6 y 7 usamos las propiedades de rect y con centerx y centery definimos el centro de la pelota en el
    centro de la pantalla. (aquí vemos porque pusimos WIDTH y HEIGHT como constantes globales).

    La línea 8 define la velocidad que queremos para la pelota, separamos la velocidad en dos, la velocidad en el eje
    x y la velocidad en el eje y, luego veremos porqué.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed = [0.5, -0.5]

    def actualizar(self, time, pala_jug, pala_cpu, puntos):
        """[summary] La linea 1 define el método, recibe el parámetro self (como siempre) y el parámetro time que es
        el tiempo transcurrido, más adelante lo explicamos.

        La línea 2 y 3 usa la física básica de espacio es igual a la velocidad por el tiempo (e = v*t), por tanto
        establecemos que el centro de nuestro rectangulo en x es el valor que tenía (self.rect.centerx) más (+=) la
        valocidad a la que se mueve en el eje x (self.speed[0]) por (*) el tiempo transcurrido (time). Lo mismo se
        aplica al eje y en la línea 3.

        La linea 4, 5 y 6 establece que si la parte izquierda del rectángulo de la bola es menor o igual a 0 ó mayor
        o igual a el ancho de la pantalla (WIDTH), es decir,  que este en el extremo izquierdo o derecho,
        la velocidad de x (self.speed[0]) cambie de signo (-self.speed[0]) con esto conseguiremos que vaya hacia el
        otro lado.

        Las líneas 7, 8 y 9 es lo mismo pero en el eje y como se puede ver.

        Como vemos todo igual, salvo que ahora recibe un parámetro más que es pala_jug por el que pasaremos el Sprite
        con el que queremos comprobar si colisiona, en este caso pala_jug.

        Luego al final añadimos 3 líneas con un nuevo condicional con el que comprobamos si la pelota choca contra la
        pala, en caso afirmativo cambiamos la dirección de la bola como cuando choca con el borde izquierdo de la
        ventana
        --
        Como podemos ver añadimos otro párametro al método pala_cpu que servirá para añadirle el Sprite pala_cpu como
        hicimos con pala_jug y añadimos las tres últimas líneas que son idénticas a las anteriores salvo que ahora
        para pala_cpu.
        ---
        Como vemos le añadimos un nuevo parámetro llamado puntos, puntos es una lista que contiene los puntos de los
        dos jugadores en el el puntos[0] los puntos del jugador y en el puntos[1] los puntos de la cpu.

        Luego añadimos las líneas de la 5 a la 8 que controlan si la parte izquierda de la pelota (línea 5) toca el
        el borde izquierdo de la ventana en cuyo caso aumenta puntos[1] (el marcador de la cpu) en 1 (línea 6). La
        líneas 7 y 8 hacen lo mismo, pero a la inversa.

        Por último al final del método se retorna puntos, necesario para almacenarla en una variable.

        Args:
            time ([type]): [description]
            pala_jug([type]): [description]
        """

        self.rect.centerx += int(self.speed[0] * time)
        self.rect.centery += int(self.speed[1] * time)
        if self.rect.left <= 0:
            puntos[1] += 1
        if self.rect.right >= WIDTH:
            puntos[0] += 1

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += int(self.speed[0] * time)

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time

        # Saber si un Sprite colisiona con otro es muy fácil en Python, basta con ejecutar el siguiente método:
        if pygame.sprite.collide_rect(self, pala_jug):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

        #añadida colisión con pala de CPU
        if pygame.sprite.collide_rect(self, pala_cpu):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

        return puntos


class Pala(pygame.sprite.Sprite):
    """
    Como vemos es casi idéntica a bola, salvo que ahora le pasamos el parámetro x para usarlo en self.rect.centerx,
    esto es debido a que necesitamos dos palas una en la parte izquierda y otra en la derecha, con el parámetro x
    definimos a que altura del eje x queremos colocar el Sprite.

    Otro cambio es la velocidad, como la pala del Pong solo se mueve en el eje y no definimos velocidad para el eje x.
    """

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("images/pala.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5

    def mover(self, time, keys):
        """
        Recibe los parámetros self y time como el método actualizar de la bola y además recibe el parámetro keys que
        luego definiremos y que es una lista con el valor booleano de las teclas pulsadas.

        La línea 2 y 5 comprueban que la parte superior (en el caso de la linea 2) de la pala sea mayor o igual a 0 y
        que la parte inferior de la pala (línea 5) sea menor o igual que que la altura de la ventana. Resumiendo
        comprueban que la pala no se sale de la ventana.

        La línea 3 comprueba si la constante K_UP de keys es 1, lo que querría decir que tenemos presionada la tecla
        de la flecha hacia arriba del teclado.

        La línea 5 en caso de tener la tecla presionada disminuye el valor de centery haciendo que la pala se mueva
        hacia arriba.

        La línea 6 y 7 hacen lo mismo, pero para abajo y aumentando el valor de centery.
        :param time:
        :param keys:
        :return:
        """
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time

    def ia(self, time, ball):
        """
        En la línea 1 vemos que recibe como siempre self y time y aparte recibe ball que es la bola, es necesario
        pues el método necesita conocer donde está la bola.

        En la línea 2 comprobamos que ball.speed[0] >= 0, es decir, que la velocidad en el eje x de la pelota sea
        positiva, es decir, que la pelota se este moviendo hacia la derecha (hacia la pala de la cpu) y tambien
        comprueba que ball.rect.centerx >= WIDTH/2 es decir que el centro x de la pelota sea mayor o igual que el
        centro del tablero, es decir, que la pelota este en el campo de la cpu.

        Por tanto la línea 2 es un condicional que comprueba que la pelota vaya hacia donde está la pala de la cpu y
        que este en su campo, sino, que no se mueva. Esto se hace para que la CPU no sea invencible y no llegue a
        todas las pelotas.

        La línea 3 comprueba si el centery de la pelota es menor que el centery de la bola, es decir si la pala está
        más arriba que que la pelota en cullo caso, ejecuta la línea 4 que mueve la pala de la cpu hacia abajo.

        Las líneas 5 y 6 hacen lo mismo, pero a la inversa como se ve a simple vista.
        :param time:
        :param ball:
        :return:
        """
        if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH / 2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed * time
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
        colour = image.get_at((0, 0))
        image.set_colorkey(colour, pygame.RLEACCEL)
    return image

def texto(texto, posx, posy, color=(255, 255, 255)):
    """
    En la línea 1 creamos la función, vemos que recibe 4 parámetros: texto que debe ser una string, posx y posy que
    serán las coordenadas del centro de nuestro texto y color que es una tupla con los valores RGB, color es opcional
    y si no se define, por defecto será blanco.

    La línea 2 asigna una tipografía a la variable fuente como vemos lo hacemos con pygame.font.Font() al que le
    pasamos como primer parámetro la ruta de la tipografía que queremos usar y como segundo el tamaño de la tipografía.

    En la linea 3 creamos la variable salida asignandole pygame.font.Font.render() este método lo que hace es
    convertir un texto en un Sprite, como vemos como primer parámetro recibe una fuente tipográfica, le pasamos la
    creada en la línea anterior, como segundo recibe el texto a mostrar, el tercer parámetro es el antialias y puede
    ser verdadero o falso (con o sin antialias), por último recibe el color.

    En la línea 4 obtenemos el rect como si de un Sprite más se tratare y lo almacenamos en salida_rect.

    Las líneas 5 y 6 modifican el centro del Sprite en función de los valores posx y posy.

    Por último la línea 7 retorna una tupla con el Sprite y su correspondiente rect. Ojo a la ahora de utlizarla,
    recordad que retorna dos valores y no uno.

    :param texto:
    :param posx:
    :param posy:
    :param color:
    :return:
    """
    fuente = pygame.font.Font("images/DroidSans.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

# ---------------------------------------------------------------------


def main():
    # establecer el modo de la pantalla de juego
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pruebas Pygame")  # crear y abrir la ventana
    background_image = load_image('images/fondo_pong.png')  # cargar imagen
    bola = Bola()
    pala_jug = Pala(30)
    pala_cpu = Pala(WIDTH - 30) #pala del ordenador a 30 píxeles del borde

    # Ahora vamos a crear un reloj que controle el tiempo del juego, esto es
    # importante para el movimiento, pues sabemos cuanto tiempo a pasado desde
    # la ultima actualización de la pelota y con ello poder situarla en el espacio.
    clock = pygame.time.Clock()

    puntos = [0, 0]

    while True:  # bucle de juego Game Loop
        # Ahora necesitamos saber cuanto tiempo pasa cada vez que se ejecuta
        # una interección del bucle, para ello dentro del bucle ponemos como primera línea:
        # 60 nos da el "framerate"
        time = clock.tick(60)
        keys = pygame.key.get_pressed()  # controlar pulsación de teclas
        for eventos in pygame.event.get():  # manejo de eventos
            if eventos.type == QUIT:  # pygame.locals.QUIT
                pygame.quit()
                sys.exit(0)

        # actualizar la posición de la bola, pala del jugador y de la cpu antes de repintar
        #actualizar también los puntos
        puntos=bola.actualizar(time, pala_jug, pala_cpu, puntos)
        pala_jug.mover(time, keys)
        pala_cpu.ia(time, bola)

        # Con la función texto() poner texto es muy fácil, vamos a utilizarla para mostrar nuestras puntuaciones,
        # añadimos las siguientes líneas en el bucle del juego:

        p_jug, p_jug_rect = texto(str(puntos[0]), WIDTH / 4, 40)
        p_cpu, p_cpu_rect = texto(str(puntos[1]), WIDTH - WIDTH / 4, 40)

        #Las dos líneas anteriores nos crea dos Sprites con sus respectivos rects. El primero recibe como texto puntos[0], es decir los
        #puntos del jugador (ojo con la conversión str(), recodad que debe de ser una string), como parámetro posx
        #recibe WIDTH/4 es decir la WIDTH/2/2 que es la mitad de la mitad de la pantalla (para centrarlo en el campo
        #del jugador) y como parámetro posy he situado a 40px del norde superior.
        #El otro Sprite exactamente lo mismo, pero para los puntos de la CPU y centrado en el campo de la CPU el posx
        #(WIDTH-WIDTH/4).


        screen.blit(background_image, (0, 0))# ponerla en la ventana, en la posición x=0,y=0


        screen.blit(bola.image, bola.rect)  # dibujar la bola
        screen.blit(pala_jug.image, pala_jug.rect)  # dibujar pala del jugador
        screen.blit(pala_cpu.image, pala_cpu.rect)  # dibujar pala de la cpu
        pygame.display.flip()  # actualiza la pantalla para que se muestre la imagen
        # Ponemos los sprites del marcador ¿por qué la pelota pasa por debajo?
        screen.blit(p_jug, p_jug_rect)
        screen.blit(p_cpu, p_cpu_rect)
    return 0


if __name__ == '__main__':
    # establecer variable de entorno para centrar la venta Linux, ¿Windows?
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()  # habla por sí sola
    main()
