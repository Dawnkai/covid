import tkinter as tk
from random import randint

class Atom:
  def __init__(self, promien, n, predkosc):
    self.masa = 1
    self.promien = promien
    self.polozenie = [randint(promien, (n-2) * promien), randint(promien, (n-2) * promien)]
    self.predkosc = [randint(-predkosc,predkosc),randint(-predkosc,predkosc)]

root = tk.Tk()
class App(tk.Frame):
    def __init__(self,n,r,master=None):
        super().__init__(master)
        self.configure(master,width=n*r, height =n*r)
        self.canvas = tk.Canvas(master,width = n*r, height = n*r)
        self.oval = self.canvas.create_oval(4,596-2*r,4+2*r,596, fill = "red")
        self.atoms=[]
        self.ovals=[]
        self.ov =[]
        for i in range (n):
            self.atoms.append(Atom(r,n,5))
            self.ovals.append([self.atoms[i].polozenie[0]-r,self.atoms[i].polozenie[1]-r,self.atoms[i].polozenie[0]+r,self.atoms[i].polozenie[1]+r])
            self.ov.append(self.canvas.create_oval(self.ovals[i],fill = "blue"))
        self.canvas.pack()

        self.movement()
    def movement(self):

        for i in range(n):
            self.wall(i)
            self.canvas.move(self.ov[i],self.atoms[i].predkosc[0],self.atoms[i].predkosc[1])
        self.canvas.after(100,self.movement)


    def wall(self,i):
        if self.atoms[i].polozenie[0]-r < 1 or self.atoms[i].polozenie[0]+r >= (n-1)*r:
            self.atoms[i].predkosc[0] = -self.atoms[i].predkosc[0]
        if self.atoms[i].polozenie[1]-r < 1 or self.atoms[i].polozenie[1]+r >= (n-1)*r:
            self.atoms[i].predkosc[1] = -self.atoms[i].predkosc[1]


n = 100
r = 6

app = App(n,r)
app.master.title("Zderzenia")
app.master.maxsize(n*r,n*r)
app.master.minsize(n*r,n*r)
app.mainloop()