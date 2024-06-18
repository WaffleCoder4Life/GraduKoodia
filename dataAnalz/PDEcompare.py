import matplotlib.pyplot as plt
import fileHandler as fh
import readSourceMeterDataFine as read
from tkinter import messagebox


def selectFiles() -> dict:
    fileDict = {}
    key = fh.inputText("dictionary key")
    file, msbox = fh.ChooseFileMultiple(initdir="./dataCollection", text = "Choose a single file for "+key)
    fileDict[key] = file
    while msbox == "yes":
        key2 = fh.inputText("dictionary key")
        file2, msbox = fh.ChooseFileMultiple(initdir="./dataCollection", text = "Choose a single file for "+key2)
        fileDict[key2] = file2
    return fileDict

def filesIntoData(dict) -> dict:
    """Opens files and creates a dictionary; key = (voltage_list, current_list)"""
    newDict = {}
    for key in dict:
        newDict[key] = (read.readSourceMeterDataFine(dict[key][0], 0), read.readSourceMeterDataFine(dict[key][0],1))
    return newDict

def bdvoltageIndex(voltList, bdvolt):
    """Help function to return index of breakdown point"""
    data = [round(point,1) for point in voltList]
    return data.index(bdvolt)


def plotCompareIV(dataDict: dict) -> None:
    """Plots all IV curves from given dictionary. Asks names for plots and folder/name for image to be saved to. Scaling of X-axis for overvoltage."""
    colours = ["indigo","blue","lightseagreen","green","yellowgreen","gold", "darkorange", "red"]
    i = 0
    msgbox = messagebox.askquestion ('Plot as a function of overvoltage','Plot as a function of overvoltage (yes) or biasvoltage (no)?',icon = 'warning')
    if msgbox == "no":
        for key in dataDict:
            plotName = fh.inputText("name for plot "+key)
            plt.scatter(dataDict[key][0], dataDict[key][1], s = 2, marker = "d", label = plotName, color = colours[i])
            i += 1
        imageName = fh.inputText("image file name")
        imageFolder = fh.ChooseFolder(initdir="./dataCollection", title = "save" +imageName+ "to")
        plt.savefig(imageFolder+"/"+imageName)
        plt.show()


    if msgbox == "yes":
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        for key in dataDict:
            msgbox2 = messagebox.askquestion ('Plotting axis','Plot ' +key+ ' to ax1 (yes) or ax2 (no)',icon = 'warning')
            if msgbox2 == "yes":
                bdVolt = float(fh.inputText("Breakdown voltage for "+key))
                bdindex = bdvoltageIndex(dataDict[key][0], bdVolt)
                endIndex = bdvoltageIndex(dataDict[key][0], bdVolt+2.4)
                overVolt = [point-bdVolt for point in dataDict[key][0][bdindex:endIndex]]
                plotName = fh.inputText("name for plot "+key)
                ax1.scatter(overVolt,[point*1e6 for point in dataDict[key][1][bdindex:endIndex]], s = 3, marker = "d", label = plotName, color = colours[i])
                i += 1
            if msgbox2 == "no":
                bdVolt = float(fh.inputText("Breakdown voltage for "+key))
                bdindex = bdvoltageIndex(dataDict[key][0], bdVolt)
                endIndex = bdvoltageIndex(dataDict[key][0], bdVolt+2.4)
                overVolt = [point-bdVolt for point in dataDict[key][0][bdindex:endIndex]]
                plotName = fh.inputText("name for plot "+key)
                ax2.scatter(overVolt, [point*1e6 for point in dataDict[key][1][bdindex:endIndex]], s = 3, marker = "s", label = plotName, color = colours[i])
                i += 1
        ax1.legend()
        ax2.legend(loc = "upper right")
        ax1.set_ylabel("$I$ / $\\mathrm{\\mu}$A") # Check that scaling corresponds to correct unit (1E-6 = uA etc.)
        ax2.set_ylabel("$I$ / $\\mathrm{\\mu}$A")
        fig.tight_layout()
        """ imageName = fh.inputText("image file name")
        imageFolder = fh.ChooseFolder(initdir="./dataCollection", title = "save" +imageName+ "to")
        plt.savefig(imageFolder+"/"+imageName) """
        plt.show()
    
def plotRelativeIV(dataDict: dict):
    """Relative IV plot. First IV (file) is divided by the second IV."""
    key1 = list(dataDict.keys())[0]
    key2 = list(dataDict.keys())[1]
    relativeIV = []
    bdVolt1 = 21
    bdVolt2 = 24.5
    bdIndex1 = bdvoltageIndex(dataDict[key1][0], bdVolt1)
    bdIndex2 = bdvoltageIndex(dataDict[key2][0], bdVolt2)
    for data1, data2 in zip(dataDict[key1][1][bdIndex1:], dataDict[key2][1][bdIndex2:]):
        relativeIV.append(data1/data2)
    overVolt = [point-bdVolt1 for point in dataDict[key1][0][bdIndex1:]]
    plt.scatter(overVolt[5:len(relativeIV)], relativeIV[5:], s=4, marker = "d", c="black")
    plt.xlabel("Overvoltage / V")
    plt.ylabel("Relative current")
    plt.show()
    
    

def plotPDE() -> None:
    pass







def main():
    fileDict = selectFiles()
    dataDict = filesIntoData(fileDict)
    #plotCompareIV(dataDict)
    plotRelativeIV(dataDict)


if __name__ == "__main__":
    main()
