import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import os


date = "10062024"
#uv, blue or both
whichFiles = "blue"

imageTitleUV = "Room temp uv"
saveImageNameUV = f"./dataCollection/{date}/{date}test"

imageTitleBLUE = "Liquid nitrogen blue"
saveImageNameBLUE = f"./dataCollection/{date}/{date}nitroBLUE"

def generateFileNameLists(which):
    '''Generates dict of TPB measurements for uv (key 0) and blue (key 1)\nwhich: uv, blue or both\nreturns dict of tuples of paths'''

    pathDict = {}
    Tk().withdraw()
    if which == "uv":
        pathDict[0] = askopenfilenames(initialdir=os.getcwd(), title="Select UV files", filetypes=[('csv files', '*.csv')])
    elif which == "blue":
        pathDict[1] = askopenfilenames(initialdir=os.getcwd(), title="Select Blue files", filetypes=[('csv files', '*.csv')])
    else:
        pathDict[0] = askopenfilenames(initialdir=os.getcwd(), title="Select UV files", filetypes=[('csv files', '*.csv')])
        pathDict[1] = askopenfilenames(initialdir=os.getcwd(), title="Select Blue files", filetypes=[('csv files', '*.csv')])
    return pathDict

def readSourceMeterDataFine(fileName: str, dataType: int)->list:
    """NEW VERSION: ONLY TAKES CURRENT AND SOURCE VOLTAGE.  [0, 1] -> [SOURCE VOLTAGE, CURRENT]
    
    Reads the voltage source data from .csv file and returns a float type list. 
    dataType allowed arguments [0, 1, 2, 3] to determine which datalist 
    is returned [CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE]"""


    with open(fileName) as file:
        rows = []
        #File rows into a list, then delete first two rows not containing data
        for row in file:
            rows.append(row)
        del rows[2]
        del rows[1]
        del rows[0]

        dataList = []
        
        
        
        #Split row into a list and add given dataType to dataList
        for element in rows:
            rowAsList = element.split(",")
            dataList.append(float(rowAsList[dataType]))
        
        
        return dataList    


def main():

    files = generateFileNameLists(whichFiles)
    masterData = {}
    if len(files) == 1 and whichFiles == "uv":
        masterData[0] = []
        colors1 = [cm.Purples(i) for i in np.linspace(0.5, 0.9, len(files[0]))]
    elif len(files) == 1 and whichFiles == "blue":
        masterData[1] = []
        colors2 = [cm.Blues(i) for i in np.linspace(0.5, 0.9, len(files[1]))]
    else:
        masterData[0] = []
        masterData[1] = []
        colors1 = [cm.Purples(i) for i in np.linspace(0.5, 0.9, len(files[0]))]
        colors2 = [cm.Blues(i) for i in np.linspace(0.5, 0.9, len(files[1]))]

    for key in files:
        for i in range(len(files[key])):
            if "noSample" in files[key][i]:
                masterData[key].append(([1e3 * point for point in readSourceMeterDataFine(files[key][i], 0)], [1e6 * point for point in readSourceMeterDataFine(files[key][i], 1)], "noSample"))
            elif "NoTPB" in files[key][i]:
                masterData[key].append(([1e3 * point for point in readSourceMeterDataFine(files[key][i], 0)], [1e6 * point for point in readSourceMeterDataFine(files[key][i], 1)], "NoTPB"))
            else:
                masterData[key].append(([1e3 * point for point in readSourceMeterDataFine(files[key][i], 0)], [1e6 * point for point in readSourceMeterDataFine(files[key][i], 1)], "TPB"))

    if len(masterData) == 1 and whichFiles == "uv":
        i = 0
        for data in masterData[0]:
            if data[2] == "NoTPB":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors1[i], label="Plexiglas")
            elif data[2] == "noSample":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors1[i], label="No sample")
            elif data[2] == "TPB":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors1[i], label="Plexiglas with TPB")
            i += 1
        plt.xlabel("$I_{\\mathrm{led}}$ / mA", fontsize=13)
        plt.ylabel("$I_{\\mathrm{SiPM}}$ / $\\mu$A", fontsize=13)
        plt.title(imageTitleUV)
        plt.legend()
        plt.tight_layout()
        plt.savefig(saveImageNameUV)
        plt.show()
    
    if len(masterData) == 1 and whichFiles == "blue":
        i = 0
        for data in masterData[1]:
            if data[2] == "NoTPB":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors2[i], label="Plexiglas")
            elif data[2] == "noSample":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors2[i], label="No sample")
            elif data[2] == "TPB":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors2[i], label="Plexiglas with TPB")
            i += 1
        plt.xlabel("$I_{\\mathrm{led}}$ / mA", fontsize=13)
        plt.ylabel("$I_{\\mathrm{SiPM}}$ / $\\mu$A", fontsize=13)
        plt.title(imageTitleUV)
        plt.legend()
        plt.tight_layout()
        plt.savefig(saveImageNameUV)
        plt.show()
    
    if len(masterData) == 2:

        i = 0
        for data in masterData[0]:
            if data[2] == "NoTPB":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors1[i], label="Plexiglas")
            elif data[2] == "noSample":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors1[i], label="No sample")
            elif data[2] == "TPB":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors1[i], label="Plexiglas with TPB")
            i += 1
        plt.xlabel("$I_{\\mathrm{led}}$ / mA", fontsize=13)
        plt.ylabel("$I_{\\mathrm{SiPM}}$ / $\\mu$A", fontsize=13)
        plt.title(imageTitleUV)
        plt.legend()
        plt.tight_layout()
        plt.savefig(saveImageNameUV)
        plt.show()

        i = 0
        for data in masterData[1]:
            if data[2] == "NoTPB":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors2[i], label="Plexiglas")
            elif data[2] == "noSample":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors2[i], label="No sample")
            elif data[2] == "TPB":
                plt.scatter(data[0], data[1], marker='d', s=10, color=colors2[i], label="Plexiglas with TPB")
            i += 1
        plt.xlabel("$I_{\\mathrm{led}}$ / mA", fontsize=13)
        plt.ylabel("$I_{\\mathrm{SiPM}}$ / $\\mu$A", fontsize=13)
        plt.title(imageTitleBLUE)
        plt.legend()
        plt.tight_layout()
        plt.savefig(saveImageNameBLUE)
        plt.show()

if __name__ == "__main__":
    main()