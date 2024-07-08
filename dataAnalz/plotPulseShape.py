import fileHandler as fh
import readOscilloscopeDataGeneral as rod
import tkinter as tk
from tkinter import messagebox
import averagefrfr as av
import matplotlib.pyplot as plt
import os
import morningCoffee as mc
from datetime import date
from scipy.optimize import curve_fit
import numpy as np
from pyarma import *
import pyarma

def exp(x, m, t, b):
        return m * np.exp(-x / t) + b

def expSup(x, m, t, y, n, tt):
        return m * np.exp(-x / t) + n * np.exp(-y / tt)


def averagePulseData():
    """Counts average pulse data from multiple datasets taken with CaprutePulseShape.py. Returns U [mV] and t [s] lists. Saves the lists to Temp folder to be used again."""

    """Creates folder if it does no exists, saves selection to Temp folder so it can be quickly accessed again to change plot settings."""
    mc.main()
    tempFolder = fh.returnToday() + "/Temp/previousSelection"
    with open("./Datacollection./"+tempFolder, "a") as temp:
        files = fh.ChooseFiles(initdir = "./dataCollection")
        numberOfDatasets = len(files)

        #SAVE DATASETS FROM DARKCOUNTS TO A LIST AND CHANGES V TO mV
        datasets = []
        for file in files:
            tempor = [1E3 * point for point in rod.readOscilloscopeData(file, 1)] #NOW [U] = mV
            datasets.append(tempor)
            temp.write(file+"\n")
        temp.write("NEW DATASET\n")
        # AVERAGE OF BACKGROUND FROM ALL DATASETS FROM START TO PULSE
        # AVERAGE OF THE AVERAGE: TO BE SUBTRACTED FROM PULSE DATA TO COMPENSATE BG
        BGaverage = av.averageData(numberOfDatasets, [dataset[:450] for dataset in datasets]) # With time range of 50 ns/division takes 999 datapoints
        BGcorrectiontemp = 0
        for point in BGaverage:
            BGcorrectiontemp = BGcorrectiontemp + point
        BGcorrection = BGcorrectiontemp / len(BGaverage)

        #AVERAGE PULSE DATA FROM ALL DATASETS AND SUBTRACT BG CORRECTION
        pulseaveragetemp = av.averageData(numberOfDatasets, [dataset[400:] for dataset in datasets])
        pulseaverage = [point - BGcorrection for point in pulseaveragetemp]
        timeAxis = [point for point in rod.readOscilloscopeData(files[0], 0)[400:]]
        

    return pulseaverage, timeAxis

def averagePulseDataPreviousSelect(tempFolder):
    """Using previously selected files counts average pulse data from multiple datasets taken with CaprutePulseShape.py. Returns U [mV] and t [s] lists.
      Saves the lists to Temp folder to be used again.
      NEXT TIME: split csv file into lists containing the file names, make plotting scheme for that shit."""

   
    with open("./Datacollection./"+tempFolder, "r") as temp:
        dataDict = {}
        i = 1
        dataDict[i] = []
        for line in temp:
            if line.strip() == "NEW DATASET":
                i += 1
                dataDict[i] = []
            else:
                dataDict[i].append(line.strip())
        dataDict.popitem()
        voltDict = {}
        timeDict = {}

        #SAVE DATASETS FROM DARKCOUNTS TO A LIST AND CHANGES V TO mV
        for key in dataDict.keys():
            dataVolt = []
            for j in range(len(dataDict[key])):
                dataVolt.append([1E3 * point for point in rod.readOscilloscopeData(dataDict[key][j], 1)]) #NOW [U] = mV

            # AVERAGE OF BACKGROUND FROM ALL DATASETS FROM START TO PULSE
            # AVERAGE OF THE AVERAGE: TO BE SUBTRACTED FROM PULSE DATA TO COMPENSATE BG
            BGaverage = av.averageData(len(dataDict[key]), [dataset[:450] for dataset in dataVolt]) # With time range of 50 ns/division takes 999 datapoints
            BGcorrectiontemp = 0
            for point in BGaverage:
                BGcorrectiontemp = BGcorrectiontemp + point
            BGcorrection = BGcorrectiontemp / len(BGaverage)

            #AVERAGE PULSE DATA FROM ALL DATASETS AND SUBTRACT BG CORRECTION
            pulseaveragetemp = av.averageData(len(dataDict[key]), [dataset[400:] for dataset in dataVolt])
            pulseaverage = [point - BGcorrection for point in pulseaveragetemp]
            voltDict[key] = pulseaverage
            timeDict[key] = rod.readOscilloscopeData(dataDict[key][0], 0)[400:]

        return voltDict, timeDict

def plotPulses(numberOfPulses):
    """Argument numberOfPulses = how many different pulses to plot. Plots average data taken with CapturePulseShape.py and saves image."""
    colours = ["indigo","blue","lightseagreen","green","yellowgreen","gold", "darkorange", "red"]
    chooseWind = fh.ButtonWindow("Use previous selected files or select new files?", 'Select new files', 'Use previous selection')
    choice = chooseWind.run()
    print(choice)

    if choice == 1:
        if os.path.exists(fh.returnToday() + "/Temp/previousSelection"):
            os.remove(fh.returnToday() + "/Temp/previousSelection")
        i = 1
        while i <= numberOfPulses:
            voltageAxis, timeAxis = averagePulseData()
            print(len(voltageAxis))
            label = fh.inputText("label for plot")
            plt.plot([(1E9 * point)-250 for point in timeAxis[110:]], voltageAxis[110:], c=colours[i+1], label=str(label))
            asd = np.linspace(timeAxis[110], timeAxis[-1], 100)
            popt, pcov = curve_fit(exp, timeAxis[110:], voltageAxis[110:], (100, 60e-9, 0))
            line = exp(asd, *popt)
            plt.plot([1e9 * point -250 for point in asd], line)
            print(popt, pcov)
            i += 1
    if choice == 2:
        print("we are here")
        tempFolder = fh.returnToday() + "/Temp/previousSelection"
        voltageDict, timeDict = averagePulseDataPreviousSelect(tempFolder)
        #print(timeDict[1])
        for key in voltageDict:
            label = fh.inputText("label for plot")
            plt.plot([(1E9 * point)-250 for point in timeDict[1]], voltageDict[key], c=colours[key], label=str(label))
    title = fh.inputText("image TITLE")
    plt.title(title)
    plt.xlabel("$t$ / ns")
    plt.ylabel("$U$ / mV")
    plt.xlim(-50, 250)
    plt.legend()
    plt.tight_layout()
    folder = fh.ChooseFolder(initdir = "./dataCollection", title = "Save image to")
    name = fh.inputText("image file name")
    plt.savefig(folder+"/"+name+".png")
    plt.show()

def exponentialFit():
    """Fit to calculate the time constant. Choose files from foulder, takes the average pulse shape, choose start and end points for exponential fit"""
    voltageAxis, timeAxis = averagePulseData()
    voltageAxis = voltageAxis[100:]
    timeAxis = timeAxis[100:]
    start = pick_point_from_scatter(timeAxis, voltageAxis, "Select starting point for exponential fit")
    end = pick_point_from_scatter(timeAxis, voltageAxis, "Select ending point for exponential fit")
    #plt.plot([(1E9 * point)-250 for point in timeAxis[110:]], voltageAxis[110:], c="indigo", label=str("Data points"))
    asd = np.linspace(timeAxis[start], timeAxis[end], 100)
    print(voltageAxis[start])
    popt, pcov = curve_fit(exp, timeAxis[start:end], voltageAxis[start:end], (voltageAxis[start], 1e-9, 0)) # Curve fit with starting quess [highest voltage, time constant, baseline]
    line = exp(asd, *popt)
    plt.plot([point for point in asd], line, label=str(r"Exponential fit $V_{0}\cdot e^{-t/\tau}$"))
    print(popt, pcov)
    plt.xlabel("$t$ / ns")
    plt.ylabel("$U$ / mV")
    #plt.xlim(-50, 250)
    plt.legend()
    plt.tight_layout()
    print(f"Time constant {popt[1]} with standard deviation of {np.sqrt(pcov[1][1])}")
    plt.show()


def expFitInternet():
    

    # Generate data to fit
    """ dx = 0.02
    x = pyarma.regspace(dx, dx, 1.5)
    y = 5*pyarma.exp(0.5*x) + 4*pyarma.exp(-3*x) + 2*pyarma.exp(-2*x) - 3*pyarma.exp(0.15*x)
    print(x) """

    y, x = averagePulseData()
    plt.scatter([(1E9 * point)-250 for point in x[100:]], y[100:])
    y = pyarma.mat(y[110:])
    x = pyarma.mat(x[110:])
    y.reshape(499,1)
    x.reshape(499,1)
    print(x)
    print(y)

    # Compute integrals
    def cumtrapz(x, y):
        return pyarma.join_vert(pyarma.mat(1,1), 0.5 * pyarma.cumsum(pyarma.diff(x) @ (y[1:y.n_elem-1,0] + y[0:y.n_elem-2,0])))

    iy1 = cumtrapz(x, y)
    iy2 = cumtrapz(x, iy1)
    #iy3 = cumtrapz(x, iy2)
    #iy4 = cumtrapz(x, iy3)

    # Compute exponentials lambdas
    def join_horizontal(*args):
        if type(args[0]) is tuple:
            args = args[0]
        if len(args) == 1:
            return args[0]
        else:
            return pyarma.join_horiz(args[0], join_horizontal(args[1:len(args)]))

    #Y = join_horizontal(iy1, iy2, iy3, iy4, pow(x, 3), pow(x, 2), x, pyarma.ones(pyarma.size(x))) ORIGINAL
    Y = join_horizontal(iy1, iy2, pow(x, 3), pow(x, 2), x, pyarma.ones(pyarma.size(x)))
    A = pyarma.pinv(Y)*y;
    """ lambdas = pyarma.eig_gen(pyarma.mat([
        [A[0], A[1], A[2], A[3]],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0]
    ]))[0] """
    lambdas = pyarma.eig_gen(pyarma.mat([
        [A[0], A[1]],
        [1, 0]
    ]))[0]
    lambdas = pyarma.real(lambdas)
    lambdas.print("lambdas = ")
    #lambdas = 
    #  -2.9991
    #  -1.9997
    #   0.5000
    #   0.1500

    # Compute exponentials multipliers
    # X = join_horizontal(pyarma.exp(lambdas[0]*x), pyarma.exp(lambdas[1]*x), pyarma.exp(lambdas[2]*x), pyarma.exp(lambdas[3]*x))
    X = join_horizontal(pyarma.exp(lambdas[0]*x), pyarma.exp(lambdas[1]*x))
    P = pyarma.pinv(X)*y;
    P.print("P = ")
    #P = 
    #   4.0042
    #   1.9955
    #   4.9998
    #  -2.9996
    linspace = np.linspace(2.5075e-07, 5.0000e-07, 100)
    line = exp(linspace, P[0], lambdas[0], 0) +  exp(linspace, P[1], lambdas[1], 0)
    plt.plot([1e9 * point -250 for point in linspace], line, label=str(r"Exponential fit $V_{0}\cdot e^{-t/\tau}$"))
    plt.show()



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
    expFitInternet()
    #exponentialFit()
    






if __name__ == "__main__":
    main()