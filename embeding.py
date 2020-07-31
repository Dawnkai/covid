import tkinter as tk
import os
import pygame as game
import random
import math
from settings import LOGO_IMAGE, BACKGROUND_IMAGE, CONTAINER_SIZE
from enum import Enum

class App(tk.Frame):
    """ Main interface GUI tkinter"""
    def __init__(self):
        self.master = None
        super().__init__(),
        self.n = 0
        self.r = 0
        self.v = 0

        # entering atom numbers
        self.AtomNumLabel = tk.Label(self.master, text="Liczba atomów", font=10)
        self.AtomNumLabel.grid(row=0)
        self.AtomNumInput = tk.Entry(self.master)
        self.AtomNumInput.grid(row=0, column=1)

        # entering atom radius
        self.AtomRadLabel = tk.Label(self.master, text="Promień atomu", font=10)
        self.AtomRadLabel.grid(row=1)
        self.AtomRadInput = tk.Entry(self.master)
        self.AtomRadInput.grid(row=1, column=1)

        # entering atom speed
        self.AtomSpeedLabel = tk.Label(self.master, text="Predkosci atomow", font=10)
        self.AtomSpeedLabel.grid(row=2)
        self.AtomSpeedInput = tk.Entry(self.master)
        self.AtomSpeedInput.grid(row=2, column=1)

        # start button
        self.StartButton = tk.Button(self.master,
                                     text="Start",
                                     command=self._generate_frame)
        self.StartButton.grid(row=3)

        #stop button
        self.StopButton = tk.Button(self.master,
                                     text="Stop",
                                     command=self._close_frame)
        self.StopButton.grid(row=3, column=1)

        self.frame = None
        self.app1 = None

        #quit button
        self.QuitButton = tk.Button(self.master,
                                    text="Quit",
                                    command=self._close_window)
        self.QuitButton.grid(row=5, column=1)

    # closing application
    def _close_window(self):
        self.app1.running = False
        self.master.destroy()

    # closing\breaking animation and destroying frame
    def _close_frame(self):
        self.app1.running = False
        game.quit()
        self.frame.destroy()

    # generate frame and start animation
    def _generate_frame(self):
        # n- no. of atoms, r - atom radius, v - atom velocity given by user
        self.n = int(self.AtomNumInput.get())
        self.r = int(self.AtomRadInput.get())
        self.v = int(self.AtomSpeedInput.get())
        # initialising frame
        self.frame = tk.Frame(self.master, height=min(self.n * self.r, 600), width=min(self.n * self.r, 600))
        self.frame.grid(row=4, columnspan=2, padx=10, pady=10)
        # embedding pygame into tkinter
        # TODO: check if supported by Linux
        os.environ['SDL_WINDOWID'] = str(self.frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        # start animation
        self.app1 = App1(self.r, self.v, self.n, 100, self.frame)
        self.app1._start()


# FIXME: Maybe there is a better way to store rgb colors than dict?
color = {
    "INFECTED": (255, 0, 0),  # Red in RGB
    "HEALTHY": (0, 0, 255),  # Blue in RGB
    "CARRIER": (255, 0, 255)  # Purple in RGB
}
# list to store distance between red atom's hits
way_segments =[]

class Color(Enum):
    PURPLE = 3
    RED = 2
    BLUE = 1

class Collision(Enum):
    A_SPEED_UP = 7
    B_SPEED_UP = 6
    SWAP_X_Y = 5
    B_PLUS_X = 4
    A_PLUS_X = 3
    B_PLUS_Y = 2
    A_PLUS_Y = 1


class Container:
    """ Main container used for simulations"""

    def __init__(self, radius, number):
        self.position = (0, 0)
        self.size = (min(radius*number, 600), min(radius*number, 600))
        self.image = game.image.load(BACKGROUND_IMAGE)
        # Scale background image to fit container size
        self.image = game.transform.scale(self.image, self.size)

    @property
    def borders(self):
        """ Automatically calculate container borders.
        :return: dict with borders
        """
        return {
            "left": self.position[0],
            "right": self.position[0] + self.size[0],
            "up": self.position[1],
            "down": self.position[1] + self.size[1]
        }


class Atom:
    """ Class representing single atom """

    def __init__(self, radius, screen, container, velocity):
        """ Generate atom
        :param radius: radius of an atom
        :param screen: reference to main display
        :param container: container object where to put atoms
        """

        # Start positions on x and y axis
        self.x = random.randint(radius, container.size[0] - radius)
        self.y = random.randint(radius, container.size[1] - radius)

        self.radius = radius
        self.color = color['HEALTHY']
        self.thickness = 1
        self.speed = [random.randint(0, velocity), random.randint(0, velocity)]
        self.angle = random.uniform(0, math.pi * 2)
        # Main display
        self.screen = screen
        # Container in which atoms are present
        self.container = container
        self.main_speed = self._calculate_speed()
        self.type = Color.BLUE

    def _calculate_speed(self):
        ms = math.sqrt(self.speed[0]**2 + self.speed[1]**2)
        return ms

    def draw(self):
        """ Draw atom on screen """
        game.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius, self.thickness)

    def bounce(self):
        """ Bounce Atom from the walls """

        # Use "Exceeding boundaries" section for calculating new direction
        # http://archive.petercollingridge.co.uk/book/export/html/6

        if self.x > self.container.size[0] - self.radius:
            self.x = 2 * (self.container.size[0] - self.radius) - self.x
            self.angle = - self.angle

        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = - self.angle

        if self.y > self.container.size[1] - self.radius:
            self.y = 2 * (self.container.size[1] - self.radius) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle

    def move(self):
        """ Move Atom by one frame """
        self.x += math.sin(self.angle) * self.speed[0]
        self.y -= math.cos(self.angle) * self.speed[1]
        self.bounce()


class App1:
    """ Main application window """

    def __init__(self, radius, velocity, number_of_atoms, time_coeff, parent):
        """ Generate main game
        :param radius: radius of single atom
        :param number_of_atoms: number of atoms in container
        :param velocity: maximum velocity of single atom
        :param time_coeff: time coefficient - M in task contents
        :param parent: relate to tkinter frame - updating frame
        """
        self.frame = parent
        self.display = game.display.set_mode((radius*number_of_atoms, radius*number_of_atoms))
        self.running = True
        # FPS clock
        self.clock = game.time.Clock()
        # Container with atoms
        self.container = Container(radius, number_of_atoms)
        # Generate atoms
        self.atoms = [Atom(radius, self.display, self.container, velocity) for i in range(number_of_atoms+1)]
        self.red_hits = 0
        self.types = [number_of_atoms, 1, 0]
        self.ticks_count = 0
        self.tries = (velocity * number_of_atoms * time_coeff)//10
        self.red_ticks = 0

    def _start(self):
        """ Start the simulation """
        self._init_red()
        while self.running:

            if self.types[0] == 0 or self.tries == 0:
                print("Red atom hits frequency:", round(self.red_hits/self.ticks_count, 4), "per tick" )
                print("Healthy:", self.types[0], "Infected:", self.types[1], "Carriers:", self.types[2])
                print("avg distance between hits:", round(sum(way_segments)/self.red_hits, 3))
                break
            self.red_ticks += 1
            self._tick()
            self.tries -= 1
            self.ticks_count += 1


    def _tick(self):
        """ Frame function - called every frame """
        self.display.blit(self.container.image, self.container.position)
        for atom in self.atoms:
            atom.move()
            self._collide(atom)
            atom.draw()
        game.display.flip()
        self.frame.update()
        # Tick frame, increasing tick will result in faster simulation
        self.clock.tick(60)

    def _init_red(self):
        self.atoms[0].x = self.atoms[0].radius
        self.atoms[0].y = self.atoms[0].container.borders["down"] - self.atoms[0].radius
        self.atoms[0].color = color["INFECTED"]
        self.atoms[0].angle = 5*math.pi/4
        self.atoms[0].type = Color.RED

    # for each atom in self.atoms which is not A check if 2 atoms collide with each other
    def _collide(self, A):
        for at in self.atoms:
            if at != A:
                if collision(A, at):
                    if A.type == Color.RED:
                        self.red_hits += 1
                        way_segments.append(self.red_ticks * A.main_speed)
                        self.red_ticks = 0
                        if at.type == Color.BLUE:
                            at.type = Color.PURPLE
                            at.color = color["CARRIER"]
                            self.types[0] -= 1
                            self.types[2] += 1
                    elif at.type == Color.RED:
                        self.red_hits += 1
                        way_segments.append(self.red_ticks * at.main_speed)
                        self.red_ticks = 0
                        if A.type == Color.BLUE:
                            A.type = Color.PURPLE
                            A.color = color["CARRIER"]
                            self.types[0] -= 1
                            self.types[2] += 1
                    collision_type = parallel(A, at)
                    # A speeds up, B stops
                    if collision_type == Collision.B_SPEED_UP:
                        A.speed = [A.speed[0] + at.speed[0], A.speed[1] + at.speed[1]]
                        at.speed = [0, 0]
                    # B speeds up, A stops
                    elif collision_type == Collision.A_SPEED_UP:
                        at.speed = [A.speed[0] + at.speed[0], A.speed[1] + at.speed[1]]
                        A.speed = [0, 0]
                    # A and B change velocity and angles
                    elif collision_type == Collision.SWAP_X_Y:
                        A.speed, at.speed = at.speed, A.speed
                        A.angle, at.angle = at.angle, A.angle
                    # B gets A horizontal velocity + exchange angles
                    elif collision_type == Collision.B_PLUS_X:
                        at.speed[0] = A.speed[0]
                        A.speed[0] = 0
                        A.angle, at.angle = at.angle, A.angle
                    # A gets B horizontal velocity + exchange angles
                    elif collision_type == Collision.A_PLUS_X:
                        A.speed[0] = at.speed[0]
                        at.speed[0] = 0
                        A.angle, at.angle = at.angle, A.angle
                    # B gets A vertical velocity + exchange angles
                    elif collision_type == Collision.B_PLUS_Y:
                        at.speed[1] = A.speed[1]
                        A.speed[1] = 0
                        A.angle, at.angle = at.angle, A.angle
                    # A gets B vertical velocity + exchange angles
                    elif collision_type == Collision.A_PLUS_Y:
                        A.speed[1] = at.speed[1]
                        at.speed[1] = 0
                        A.angle, at.angle = at.angle, A.angle
                    A.main_speed = A._calculate_speed()
                    at.main_speed = at._calculate_speed()


def distance(A, B):
    dist = math.sqrt((A.x-B.x)**2 + (A.y-B.y)**2)
    return dist

def collision(A, B):
    if distance(A, B) < 21/10*A.radius:
        return True
    return False

def float_compare(a, b):
    d = 0.01  # tolerance of comparison
    if 0 < a < b-d:
        return 1  # (0, 90) degree
    if b-d <= a:
        return 2  # <90,180) degree

    return 0

# values (1-4) angle difference (0, 90), value 5 angle difference (90, 180), values (6-7) angle =0
# 0 - no collision, 1- x collide 1-> 2, 2- x collide 2-> 1, 3- y collide 1-> 2, 4- y collide 2-> 1,
# 5 - x,y collision, 6 - supercollision 1-> 2, 7 - supercollision 2-> 1
def parallel(A, B):

    # the same direction B hits A
    if A.angle == B.angle and B.main_speed > A.main_speed:
        return Collision.B_SPEED_UP

    # the same direction A hits B
    if A.angle == B.angle and A.main_speed > B.main_speed:
        return Collision.A_SPEED_UP

    # obtuse angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 2:
        return Collision.SWAP_X_Y

    # B.angle =/= 90 or 270 and acute angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 1 and B.speed[0] == 0:
        return Collision.B_PLUS_X

    # A.angle =/= 90 or 270 and acute angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 1 and A.speed[0] == 0:
        return Collision.A_PLUS_X

    # B.angle =/= 0 or 180 and acute angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 1 and B.speed[1] == 0:
        return Collision.B_PLUS_Y

    # A.angle =/= 0 or 180 and acute angle between A and B
    if float_compare(abs(A.angle - B.angle), math.pi/2) == 1 and A.speed[1] == 0:
        return Collision.A_PLUS_Y
    # No collision
    return 0


if __name__ =="__main__":
    app = App()
    app.master.title("Atoms collision")
    app.master.maxsize(650, 770)
    app.mainloop()
