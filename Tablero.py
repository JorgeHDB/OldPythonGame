__author__      = "Jorge Hernandez de Benito"

from types import IntType
from random import randint
import TablerosFijos

class Tablero:
  # Objeto que implementa el tablero de un juego Rompebolas. Posee una matriz 9x9 de bolas de distintos colores que pueden
  # ser tocados para ir despejando el tablero.

  def __init__(self, dificultad, fijado=0):
    assert type(dificultad) is IntType # Dificultad ha de ser numerico
    assert type(fijado) is IntType # Fijado igual
    assert dificultad > 0 and dificultad < 5 # Solo se puede crear con dificultad entre 1 y 4
    assert not( dificultad == 4 and (fijado < 1 or fijado > TablerosFijos.TABLEROS_PREFIJADOS) ) # Solo hay 3 tableros prefijados

    self.dificultad = dificultad
    self.tipo = fijado
    if dificultad < 4:
      self.tablero = [[randint(1,2+dificultad) for x in range(9)] for x in range(9)] # 3, 4 o 5 colores distintos.
    else:
      self.tablero= TablerosFijos.tableroFijo(fijado)

  def color_casilla(self,x,y):
    # Devuelve el color de la bola situada en la casilla (x,y). Los parametros x e y son la fila y columna de la casilla,
    # respectivamente.

    assert x>0 and x<10 and y>0 and y < 10
    assert type(x) is IntType
    assert type(y) is IntType

    return self.tablero[9-x][y-1]

  def vaciar_casilla(self,x,y):
    # Elimina del tablero la bola situada en la casilla (x,y). Los parametros x e y son la fila y columna de la casilla,
    # respectivamente.

    assert x>0 and x<10 and y>0 and y < 10
    assert type(x) is IntType
    assert type(y) is IntType

    self.tablero[9-x][y-1]=0

  def adyacentes(self,x,y):
    # Devuelve las casillas adyacentes a la casilla (x,y). Los parametros x e y son la fila y columna de la casilla,
    # respectivamente.

    assert x>0 and x<10 and y>0 and y < 10
    assert type(x) is IntType
    assert type(y) is IntType

    ady=[]
    if(x!=9):
      ady.append([x+1,y])
    if(x!=1):
      ady.append([x-1,y])
    if(y!=9):
      ady.append([x,y+1])
    if(y!=1):
      ady.append([x,y-1])
    return ady

  def forma_bloque(self,x,y):
    # Comprueba si en la casilla (x,y) hay una bola que forma parte de un bloque. Devuelve True en caso afirmativo,
    # y False si no hay bola o la bola no forma parte de un bloque. Los parametros x e y son la fila y columna
    # de la casilla, respectivamente.

    color=self.color_casilla(x,y)
    if color == 0:
      return False
    for t in self.adyacentes(x,y):
      if color == self.color_casilla(t[0],t[1]):
        return True
    return False

  def tocar_bloque(self,x,y):
    # Elimina el bloque formado por la casilla (x,y). Los parametros x e y son la fila y columna
    # de la casilla, respectivamente. Devuelve el numero de bolas que formaban el bloque tocado.

    assert x>0 and x<10 and y>0 and y < 10
    assert type(x) is IntType
    assert type(y) is IntType

    bloques = 1
    color = self.color_casilla(x,y)
    self.vaciar_casilla(x,y)
    for t in self.adyacentes(x,y):
      if color == self.color_casilla(t[0],t[1]):
        bloques+=self.tocar_bloque(t[0],t[1])
    return bloques

  def gravedad_filas(self):
    # Las bolas del tablero caen hacia abajo hasta tener una bola por debajo que las sustente.

    # Extraemos las columnas
    columnas = [[row[i] for row in self.tablero] for i in range(9)]
    for col in columnas:
       for i in range(1,9):
         if(col[i]==0): # Si una casilla no tiene bola, rellenamos el hueco formado.
           col[1:(i+1)]=col[0:i]
           col[0]=0 # El hueco ahora esta arriba en la columna

    # Transponemos de nuevo las columnas para obtener el tablero por filas.
    self.tablero = [[row[i] for row in columnas] for i in range(9)]

  def gravedad_columnas(self):
    # Si una columna esta vacia, todas las columas a su derecha se mueven hacia la izquierda del tablero.

    columnas = [[row[i] for row in self.tablero] for i in range(9)]
    for i in range(8,-1,-1): #Trabajamos por columnas, desde la penultima hasta la primera.
      col = columnas[i][:]
      if sum(col)==0: # Suman 0 cuando no hay ninguna bola en dicha columna.
        for j in range(i,8): # Desplazamos las columnas a su derecha.
          columnas[j][:]=columnas[j+1][:]
        columnas[8][:]=[0 for k in range(9)] # La ultima columna queda vacia entonces.

    # Transponemos de nuevo las columnas para obtener el tablero por filas.
    self.tablero = [[row[i] for row in columnas] for i in range(9)]

  def quedan_bloques(self):
  # Comprobacion de si quedan bloques en el tablero (dos o mas bolas adyacentes del mismo color).
  # Devuelve true si se puede seguir jugando y false si la partida esta acabada.
  
    for i in range(9,0,-1): # Comenzamos por la fila de abajo pues es donde se concentran las bolas.
      for j in range(1,10):
        if self.forma_bloque(i,j):
          return True
    return False

  def get_fila(self,n):
    # Devuelve una lista con los elementos de la fila pedida, util para imprimir el tablero por filas.

    assert n>0 and n<10
    assert type(n) is IntType
    return self.tablero[(9-n)][:]