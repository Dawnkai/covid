# Main application
import tkinter as tk
from tkinter import messagebox
import os
import pygame as game
from simulator import Simulation
from plot import Plot
import platform
import sys
from settings import DISPLAY_SIZE, CONTAINER_SIZE


class App(tk.Frame):
    """Main interface GUI tkinter."""

    def __init__(self):
        self.master = None
        super().__init__()
        self._sanity_check()
        self.number_of_atoms = 0
        self.radius = 0
        self.velocity = 0
        self.time_coefficient = 0
        self.results = [[], [], [], []]
        self.simulation = None

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

        # Time coefficient input
        self.TimeLabel = tk.Label(self.master, text="Wspolczynnik czasu", font=10)
        self.TimeLabel.grid(row=3)
        self.TimeInput = tk.Entry(self.master)
        self.TimeInput.grid(row=3, column=1)

        # Simulation start button
        self.StartButton = tk.Button(
            self.master, text="Start", command=self._start_simulation
        )
        self.StartButton.grid(row=4)

        # Close simulation button
        self.StopButton = tk.Button(
            self.master, text="Stop", command=self._close_simulation
        )
        self.StopButton.grid(row=4, column=1)

        # Draw plot button
        self.DrawPlotButton = tk.Button(
            self.master, text="Draw Plot", command=self._display_plot
        )
        self.DrawPlotButton.grid(row=6)

        # Quit button
        self.QuitButton = tk.Button(self.master, text="Quit", command=self._exit)
        self.QuitButton.grid(row=6, columnspan=2)

        # Simulation
        self.simulation_window = None
        self.simulation = None

        # Plot
        self.plot_distance_window = None
        self.plot_frequency_window = None
        self.plot_distance = None
        self.plot_frequency = None

    def _sanity_check(self):
        """Workaround for Windows."""
        if platform.system() == "Windows":
            os.environ["SDL_VIDEODRIVER"] = "windib"
        else:
            game.init()

    def _exit(self):
        """Exit the program."""
        print(self.results)
        sys.exit()

    def _close_simulation(self):
        """Close the simulation."""
        if self.simulation:
            self.results[0].append(self.number_of_atoms)
            self.results[1].append(self.time_coefficient)
            self.results[2].append(self.simulation.result_distance)
            self.results[3].append(self.simulation.result_frequency)
            self.simulation_window.destroy()
            self.simulation._exit()

    def _start_simulation(self):
        """Start simulation in pygame."""
        self.number_of_atoms = int(self.AtomNumInput.get())
        self.radius = int(self.AtomRadInput.get())
        self.velocity = int(self.AtomVelocityInput.get())
        self.time_coefficient = int(self.TimeInput.get())

        if self.number_of_atoms <= 100:
            self._scaling()
            # Create frame for pygame
            self.simulation_window = tk.Frame(
                self.master, height=CONTAINER_SIZE[0], width=CONTAINER_SIZE[1]
            )
            self.simulation_window.grid(row=5, columnspan=2, padx=10, pady=10)

            # Embed pygame into frame
            os.environ["SDL_WINDOWID"] = str(self.simulation_window.winfo_id())
            # Start simulation
            self.simulation = Simulation(
                self.radius,
                self.velocity,
                self.number_of_atoms,
                self.time_coefficient,
                self.simulation_window,
            )
            self.simulation._start()
        else:
            messagebox.showerror("Błąd", "Liczba atomów nie może być większa niż 100.")

    def _display_plot(self):
        """Display results as plot"""
        self.plot_distance = Plot(
            self.results[0], self.results[1], self.results[2], self.results[3]
        )
        self.plot_distance.generate_plot()

    def _scaling(self):
        """Scale atom radius and velocity based on display size and number of atoms"""
        scaling_parameter = CONTAINER_SIZE[0] / (self.radius * self.number_of_atoms)
        self.radius = max(int(self.radius * scaling_parameter), 3)
        self.velocity = max(int(self.velocity * scaling_parameter), 1)


if __name__ == "__main__":
    app = App()
    app.master.title("Atom collisions")
    app.master.maxsize(DISPLAY_SIZE[0], DISPLAY_SIZE[1])
    app.mainloop()
