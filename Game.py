# -*- coding: latin-1 -*-

__author__ = "Jorge Hernandez de Benito"

from Tablero import Tablero
from TablerosFijos import TABLEROS_PREFIJADOS
from sys import exit
import copy
import os
import pygame
from pygame.locals import *

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


#CONSTANTES:
ANCHO = 640  # Ancho en pixeles de la pantalla
ALTO = 480  # Alto en pixeles de la pantalla
FPS = 20 # Frames per second

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)

class Game:
    # Clase que implementa un juego Rompebolas. Controla la lógica del juego asi como la interfaz del usuario.

    def __init__(self):
        # Constructor del juego Rompebolas.
        # t-> variable de tipo tablero.
        # puntuacion -> variable entera para almacenar la puntuacion de la partida actual
        # maxpunt -> variable entera para almacenar la maxima puntuacion en el tipo de partida actual
        # bloquesRestantes-> variable entera para almacenar las bolas restantes en el tablero.
        # puntuaciones -> lista para almacenar las puntuaciones de anteriores partidas, que son extraidas de un fichero.
        # PYGAME: reloj, pantalla, reproductor de sonidos y fuente (tipografia).
        self.t = Tablero(1)
        self.old_t = Tablero(1)
        self.puntuacion = 0
        self.maxpunt = 0
        self.bloquesRestantes = 0
        self.puntuaciones = []
        if not os.path.exists('highscores'):
            f = open('highscores', 'w')
            for i in range(0, 3 + TABLEROS_PREFIJADOS):
                f.write("0\n")
            f.close()
        with open('highscores', 'r') as f:
            for l in f.readlines():
                self.puntuaciones.append(int(l))

        pygame.init()
        self.reloj = pygame.time.Clock()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption('Rompebolas') # Cambia el nombre de la ventana.

        self.sonido = pygame.mixer.init()
        self.wrong = pygame.mixer.Sound("Sonidos\wrong.wav")
        self.button = pygame.mixer.Sound("Sonidos\\button.wav")
        self.pop = pygame.mixer.Sound("Sonidos\pop.wav")

        self.fuente = pygame.font.SysFont('iskoolapota', 26, True, False)

    def main(self):
        # Bucle principal del juego.
        while True:
            self.menu()

    def menu(self):
        # Muestra un menu y espera hasta que el usuario pinche en uno de los botones. La opción
        # seleccionada es llevada a cabo a continuacion.

        botones = [Rect((171, 18 + 66 * i), (309, 49)) for i in range(7)] # Posicion de los botones

        fondo = pygame.image.load('Graficos\Menu.png') # Pintamos el fondo
        self.pantalla.blit(fondo, fondo.get_rect())
        pygame.display.update()

        seleccion = False
        while not seleccion: 
            for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                if event.type == QUIT: # Pinchó en la cruz de cerrar la pantalla.
                    exit()
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    for i in range(7):  # Comprobamos qué botón pulsó.
                        if botones[i].collidepoint((mousex, mousey)):
                            self.button.play()
                            seleccion = True
                            break
            self.reloj.tick(FPS)
        self.opcion(i)

    def menuTablero(self):
        # Muestra un menu para seleccionar uno de los tableros prefijados.
        # Devuelve la opción tomada (0 -> atras, 1 2 o 3 -> tablero 1 2 o 3).

        fondo = pygame.image.load('Graficos\MenuTablero.png') # Pinto el fondo
        self.pantalla.blit(fondo, fondo.get_rect())
        pygame.display.update()

        botones = [Rect((594, 6), (36, 36))] # Botón de vuelta al menú principal.
        for i in range(3):
            botones.append(Rect((42 + 199 * i, 120), (157, 154))) #Cada uno de los tableros

        while True:
            for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    for i in range(4):  # Comprobamos qué botón pulsó.
                        if botones[i].collidepoint((mousex, mousey)):
                            self.button.play()
                            return i
            self.reloj.tick(FPS)

    def opcion(self, opt):
        # Realiza la opcion seleccionada en el menu por el usuario. El parametro opt es la opcion seleccionada.

        if opt == 6:  # Decide salir.
            exit()

        elif opt == 4:  # Decide comprobar las puntuaciones,
            fondo = pygame.image.load('Graficos\Records.png') # Pintamos el fondo
            botonSalir = Rect((594, 6), (36, 36)) # Botón de atrás
            self.pantalla.blit(fondo, fondo.get_rect())
            #Escribir los records
            tipos = ["FÁCIL", "INTERMEDIO", "DIFÍCIL", "CUADRADO", "ROMBO", "CASI DAMERO"]
            for i in range(len(self.puntuaciones)):
                punt_text = self.fuente.render(tipos[i], True, WHITE) # Imprimimos el tipo de partida a la izquierda
                pos = punt_text.get_rect()
                pos.topleft = (ANCHO/4, 115+i*43)
                self.pantalla.blit(punt_text, pos)
                punt_text = self.fuente.render("%s" % self.puntuaciones[i], True, WHITE) # Y a la derecha la puntuacion
                pos = punt_text.get_rect()
                pos.topright = (3*ANCHO/4, 115+i*43)
                self.pantalla.blit(punt_text, pos)
            pygame.display.update()

            salir = False
            while not salir:
                for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                    if event.type == QUIT:
                        exit()
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        if botonSalir.collidepoint((mousex, mousey)):
                            self.button.play()
                            salir = True
                self.reloj.tick(FPS)


        elif opt == 5:  # Decide borrar las puntuaciones
            f = open('highscores', 'w') # Abrimos el fichero con las puntuaciones
            for i in range(0, 3 + TABLEROS_PREFIJADOS): 
                f.write("0\n") # Escribimos 0's
            f.close()
            self.puntuaciones = []
            with open('highscores', 'r') as f:
                for l in f.readlines():
                    self.puntuaciones.append(int(l))

            # Retroalimentacion para el usuario, aparece y desaparece un tick al lado del botón borrar puntuaciones
            fondo = pygame.image.load('Graficos\Menu.png') # Cargamos las imágenes
            correcto = pygame.image.load('Graficos\Correcto.png').convert()
            pos = Rect((446, 358), (25, 24))
            for i in range(0, 256, 25):
                for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                    if event.type == QUIT:
                        exit()
                self.pantalla.blit(fondo, fondo.get_rect())
                correcto.set_alpha(i)
                self.pantalla.blit(correcto, pos)
                pygame.display.update()
                self.reloj.tick(FPS)
            for i in range(255, 0, -25):
                for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                    if event.type == QUIT:
                        exit()
                self.pantalla.blit(fondo, fondo.get_rect())
                correcto.set_alpha(i)
                self.pantalla.blit(correcto, pos)
                pygame.display.update()
                self.reloj.tick(FPS)

        else: # Ha seleccionado una opcion de jugar tablero
            tab = -1 # En caso de que quiera repetir un tablero fijo, guardaremos en esta variable su elección.
            while True:
                if opt == 3:  # Pide jugar un tablero fijo, por lo que se le muestra el menu de tablero y se comprueba que opcion devuelve:
                    if tab == -1:
                        tab = self.menuTablero()
                    if tab == 0:
                        break
                    else:
                        self.t = Tablero(4, tab)
                        self.maxpunt = self.puntuaciones[2 + tab]
                else:  # 0, 1 o 2
                    self.t = Tablero(opt + 1)
                    self.maxpunt = self.puntuaciones[self.t.dificultad - 1]

                self.puntuacion = 0 # Iniciamos la puntuación a 0 y bloques a 81
                self.bloquesRestantes = 81
                if self.partida() == False: # Comenzamos la partida con el tablero seleccionado. Devuelve si quiere continuar jugando
                    break # Rompemos el while True, saliendo al menu principal

    def pintarTablero(self):
        # Pinta el tablero por primera vez, animacion en la que van saliendo las bolas desde la esquina inferior
        circulo = [pygame.image.load('Graficos\circle%s.png' % i) for i in range(1, 6)]  # Cargamos los cinco colores
        fondo = pygame.image.load('Graficos\Partida.png') # Y dibujamos el fondo
        self.pantalla.blit(fondo, fondo.get_rect())
        self.pintarPuntuacion(False) # Pintamos la puntuación máxima y actual (0 presumiblemente)

        for i in range(1, 20):
            for j in range(1, 10):
                for k in range(1, 10):
                    if j + k == i:
                        if self.t.color_casilla(j, k) != 0: # Puede pasar que sea 0? quiza en otro juego
                            posicion = Rect(( 140 + 42 * (k - 1), 378 - 42 * (j - 1) ), (36, 36))
                            self.pantalla.blit(circulo[self.t.color_casilla(j, k) - 1], posicion)
            for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                if event.type == QUIT:
                    exit()
            pygame.display.update()
            self.reloj.tick(FPS)

    def pintarPuntuacion(self, actualizar):
        # Pinta en la pantalla a la derecha la puntuación máxima y actual del jugador.
        punt_text = self.fuente.render("%s" % self.puntuacion, True, BLACK) # Pintamos la puntuación .
        pos = punt_text.get_rect()
        pos.topright = (ANCHO - 20, 150)
        self.pantalla.blit(punt_text, pos)
        top_punt_text = self.fuente.render("%s" % self.maxpunt, True, BLACK)
        pos = top_punt_text.get_rect()
        pos.topright = (ANCHO - 20, 115)
        self.pantalla.blit(top_punt_text, pos)
        if actualizar:
            pygame.display.update()

    def partida(self):
        # Implementacion de la logica del juego. Al terminar en modo normal se le pregunta al usuario si desea jugar
        # otra partida en las mismas condiciones. Devuelve False si la partida se suspendio a la mitad o si el usuario
        # decide dejar de jugar. Devuelve True si el usuario quiere jugar otra partida igual.

        self.pintarTablero()

        # La partida termina cuando no quedan bloques que seleccionar.
        while ( self.t.quedan_bloques()):
            self.refrescar_pantalla()

            # Bucle para esperar que el usuario pinche en la pantalla
            seleccion = False
            mousex, mousey = (0, 0)
            while not seleccion:
                for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                    if event.type == QUIT:
                        exit()
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        seleccion = True
                self.reloj.tick(FPS)

            #Si le ha dado a salir, volvemos al menu principal
            if (Rect((594, 6), (36, 36)).collidepoint(mousex, mousey)):
                self.button.play()
                return False
            #En otro caso, traducimos el click a fila-columna seleccionada:
            for i in range(1, 10):
                for j in range(1, 10):
                    if Rect((140 + 42 * (j - 1), 378 - 42 * (i - 1)), (36, 36)).collidepoint(mousex, mousey):
                        # Ha seleccionado la casilla i , j. Puede ser que no forme bloque o que fuera casilla vacía.
                        if (self.t.forma_bloque(i, j)):
                            self.pop.play()

                            # Ralizamos la jugada del bloque tocado. 
                            self.old_t = copy.deepcopy(self.t) # Copiamos el tablero antes de ser tocado
                            bloques = self.t.tocar_bloque(i, j)
                            self.refrescar_tras_tocar_bloque() # Animacion de desaparicion de bloques tocados

                            self.bloquesRestantes -= bloques # Actualizamos los bloques restantes y la puntuacion
                            self.puntuacion += bloques * bloques * 5

                            self.old_t = copy.deepcopy(self.t) # Copiamos el tablero antes de que las bolas caigan
                            self.t.gravedad_filas()
                            self.refrescar_gravedad_filas() # Animacion de bolas cayendo dentro de su columna

                            self.old_t = copy.deepcopy(self.t) # Copiamos el tablero antes de que las columnas se desplazen
                            self.t.gravedad_columnas()
                            self.refrescar_gravedad_columnas() # Animacion en que las columnas se desplazan hacia la izquierda

                        elif ( self.t.color_casilla(i, j) != 0):
                            self.wrong.play()


        # Sumamos el bonus por haber despejado gran parte del tablero, y si se superó la puntuacion maxima se actualiza
        # el fichero de puntuaciones.
        if self.bloquesRestantes < 15:
            self.puntuacion += 2000 - self.bloquesRestantes * self.bloquesRestantes * 10

        if self.puntuacion > self.maxpunt:
            if self.t.dificultad < 4:
                self.puntuaciones[self.t.dificultad - 1] = self.puntuacion
            else:
                self.puntuaciones[2 + self.t.tipo] = self.puntuacion
            f = open('highscores', 'w')
            for punt in self.puntuaciones:
                f.write(str(punt) + "\n")
            f.close()

        # Mostramos por ultima vez el tablero final y preguntamos si quiere jugar de nuevo
        self.refrescar_pantalla()

        mens = pygame.image.load('Graficos\Mensaje.png').convert()
        si = pygame.image.load('Graficos\Si.png').convert()
        no = pygame.image.load('Graficos\No.png').convert()
        mens.set_colorkey((0, 0, 0))
        mens.set_alpha(255)
        si.set_colorkey((0, 0, 0))
        si.set_alpha(255)
        no.set_colorkey((0, 0, 0))
        no.set_alpha(255)
        posmens = mens.get_rect()
        posmens.center = (ANCHO / 2, ALTO / 3)
        possi = si.get_rect()
        possi.center = (ANCHO / 2 - 40, ALTO / 3 + 40)
        posno = no.get_rect()
        posno.center = (ANCHO / 2 + 40, ALTO / 3 + 40)
        self.pantalla.blit(mens, posmens)
        self.pantalla.blit(si, possi)
        self.pantalla.blit(no, posno)
        pygame.display.update()

        seleccion = False
        while not seleccion:
            for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEBUTTONUP:
                    if possi.collidepoint(event.pos):
                        return True
                    if posno.collidepoint(event.pos):
                        return False
                    if (Rect((594, 6), (36, 36)).collidepoint(mousex, mousey)):
                        return False
            self.reloj.tick(FPS)

    def refrescar_tras_tocar_bloque(self):
        # Animacion de las bolas que han sido tocadas, desaparecen haciendose cada vez mas pequeñas.
        # En self.old_t está el tablero con las bolas antes de ser tocado, y en self.t están las bolas
        # tras haber tocado un bloque.

        circulo = [pygame.image.load('Graficos\circle%s.png' % i) for i in range(1, 6)]  # Cargamos los cinco colores

        #Graficos estáticos:
        fondo = pygame.image.load('Graficos\Partida.png')
        punt_text = self.fuente.render("%s" % self.puntuacion, True, BLACK)
        pos = punt_text.get_rect()
        pos.topright = (ANCHO - 20, 150)
        top_punt_text = self.fuente.render("%s" % self.maxpunt, True, BLACK)
        pos2 = top_punt_text.get_rect()
        pos2.topright = (ANCHO - 20, 115)

        # EL tamaño de un circulo es 36x36 y (36-6*j)x(36-6*j)
        for j in range(36,0,-6):
            circulos_desaparecen = [];
            for i in range(5):
                circulos_desaparecen.append(pygame.transform.scale(circulo[i], (j,j)))  # Los hacemos de tamaño mas pequeño progresivamente

            self.pantalla.blit(fondo, fondo.get_rect())
            self.pantalla.blit(punt_text, pos)
            self.pantalla.blit(top_punt_text, pos2)
            for columna in range(1,10):
                for fila in range(1,10):
                    if self.old_t.color_casilla(fila,columna) != self.t.color_casilla(fila,columna): # La bola se ha tocado esta vez
                        posicion = Rect(( 140 + 42 * (columna - 1) +(36-j)/2, 378 - 42 * (fila - 1)+(36-j)/2), (j, j))
                        self.pantalla.blit(circulos_desaparecen[self.old_t.color_casilla(fila, columna) - 1], posicion)
                    elif self.old_t.color_casilla(fila,columna) != 0: # La bola no se ha tocado esta vez
                        posicion = Rect(( 140 + 42 * (columna - 1), 378 - 42 * (fila - 1)), (36, 36))
                        self.pantalla.blit(circulo[self.old_t.color_casilla(fila, columna) - 1], posicion)
            pygame.display.update()
            self.reloj.tick(FPS)
            for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
              if event.type == QUIT:
                exit()

    def refrescar_gravedad_filas(self):
        # Desplaza las columnas hacia la izquierda en caso de que se generen columnas vacias.
        # En self.old.t está el tablero con las columnas antes de ser desplazadas


        # Vamos a añadir en un array de vectores pares (i,j) indicando que la casilla i,j ha de desplazarse x posiciones,
        # donde x es el vector al que pertenece.
        gravedad = [[] for i in range(9)] # la caida mas grande es de 8, la minima de 0 (quedarse en el sitio)

        #Estudiamos por columnas:
        for columna in range(1,10):
          caer = 0
          for fila in range(1,10):
            if self.old_t.color_casilla(fila,columna) == 0:
              caer+=1
            else:
              gravedad[caer].append([fila,columna])

        #Vemos el bloque que mas a la izquierda se desplaza, que es el que dictará los tiempos:
        max = 0
        for i in range(9):
          if len(gravedad[i])> 0:
            max = i

        circulo = [pygame.image.load('Graficos\circle%s.png' % i) for i in range(1, 6)]  # Cargamos los cinco colores

        #Graficos estáticos:
        fondo = pygame.image.load('Graficos\Partida.png')
        punt_text = self.fuente.render("%s" % self.puntuacion, True, BLACK)
        pos = punt_text.get_rect()
        pos.topright = (ANCHO - 20, 150)
        top_punt_text = self.fuente.render("%s" % self.maxpunt, True, BLACK)
        pos2 = top_punt_text.get_rect()
        pos2.topright = (ANCHO - 20, 115)

        for i in range(max+1):
          for j in range(0,42,15):
            self.pantalla.blit(fondo, fondo.get_rect())
            self.pantalla.blit(punt_text, pos)
            self.pantalla.blit(top_punt_text, pos2)
            for k in range(max+1):
              if k > i: # Si k < i ya está en su posicion
                for casilla in gravedad[k]:
                  posicion = Rect(( 140 + 42 * (casilla[1] - 1), 378 - 42 * (casilla[0] - 1 - i) + j), (36, 36))
                  self.pantalla.blit(circulo[self.old_t.color_casilla(casilla[0], casilla[1]) - 1], posicion)
              else:
                for casilla in gravedad[k]:
                  posicion = Rect(( 140 + 42 * (casilla[1] - 1), 378 - 42 * (casilla[0] - 1 - k) ), (36, 36))
                  self.pantalla.blit(circulo[self.old_t.color_casilla(casilla[0], casilla[1]) - 1], posicion)
            pygame.display.update()
            self.reloj.tick(FPS)
            for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
              if event.type == QUIT:
                exit()

    def refrescar_gravedad_columnas(self):
        # Hace caer las bolas hacia la posicion que le corresponde dentro de su columna (gravedad hacia abajo).
        # en self.old.t está el tablero con los huecos en el suelo.

        # Vamos a añadir en un array de vectores pares (i,j) indicando que la casilla i,j ha de caer x posiciones,
        # donde x es el vector al que pertenece.
        gravedad = [[] for i in range(9)] # la caida mas grande es de 8, la minima de 0 (quedarse en el sitio)

        #Estudiamos por columnas, comprobamos si la columna está vacía:
        caer = 0
        for columna in range(1,10):
          vacia = 0
          for fila in range(1,10):
            vacia+=self.old_t.color_casilla(fila,columna)
          if vacia == 0:
            caer+=1
          else:
            for fila in range(1,10):
              if self.old_t.color_casilla(fila,columna) != 0:
                gravedad[caer].append([fila,columna])

        #Vemos el bloque que mas bajo ha caido, que es el que dictará los tiempos:
        max = 0
        for i in range(9):
          if len(gravedad[i])> 0:
            max = i

        circulo = [pygame.image.load('Graficos\circle%s.png' % i) for i in range(1, 6)]  # Cargamos los cinco colores

        #Graficos estáticos:
        fondo = pygame.image.load('Graficos\Partida.png')
        punt_text = self.fuente.render("%s" % self.puntuacion, True, BLACK)
        pos = punt_text.get_rect()
        pos.topright = (ANCHO - 20, 150)
        top_punt_text = self.fuente.render("%s" % self.maxpunt, True, BLACK)
        pos2 = top_punt_text.get_rect()
        pos2.topright = (ANCHO - 20, 115)

        for i in range(max+1):
          for j in range(0,42,15):
            self.pantalla.blit(fondo, fondo.get_rect())
            self.pantalla.blit(punt_text, pos)
            self.pantalla.blit(top_punt_text, pos2)
            for k in range(max+1):
              if k > i: # Si k < i ya está en su posicion
                for casilla in gravedad[k]:
                  posicion = Rect(( 140 + 42 * (casilla[1] - 1 - i) -j, 378 - 42 * (casilla[0] - 1)), (36, 36))
                  self.pantalla.blit(circulo[self.old_t.color_casilla(casilla[0], casilla[1]) - 1], posicion)
              else:
                for casilla in gravedad[k]:
                  posicion = Rect(( 140 + 42 * (casilla[1] - 1 - k), 378 - 42 * (casilla[0] - 1) ), (36, 36))
                  self.pantalla.blit(circulo[self.old_t.color_casilla(casilla[0], casilla[1]) - 1], posicion)
            pygame.display.update()
            self.reloj.tick(FPS)
            for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
              if event.type == QUIT:
                exit()

    def refrescar_pantalla(self):
        # Actualiza la pantalla, mostrando el estado actual del tablero y la puntuacion de la
        # partida, asi como la puntuacion maxima obtenida en partidas previas.
        fondo = pygame.image.load('Graficos\Partida.png')
        circulo = [pygame.image.load('Graficos\circle%s.png' % i) for i in range(1, 6)]  # Cargamos los cinco colores
        self.pantalla.blit(fondo, fondo.get_rect())

        self.pintarPuntuacion(False)

        for i in range(1, 10):
            bloques = self.t.get_fila(i)
            for j in range(9):
                if bloques[j] != 0: # Dibuja cada bola en su sitio
                    posicion = Rect((140 + 42 * j, 378 - 42 * (i - 1)), (36, 36))
                    self.pantalla.blit(circulo[bloques[j] - 1], posicion)
        pygame.display.update()


    def pauseMessage(self, s):
        #DEBUG
        mensaje = self.fuente.render(s, True, BLACK, BLACK)
        rect = mensaje.get_rect()
        rect.center = (ANCHO / 2, ALTO * 2 / 3)
        pygame.draw.rect(self.pantalla, BLACK, Rect((0, 0), (ANCHO, ALTO)))
        self.pantalla.blit(mensaje, rect)
        while True:
            for event in pygame.event.get():  # Bucle de control de eventos, buscamos clicks de raton
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEBUTTONUP:
                    pygame.draw.rect(self.pantalla, BLACK, Rect((0, 0), (ANCHO, ALTO)))
                    return True
            self.reloj.tick(FPS)
            pygame.display.update()