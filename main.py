import tkinter as tk
from random import randint

class Atom:
  def __init__(self, promien, n):
    self.masa = 1
    self.promien = promien
    self.srodek = [randint(promien, (n-2) * promien), randint(promien, (n-2) * promien)]
    self.rozmiar = [self.srodek[0] - promien, self.srodek[1] - promien, self.srodek[0] + promien, self.srodek[1] + promien]


root = tk.Tk()
class App(tk.Frame):
    def __init__(self):
        self.master = None
        super().__init__(self.master)
        self.n = 0
        self.r = 0

        self.AtomNumLabel = tk.Label(self.master, text="Liczba atomów", font=10)
        self.AtomNumLabel.grid(row=0)
        self.AtomNumInput = tk.Entry(self.master)
        self.AtomNumInput.grid(row=0, column=1)

        self.AtomRadLabel = tk.Label(self.master, text="Promień atomu", font=10)
        self.AtomRadLabel.grid(row=1)
        self.AtomRadInput = tk.Entry(self.master)
        self.AtomRadInput.grid(row=1, column=1)

        self.StartButton = tk.Button(self.master, text="Start", command=self._generate_cavas)
        self.StartButton.grid(row=2, column=1)

        self.canvas = None
        self.atoms = []


    def _generate_cavas(self):
        self.n = int(self.AtomNumInput.get())
        self.r = int(self.AtomRadInput.get())
        self.canvas = tk.Canvas(self.master, height=self.n * self.r, width=self.n * self.r, bg="white")
        self.canvas.grid(row=3, columnspan=2)
        self._generate_atoms()
    

    def _generate_atoms(self):
        for i in range(self.n):
            atom = Atom(self.r, self.n)
            self.atoms.append({"attributes": atom, "instance": self.canvas.create_oval(atom.rozmiar, fill="blue")})


app = App()
app.master.title("Atom collisions")
app.mainloop()