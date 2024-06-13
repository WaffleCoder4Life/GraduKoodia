import fileHandler as fh
import readOscilloscopeDataGeneral as rod
import tkinter as tk
from tkinter import messagebox
import averagefrfr as av
import matplotlib.pyplot as plt
import os


def averagePulseData():
    """Counts average pulse data from multiple datasets taken with CaprutePulseShape.py. Returns U [mV] and t [s] lists."""
    files = fh.ChooseFiles(initdir = "./dataCollection")
    numberOfDatasets = len(files)

    #SAVE DATASETS FROM DARKCOUNTS TO A LIST AND CHANGES V TO mV
    datasets = []
    for file in files:
        tempor = [1E3 * point for point in rod.readOscilloscopeData(file, 1)] #NOW [U] = mV
        datasets.append(tempor)

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


def plotPulses(numberOfPulses):
    """Argument numberOfPulses = how many different pulses to plot. Plots average data taken with CapturePulseShape.py and saves image."""
    colours = ["indigo","blue","lightseagreen","green","yellowgreen","gold", "darkorange", "red"]
    i = 1
    while i <= numberOfPulses:
        voltageAxis, timeAxis = averagePulseData()
        label = fh.inputText("label for plot")
        plt.plot([(1E9 * point)-250 for point in timeAxis], voltageAxis, c=colours[i+1], label=str(label))
        i += 1
    title = fh.inputText("image title")
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




def main():
    plotPulses(3)






if __name__ == "__main__":
    main()