from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk


class Plot:
    def __init__(self, xs, ys, zs, plot_name):
        self.figure = figure()
        self.plot = self.figure.add_subplot(111, projection='3d')
        self.xs = xs
        self.ys = ys
        self.zs = zs
        self.plot_name = plot_name

    def generate_plot(self):
        self.plot.set_xlabel('Number of Atoms')
        self.plot.set_ylabel('Time coefficient')
        self.plot.set_zlabel(self.plot_name)
        self.plot.scatter(self.xs, self.ys, self.zs)
        self.figure.show()
