__author__      = "Jorge Hernandez de Benito"

from types import IntType
from random import randint

#CONSTANTES
TABLEROS_PREFIJADOS = 3

def tableroFijo(opcion):
  # Devuelve el tablero fijo solicitado.
  # Tableros actuales: 1 -> Cuadrado tres colores.
  #                    2 -> Rombo cuatro colores.
  #                    3 -> Casi damero.

  assert type(opcion) is IntType # Fijado igual
  assert opcion > 0 and opcion <= TABLEROS_PREFIJADOS # Solo se puede crear con dificultad entre 1 y 4

  if opcion == 1:
    return [[1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,1],
            [1,2,3,3,3,3,3,2,1],
            [1,2,3,1,1,1,3,2,1],
            [1,2,3,1,2,1,3,2,1],
            [1,2,3,1,1,1,3,2,1],
            [1,2,3,3,3,3,3,2,1],
            [1,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1]]
  if opcion == 2:
    return [[4,4,4,4,1,4,4,4,4],
            [4,4,4,1,2,1,4,4,4],
            [4,4,1,2,3,2,1,4,4],
            [4,1,2,3,1,3,2,1,4],
            [1,2,3,1,2,1,3,2,1],
            [4,1,2,3,1,3,2,1,4],
            [4,4,1,2,3,2,1,4,4],
            [4,4,4,1,2,1,4,4,4],
            [4,4,4,4,1,4,4,4,4]]
  if opcion == 3:
    casiDamero = [[(x+y)%2+1 for x in range(9)] for y in range(9)]
    x = randint(0, 8)
    y = randint(0, 8)
    casiDamero[x][y] = (casiDamero[x][y]%2)+1
    return casiDamero


