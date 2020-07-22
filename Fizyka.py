from enum import Enum
from random import randint

class Stan(Enum):
  ZDROWY = 1
  ZARAZONY = 2

class Kierunki(Enum):
  DOL = 1
  DOL_LEWO = 2
  DOL_PRAWO = 3
  GORA = 4
  GORA_LEWO = 5
  GORA_PRAWO = 6
  LEWO = 7
  PRAWO = 8
  STOP = 9

class Atom:
  def __init__(promien, n, predkosc):
    self.masa = 1
    self.promien = promien
    self.polozenie = [randint(0, n * promien), randint(0, n * promien)]
    self.predkosc = predkosc
    self.wektor = (self.predkosc[0] ** 2) + (self.predkosc[1] ** 2)
    self.stan = Stan.ZDROWY

  def _get_kierunek(self):

    if self.predkosc[0] < 0:
      if self.predkosc[1] < 0:
        return Kierunek.DOL_LEWO
      if self.predkosc[1] > 0:
        return Kierunek.GORA_LEWO
      return Kierunek.LEWO

    if self.predkosc[0] > 0:
      if self.predkosc[1] < 0:
        return Kierunek.DOL_PRAWO
      if self.predkosc[1] > 0:
        return Kierunek.GORA_PRAWO
      return Kierunek.PRAWO

    if self.predkosc[1] > 0:
      return Kierunek.GORA
    if self.predkosc[1] < 0:
      return Kierunek.DOL
    return STOP

class Zbiornik:
  def __init__(liczba_atomow, promien, n):
    self.atomy = [ Atom(promien) for x in range(0, liczba_atomow) ]
    self.h = n * promien
    self.l = n * promien

if __name__ == 'main':
  v = 5
  promien = 2
  n = 30
  atom_pierwotny = Atom(promien, n, [randint(1, v), randint(1, v)])
  atom_pierwotny.stan = Stan.ZARAZONY
  atom_pierwotny.polozenie = [0, 0]