# Main application
import tkinter as tk
import os
import pygame as game
from simulator import Simulation
import platform
import sys
from settings import DISPLAY_SIZE, CONTAINER_SIZE


class App(tk.Frame):
    """ Main interface GUI tkinter"""
    def __init__(self):
        self.master = None
        super().__init__()
        self._sanity_check()
        self.number_of_atoms = 0
        self.radius = 0
        self.velocity = 0

        # Atom numbers input
        self.AtomNumLabel = tk.Label(self.master, text="Liczba atomów", font=10)
        self.AtomNumLabel.grid(row=0)
        self.AtomNumInput = tk.Entry(self.master)
        self.AtomNumInput.grid(row=0, column=1)

        # Atom radius input
        self.AtomRadLabel = tk.Label(self.master, text="Promień atomu", font=10)
        self.AtomRadLabel.grid(row=1)
        self.AtomRadInput = tk.Entry(self.master)
        self.AtomRadInput.grid(row=1, column=1)

        # Atom velocity input
        self.AtomVelocityLabel = tk.Label(self.master, text="Predkości atomów", font=10)
        self.AtomVelocityLabel.grid(row=2)
        self.AtomVelocityInput = tk.Entry(self.master)
        self.AtomVelocityInput.grid(row=2, column=1)

        # Simulation start button
        self.StartButton = tk.Button(self.master,
                                     text="Start",
                                     command=self._start_simulation)
        self.StartButton.grid(row=3)

        # Close simulation button
        self.StopButton = tk.Button(self.master,
                                     text="Stop",
                                     command=self._close_simulation)
        self.StopButton.grid(row=3, column=1)

        # Quit button
        self.QuitButton = tk.Button(self.master,
                                    text="Quit",
                                    command=self._exit)
        self.QuitButton.grid(row=5, column=1)

        # Simulation
        self.simulation_window = None
        self.simulation = None


    def _sanity_check(self):
        if platform.system() == 'Windows':
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        else:
            game.init()


    # Exit the program
    def _exit(self):
        sys.exit()


    # Close the simulation
    def _close_simulation(self):
        self.simulation._exit()


    # Start simulation in pygame
    def _start_simulation(self):
        self.number_of_atoms = int(self.AtomNumInput.get())
        self.radius = int(self.AtomRadInput.get())
        self.velocity = int(self.AtomVelocityInput.get())

        # Create frame for pygame
        self.simulation_window = tk.Frame(self.master, height=CONTAINER_SIZE[0], width=CONTAINER_SIZE[1])
        self.simulation_window.grid(row=4, columnspan=2, padx=10, pady=10)

        # Embed pygame into frame
        os.environ['SDL_WINDOWID'] = str(self.simulation_window.winfo_id())
        # Start simulation
        self.simulation = Simulation(self.radius, self.velocity, self.number_of_atoms, 100)
        self.simulation._start()


if __name__ =="__main__":
    app = App()
    app.master.title("Atom collisions")
    app.master.maxsize(DISPLAY_SIZE[0], DISPLAY_SIZE[1])
    app.mainloop()
