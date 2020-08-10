from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk


class Plot:
    def __init__(self, xs, ys, zs1, zs2):
        # Creating figure and tbd plot.
        self.figure = figure()
        self.plot = None

        # Getting results from simulation
        self.xs = xs
        self.ys = ys
        self.zs1 = zs1
        self.zs2 = zs2

        # Setting figure title
        self.figure.canvas.set_window_title('Plots')

    def generate_plot(self):
        # Adding distance subplot
        self.plot = self.figure.add_subplot(121, projection='3d')
        self.plot.set_title('Distance Plot')
        self.plot.set_xlabel('Number of Atoms')
        self.plot.set_ylabel('Time coefficient')
        self.plot.set_zlabel('Distance')
        self.plot.scatter(self.xs, self.ys, self.zs1, marker = 'o')

        # Adding frequency subplot
        self.plot = self.figure.add_subplot(122, projection='3d')
        self.plot.set_title('Frequency Plot')
        self.plot.set_xlabel('Number of Atoms')
        self.plot.set_ylabel('Time coefficient')
        self.plot.set_zlabel('Frequency')
        self.plot.scatter(self.xs, self.ys, self.zs2)

        self.figure.tight_layout(pad=2)
        self.figure.show()
