mport tkinter as tk
from random import randint

class Atom:
    def __init__(self, promien, n,v):
        self.masa = 1
        self.promien = promien
        self.center = [randint(promien, (n-2) * promien), randint(promien, (n-2) * promien)]
        self.diameter = [self.center[0] - promien, self.center[1] - promien, self.center[0] + promien, self.center[1] + promien]

class App(tk.Frame):
    def __init__(self):
        self.master = None
        super().__init__(),
        self.n = 0
        self.r = 0
        self.v = 0
        self.ovals=[]

        self.AtomNumLabel = tk.Label(self.master, text="Liczba atomów", font=10)
        self.AtomNumLabel.grid(row=0)
        self.AtomNumInput = tk.Entry(self.master)
        self.AtomNumInput.grid(row=0, column=1)

        self.AtomRadLabel = tk.Label(self.master, text="Promień atomu", font=10)
        self.AtomRadLabel.grid(row=1)
        self.AtomRadInput = tk.Entry(self.master)
        self.AtomRadInput.grid(row=1, column=1)

        self.AtomSpeedLabel = tk.Label(self.master, text="Predkosci atomow", font=10)
        self.AtomSpeedLabel.grid(row=2)
        self.AtomSpeedInput = tk.Entry(self.master)
        self.AtomSpeedInput.grid(row=2, column=1)

        self.StartButton = tk.Button(self.master,
                                     text="Start",
                                     command=self._generate_canvas)
        self.StartButton.grid(row=3, column=1)

        self.canvas = None

        self.QuitButton = tk.Button(self.master,
                                text="Quit",
                                command=self._close_window)
        self.QuitButton.grid(row=5, column=1)

    def _close_window(self):
        self.master.destroy()

    def _generate_canvas(self):
      self.n = int(self.AtomNumInput.get())
      self.r = int(self.AtomRadInput.get())
      self.v = int(self.AtomSpeedInput.get())
      self.canvas = tk.Canvas(self.master,
                              height=self.n*self.r,
                              width=self.n*self.r,
                              bg="white")
      for i in range(self.n):
          atom = Atom(self.r, self.n, self.v)
          self.ovals.append([atom, self.canvas.create_oval(atom.diameter, fill="blue")])
      self.canvas.grid(row=4, columnspan=2)

app = App()
app.master.title("Zderzenia")
app.mainloop()