import tkinter as tk
from random import randint
from enum import Enum


class Kierunek(Enum):
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
    def __init__(self, promien, n, v):
        self.masa = 1
        self.promien = promien
        self.srodek = [randint(promien, (n - 2) * promien), randint(promien, (n - 2) * promien)]
        self.rozmiar = [self.srodek[0] - promien, self.srodek[1] - promien, self.srodek[0] + promien,
                        self.srodek[1] + promien]
        self.predkosc = [randint(-v, v), randint(-v, v)]
        self.kierunek = self._get_kierunek()

    def _get_kierunek(self):

        if self.predkosc[0] < 0:
            if self.predkosc[1] < 0:
                return Kierunek.GORA_LEWO
            if self.predkosc[1] > 0:
                return Kierunek.DOL_LEWO
            return Kierunek.LEWO

        if self.predkosc[0] > 0:
            if self.predkosc[1] < 0:
                return Kierunek.GORA_PRAWO
            if self.predkosc[1] > 0:
                return Kierunek.DOL_PRAWO
            return Kierunek.PRAWO

        if self.predkosc[1] > 0:
            return Kierunek.DOL
        if self.predkosc[1] < 0:
            return Kierunek.GORA
        return STOP


root = tk.Tk()


class App(tk.Frame):
    def __init__(self):
        self.master = None
        super().__init__(self.master)
        self.n = 0
        self.r = 0
        self.v = 0

        self.AtomNumLabel = tk.Label(self.master, text="Liczba atomów", font=10)
        self.AtomNumLabel.grid(row=0)
        self.AtomNumInput = tk.Entry(self.master)
        self.AtomNumInput.grid(row=0, column=1)

        self.AtomRadLabel = tk.Label(self.master, text="Promień atomu", font=10)
        self.AtomRadLabel.grid(row=1)
        self.AtomRadInput = tk.Entry(self.master)
        self.AtomRadInput.grid(row=1, column=1)

        self.AtomSpeedLabel = tk.Label(self.master, text="Predkosc atomu", font=10)
        self.AtomSpeedLabel.grid(row=2)
        self.AtomSpeedInput = tk.Entry(self.master)
        self.AtomSpeedInput.grid(row=2, column=1)

        self.StartButton = tk.Button(self.master, text="Start", command=self._generate_cavas)
        self.StartButton.grid(row=3)

        self.StopButton = tk.Button(self.master, text="Stop", command=self._close_canva)
        self.StopButton.grid(row=3, column=1)

        self.QuitButton = tk.Button(self.master, text="Zamknij", command=self._close_window)
        self.QuitButton.grid(row=5, columnspan=2)

        self.canvas = None
        self.atoms = []

    def _generate_cavas(self):
        self.n = int(self.AtomNumInput.get())
        self.r = int(self.AtomRadInput.get())
        self.v = int(self.AtomSpeedInput.get())
        if self.n * self.r < 600:
            self.canvas = tk.Canvas(self.master, height=self.n * self.r, width=self.n * self.r + 10, bg="white",
                                    relief="groove", bd=5)
            self.canvas.grid(row=4, columnspan=2, padx=(4, 4))
            self._generate_atoms()
            self._movement()
        else:
            self._error_tag()

    def _generate_atoms(self):
        for i in range(self.n):
            atom = Atom(self.r, self.n, self.v)
            self.atoms.append({"attributes": atom, "instance": self.canvas.create_oval(atom.rozmiar, fill="blue")})

    def _close_window(self):
        self.master.destroy()

    def _close_canva(self):
        self.canvas.destroy()

    def _error_tag(self):
        self.Tag = tk.Label(self.master, text="Zmniejsz liczbe atomow lub promien", fg="red", font=5)
        self.Tag.grid(row=4, columnspan=2)
        self.Tag.after(5000, self._close_tag)

    def _close_tag(self):
        self.Tag.destroy()

    def _movement(self):
        self._wall()
        for i in range(self.n):
            self.canvas.move(self.atoms[i]["instance"], self.atoms[i]["attributes"].predkosc[0],
                             self.atoms[i]["attributes"].predkosc[1])
            self.atoms[i]["attributes"].srodek[0] = self.atoms[i]["attributes"].srodek[0]+self.atoms[i]["attributes"].predkosc[0]
            self.atoms[i]["attributes"].srodek[1] = self.atoms[i]["attributes"].srodek[1] + self.atoms[i]["attributes"].predkosc[1]
            self.atoms[i]["attributes"].rozmiar[0] = self.atoms[i]["attributes"].rozmiar[0] + self.atoms[i]["attributes"].predkosc[0]
            self.atoms[i]["attributes"].rozmiar[2] = self.atoms[i]["attributes"].rozmiar[2] + self.atoms[i]["attributes"].predkosc[0]
            self.atoms[i]["attributes"].rozmiar[1] = self.atoms[i]["attributes"].rozmiar[1] + self.atoms[i]["attributes"].predkosc[1]
            self.atoms[i]["attributes"].rozmiar[3] = self.atoms[i]["attributes"].rozmiar[3] + self.atoms[i]["attributes"].predkosc[1]
            self.atoms[i]["attributes"].kierunek = self.atoms[i]["attributes"]._get_kierunek()
        self.canvas.after(1000, self._movement)

    def _wall(self):
        for i in range(self.n):
            z = max(abs(self.atoms[i]["attributes"].predkosc[0]), abs(self.atoms[i]["attributes"].predkosc[1]), self.atoms[i]["attributes"].promien)
            if self.atoms[i]["attributes"].rozmiar[0] - self.r <= z and (Kierunek.DOL_LEWO or Kierunek.GORA_LEWO or Kierunek.LEWO):
                self.atoms[i]["attributes"].predkosc[0] *= -1
                print(self.atoms[5]["attributes"].kierunek)
            if self.atoms[i]["attributes"].rozmiar[2] + self.r >= self.r * self.n-z and (Kierunek.GORA_PRAWO or Kierunek.DOL_PRAWO or Kierunek.PRAWO):
                self.atoms[i]["attributes"].predkosc[0] *= -1
            if self.atoms[i]["attributes"].rozmiar[1] - self.r <= z and (Kierunek.GORA or Kierunek.GORA_LEWO or Kierunek.GORA_PRAWO):
                self.atoms[i]["attributes"].predkosc[1] *= -1
            if self.atoms[i]["attributes"].rozmiar[3] + self.r >= self.r * self.n - z and (Kierunek.DOL_LEWO or Kierunek.DOL_PRAWO or Kierunek.DOL):
                self.atoms[i]["attributes"].predkosc[1] *= -1


app = App()
app.master.title("Atom collisions")
app.master.maxsize(640, 750)
app.mainloop()