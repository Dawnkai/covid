import tkinter as tk
from random import randint


class Atom:
    def __init__(self, promien, n,v):
        self.masa = 1
        self.promien = promien
        self.srodek = [randint(promien, (n - 2) * promien), randint(promien, (n - 2) * promien)]
        self.rozmiar = [self.srodek[0] - promien, self.srodek[1] - promien, self.srodek[0] + promien,
                        self.srodek[1] + promien]
        self.predkosc = [randint(-v, v), randint(-v, v)]


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
        self.canvas = tk.Canvas(self.master, height=self.n * self.r, width=self.n * self.r, bg="white")
        self.canvas.grid(row=4, columnspan=2)
        self._generate_atoms()
        self._movement()

    def _generate_atoms(self):
        for i in range(self.n):
            atom = Atom(self.r, self.n, self.v)
            self.atoms.append({"attributes": atom, "instance": self.canvas.create_oval(atom.rozmiar, fill="blue")})

    def _close_window(self):
        self.master.destroy()

    def _close_canva(self):
        self.canvas.destroy()

    def _movement(self):
        for i in range(self.n):
            self.canvas.move(self.atoms[i]["instance"], self.atoms[i]["attributes"].predkosc[0], self.atoms[i]["attributes"].predkosc[1])
        self.canvas.after(1000, self._movement)

app = App()
app.master.title("Atom collisions")
app.mainloop()