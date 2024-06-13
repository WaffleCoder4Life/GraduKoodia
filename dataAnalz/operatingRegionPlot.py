import matplotlib.pyplot as plt
import fileHandler as fh
import readSourceMeterDataFine as read
import scipy
import tkinter as tk
import numpy as np
from sympy import Symbol
from sympy.solvers import solve


# Dictionary with temperature : [breakdownV, tunnelingV] -pairs.
tempBreakTunnel = {
    34.5 : [20.6, 31],
    33.6 : [20.7, 30.38],
    32.2 : [20.7, 29.07],
    28.7 : [20.7, 26.20],
    25.5 : [20.7, 24.49],
    22.7 : [20.8, 24.24],
    5.4 : [21, 26.67],
    1.05 : [21, 26.72]
}






def tunnelingBreakdown():
    """Use to calculate tunneling breakdown point from data by simply fitting two lines and calculating the crossing point."""
    def line(x, a, b):
        return a*x+b

    file = fh.ChooseFiles("./DataCollection")
    voltageData = read.readSourceMeterDataFine(file[0], 0)
    currentData = read.readSourceMeterDataFine(file[0], 1)
    start1 = pick_point_from_scatter(voltageData, currentData, "Select starting point for line 1")
    end1 = pick_point_from_scatter(voltageData, currentData, "Select end point for line 1")
    start2 = pick_point_from_scatter(voltageData, currentData, "Select starting point for line 2")
    end2 = pick_point_from_scatter(voltageData, currentData, "Select end point for line 2")
    voltResult1 = scipy.optimize.curve_fit(line, xdata = voltageData[start1:end1+1], ydata = currentData[start1:end1+1]) # Gives parameters for first line fit
    voltResult2 = scipy.optimize.curve_fit(line, xdata = voltageData[start2:end2+1], ydata = currentData[start2:end2+1]) # Gives parameters for second line fit
    print(f"First line slope {voltResult1[0][0]} and intercept {voltResult1[0][1]}\nSecond line slope {voltResult2[0][0]} and intercept {voltResult2[0][1]}")
    x = Symbol("x")
    y = Symbol("y")
    lineFit1 = line(x, voltResult1[0][0], voltResult1[0][1]) # arguments x, a (slope) and b (intercept)
    lineFit2 = line(x, voltResult2[0][0], voltResult2[0][1])
    breakdownResult = solve(lineFit1-lineFit2, x) # solves x from lineFit1 - lineFit2 = 0
    print(breakdownResult)


# Chat GPT generated stuff to pick a point
class PointPicker:
    def __init__(self, x, y, selection):
        self.x = x
        self.y = y
        self.selected_index = None
        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter(x, y)
        self.ax.set_title(selection)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        
        # Calculate the distances between the click and all points
        distances = np.hypot(self.x - event.xdata, self.y - event.ydata)
        self.selected_index = np.argmin(distances)
        
        print(f'Selected point index: {self.selected_index}')
        plt.close(self.fig)  # Close the plot window

def pick_point_from_scatter(x, y, title):
    picker = PointPicker(x, y, title)
    return picker.selected_index


def main():
    tunnelingBreakdown()

if __name__ == "__main__":
    main()

    