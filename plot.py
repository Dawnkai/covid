from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class Plot:
    """Plots displaying results of the simulation."""
    def __init__(self, results):
        """Create plot.

        :param results: array, [number_of_atoms, time_coeff, distance, frequency]
        """
        # Creating figure
        self.figure = figure()
        self.plot = None

        # Getting results from simulation
        self.xs = results[0]
        self.ys = results[1]
        self.zs1 = results[2]
        self.zs2 = results[3]

        # Setting figure title
        self.figure.canvas.set_window_title("Wykresy")

    def generate_plot(self):
        """Generate plot."""
        # Adding distance subplot
        self.plot = self.figure.add_subplot(121, projection="3d")
        self.plot.set_title("Średnia droga swobodna")
        self.plot.set_xlabel("Liczba atomów")
        self.plot.set_ylabel("Stała czasowa")
        self.plot.set_zlabel("Droga")
        self.plot.scatter(self.xs, self.ys, self.zs1, marker="o")

        # Adding frequency subplot
        self.plot = self.figure.add_subplot(122, projection="3d")
        self.plot.set_title("Częstość zderzeń cząstki czerwonej")
        self.plot.set_xlabel("Liczba atomów")
        self.plot.set_ylabel("Stała czasowa")
        self.plot.set_zlabel("Częstość")
        self.plot.scatter(self.xs, self.ys, self.zs2)

        self.figure.tight_layout(pad=2)
        self.figure.show()
