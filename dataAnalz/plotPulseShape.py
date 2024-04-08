import readOscilloscopeData as rod
import averagefrfr as av
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import scipy.integrate as integ
from array import array
import numpy as np
import deviceControl as cont
import pyvisa as visa
import statistics
import os

"""Plot pulse shape for different photoelectron pulses. Captures multiple screens from oscilloscope, reduces backround noice measured before the pulse and plots an average pulse
shape. Change trigger level to adjust how many p.e. pulses captured, e.g. 1 p.e. or 2 p.e. pulses. Start by manually measuring 1 p.e. pulse height"""

settings = {
            # Oscilloscope name
            "deviceName" : 'USB0::0x2A8D::0x1797::CN56396144::INSTR',

            # 1 p.e. pulse height to be used for other values
            "singlePhotonHeight" : 90E-3,

            # Display settings
            "channel" : 1,
            # Display volt range is set to 2 * singlePhotonHeight per division
            "displayTimeRange" : 500E-9, # 250 ns after triggering to show total pulse
            # Trigger level is set to 2/3 * singlePhotonHeight * photoelectronNumber

            # Measurement settings
            "photoelectronNumber" : 1, # Choose which p.e. to measure. 1, 2, 3 or 4 in room temp. In cold 1, 2 or 3.
            "numberOfDataSets" : 30, # Choose number of datasets to be taken for the average plot
            "biasVoltage" : "27_01V", # Use same voltage for measurements. Biasvoltage = breakdownVoltage + 2.5 V, V_bd to be determined beforehand.
            "peakDistance" : 200, # Set low enough to only capture single pulses

            # File settings
            "pathNameDate" : "08042024", # Run morningCoffee.py first and then change todays date for correct file path
            "fileName" : "roomTempPulseShape",
            "testDescribtion" : "Pulse shapes in room temp for different amount of photoelectrons",
            "averagePlotName" : "roomTemp1PE", # Name for image to be saved
            "pelist" : [1, 2, 3, 4], # Write all p.e. to be plotted in plotAll function

            # Control
            "connectDevice" : 1, # Connect pyvisa resource
            "setDisplay" : 1, # Set display or set it manually and disable this
            "captureData" : 0, # Capture numberOfDatasets amount of single screens
            "plotSinglePulse" : 0, # Plot single pulse for chechking that everything is fine
            "plotSingleAndAverage" : 1, # Plots all single pulses and their average in the same image and then average on new image, use to chechk that no bad pulses in average
            "plotAverage" : 0, # Plots average from taken datasets
            "plotAll" : 1 # Plots all p.e. in same image

}



if settings["connectDevice"]:
    rm = visa.ResourceManager()
    osc = rm.open_resource(settings["deviceName"])

def setOscilloscopeDisplay(settings):
    cont.setDisplay(osc, settings["channel"], 8*settings["singlePhotonHeight"]*2, settings["displayTimeRange"], settings["singlePhotonHeight"]*settings["photoelectronNumber"]*(2/3))


def captureSingleScreens(settings):
    peakHeight = settings["singlePhotonHeight"]*settings["photoelectronNumber"]*(9/10) # Add *(9/10) for single photon average
    osc.write(":RUN")
    i = 1
    osc.write("CHAN1:DISP 1")
    while i <= settings["numberOfDataSets"]:
        cont.saveData(osc, settings["fileName"]+str(settings["photoelectronNumber"])+"pe", settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+" "+settings["testDescribtion"], True)
        temp = rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe", 1)
        if cont.countPeaks(temp, peakHeight, settings["peakDistance"]) == 1 and cont.countPeaks(temp, peakHeight + settings["singlePhotonHeight"], settings["peakDistance"]) == 0 and cont.countPeaks(temp, settings["singlePhotonHeight"], settings["peakDistance"]) == 1:
            os.rename("./dataCollection/"+settings["pathNameDate"]+"/Temp/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+".csv","./dataCollection/" + settings["pathNameDate"]+"/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+str(i)+".csv")
            i += 1
        else:
            os.remove("./dataCollection/" + settings["pathNameDate"]+"/Temp/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+".csv")

def plotSinglePulse(settings):
    """Use to check that pulse is in the middle"""
    plt.scatter([1E6 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+"1", 0)], [1E3 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+"1", 1)], s = 6)
    plt.xlabel("$t$ / $\\mathrm{\\mu}$s")
    plt.ylabel("$U$ / mV")
    plt.show()


def pulseAveragePlot(settings):
    #AVERAGE OF numberOfDataSets SINGLE COUNTS
    #print(list(cm._colormaps)) #LIST OF COLORMAPS :)
    if settings["plotSingleAndAverage"]:
        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.set_prop_cycle('color',[cm.Greens(i) for i in np.linspace(0, 1, settings["numberOfDataSets"])])


    #SAVE DATASETS FROM DARKCOUNTS TO A LIST AND CHANGES V TO mV
    #SCATTERPLOT OF ALL DATASETS WITH ns TIME AXIS
    i = 1
    datasets = []
    while i <= settings["numberOfDataSets"]:
        tempor = [1E3 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+"{0}".format(str(i)), 1)]
        #NOW [U] = mV
        datasets.append(tempor)
        if settings["plotSingleAndAverage"]:
            ax1.plot([1E9 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+"{0}".format(str(i)), 0)], tempor)
        i += 1

    # AVERAGE OF BACKGROUND FROM ALL DATASETS FROM START TO PULSE
    # AVERAGE OF THE AVERAGE: TO BE SUBTRACTED FROM PULSE DATA TO COMPENSATE BG
    BGaverage = av.averageData(settings["numberOfDataSets"], [dataset[:450] for dataset in datasets]) # With time range of 50 ns/division takes 999 datapoints
    

    BGcorrectiontemp = 0
    for point in BGaverage:
        BGcorrectiontemp = BGcorrectiontemp + point
    BGcorrection = BGcorrectiontemp / len(BGaverage)
    

    #AVERAGE PULSE DATA FROM ALL DATASETS AND SUBTRACT BG CORRECTION
    pulseaveragetemp = av.averageData(settings["numberOfDataSets"], [dataset[400:] for dataset in datasets])
    pulseaverage = [point - BGcorrection for point in pulseaveragetemp]
    timeAxis = [point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+str(settings["photoelectronNumber"])+"pe"+"1", 0)[400:]]
    

    if settings["plotSingleAndAverage"]:
        ax2.plot([(1E9 * point)-250 for point in timeAxis], pulseaverage, c="black", label=str(settings["numberOfDataSets"])+" pulse average")
        ax1.set_xlabel("$t$ / ns")
        ax1.set_ylabel("$U$ / mV")
        ax1.set_title("$R_{\\mathrm{T}}$="+", SiPM bias: "+settings["biasVoltage"])
        ax2.set_xlabel("$t$ / ns")
        ax2.set_ylabel("$U$ / mV")
        ax2.set_xlim(-50,250)
        ax2.legend()
        fig.tight_layout()
        plt.savefig("./dataCollection/"+str(settings["pathNameDate"])+"/Photos/"+settings["averagePlotName"]+"_singles_and_average"+".png")
        plt.show()
    
    plt.plot([(1E9 * point)-250 for point in timeAxis], pulseaverage, c="tomato", label=str(settings["numberOfDataSets"])+" pulse average")
    plt.xlabel("$t$ / ns")
    plt.ylabel("$U$ / mV")
    plt.xlim(-50, 250)
    plt.legend()
    plt.tight_layout()
    plt.savefig("./dataCollection/"+str(settings["pathNameDate"])+"/Photos/"+settings["averagePlotName"]+".png")
    plt.show()

def plotAll(settings):
    colours = ["steelblue", "tomato", "gold", "purple"]
    for pe in settings["pelist"]:
        pulseVolt = [point * 1E3 for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+f"{pe}"+"pe"+"1", 1)[400:]]
        pulseTime = [point * 1E9 -250 for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/"+settings["fileName"]+f"{pe}"+"pe"+"1", 0)[400:]]
        plt.plot(pulseTime, pulseVolt, c = colours[pe-1], label = f"{pe} p.e.")
    plt.xlabel("$t$ / ns")
    plt.ylabel("$U$ / mV")
    plt.legend()
    plt.xlim(-50,250)
    plt.tight_layout()
    plt.savefig("./dataCollection/"+str(settings["pathNameDate"])+"/Photos/"+settings["averagePlotName"]+"allpe"+".png")
    plt.show()

def runMeasurement(settings):

    if settings["setDisplay"]:
        setOscilloscopeDisplay(settings)

    if settings["captureData"]:
        captureSingleScreens(settings)

    if settings["plotSinglePulse"]:
        plotSinglePulse(settings)

    if settings["plotAverage"]:
        pulseAveragePlot(settings)
    
    if settings["plotAll"]:
        plotAll(settings)

runMeasurement(settings)