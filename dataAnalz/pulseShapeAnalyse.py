import readOscilloscopeData as rod
import averagefrfr as av
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import scipy.integrate as integ
from array import array
import numpy as np
import deviceControl as cont
from scipy.signal import find_peaks
import pyvisa as visa
import statistics
import os
"""Saves data from single photon pulses to CSV files and plots their average. Take measurements with different bias voltages and then use plotChargeAndHeight to determine
   breakdown voltage from pulse charge and height. When measuring charge and height of single pulse with different bias voltages start with an overvoltage of approximately
   2 V for better pulse shape. Equivalent with pulse height > 50 mV with two amplifiers at 15 V."""


settings = {
            "deviceName" : 'USB0::0x2A8D::0x1797::CN56396144::INSTR',
            #Display settings
            "channel" : 1,
            "displayVoltRange" : 400E-3,
            "displayTimeRange" : 1E-6, # With 1E-6 saves 2000 points. If changed, need to fix later plottings
            "triggerLevel" : 60E-3, # Use around 2/3 of single pulse height
            "peakDistance" : 300, # Adjust if double peaks captured. Lower value -> filters double peaks better. (If very low, filters single peaks due to noise)

            # ChANGE FOR NEW MEASUREMENTS
            "pathNameDate": "26042024",
            "fileName": "pulseChargeAndHeightPT445Ohm", #Adds biasVoltage to the end of the name.
            "biasVoltage" : "25V", # SET VOLTAGE WITH ANOTHER PROGRAM
            "temperature" : "PT 445 $\\Omega$ ",
            "testDescribtion" : "Pulse height measurements with 2 amplifiers at 14.90 V. Dark counts and temperature PT 445 Ohm",

            "numberOfDataSets": 100,
            "backroundEnd" : 980, #Display from 0 to 2000, if no delay trigger at 1000
            "filterBeforePeak" : 30E-3, # Checks if data value before pulse is higher than this value and filters it out. Used to filter noisy pulses
            
            "averagePlotName" : "100singleCountAverage",

            # CONTROL
            "connectDevice" : 1,
            "setOscilloscopeDisplay" : 1,
            "saveOscilloscopeData" : 0, #Save single screen of data. Change display settings from oscilloscope to choose what to save. Saves as fileName1, fileName2 etc.
            "pulseAveragePlot": 1,
            "plotSinglePulse": 0,
            "captureSingleScreens" : 1, #Captures NumberOfDataSets times a single pulse shape from oscilloscope

            "closeAfter" : 1
}

if settings["connectDevice"]:
    rm = visa.ResourceManager()
    osc = rm.open_resource(settings["deviceName"])
    print("Device connected")


def saveOscilloscopeData(settings):
    cont.saveData(osc, settings["fileName"]+settings["biasVoltage"], settings["testDescribtion"], False)

def setOscilloscopeDisplay(settings):
    cont.setDisplay(osc, settings["channel"], settings["displayVoltRange"], settings["displayTimeRange"], settings["triggerLevel"])

def captureSingleScreens(settings):
    cont.setDisplay(osc, settings["channel"], settings["displayVoltRange"], settings["displayTimeRange"], settings["triggerLevel"])
    i = 1
    osc.write("CHAN1:DISP 1")
    path = "./dataCollection/"+settings["pathNameDate"]+"/pulseCharge"+settings["biasVoltage"]
    if not os.path.exists(path):
        os.makedirs(path)
    while i <= settings["numberOfDataSets"]:
        osc.write(":SINGLE")
        cont.saveData(osc, settings["fileName"]+settings["biasVoltage"], settings["fileName"]+settings["biasVoltage"]+" "+settings["testDescribtion"], True)
        temp = rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+settings["biasVoltage"], 1)
        if cont.countPeaks(temp, settings["triggerLevel"]-0.005, settings["peakDistance"]) == 1 and cont.countPeaks(temp, settings["triggerLevel"] * 2, settings["peakDistance"]) == 0 and temp[990] < settings["filterBeforePeak"]:
            os.rename("./dataCollection/"+settings["pathNameDate"]+"/Temp/"+settings["fileName"]+settings["biasVoltage"]+".csv","./dataCollection/" + settings["pathNameDate"]+"/pulseCharge"+settings["biasVoltage"]+"/"+settings["fileName"]+settings["biasVoltage"]+str(i)+".csv")
            i += 1
        else:
            os.remove("./dataCollection/" + settings["pathNameDate"]+"/Temp/"+settings["fileName"]+settings["biasVoltage"]+".csv")



def plotSinglePulse(settings):
    """Use to check that pulse is in the middle"""
    plt.plot([1E6 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/pulseCharge"+settings["biasVoltage"]+"/"+settings["fileName"]+settings["biasVoltage"]+"1", 0)], [1E3 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/pulseCharge"+settings["biasVoltage"]+"/"+settings["fileName"]+settings["biasVoltage"]+"1", 1)])
    plt.xlabel("$t$ / $\\mathrm{\\mu}$s")
    plt.ylabel("$U$ / mV")
    plt.show()


def pulseAveragePlot(settings):
    #AVERAGE OF numberOfDataSets SINGLE COUNTS
    #print(list(cm._colormaps)) #LIST OF COLORMAPS :)
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_prop_cycle('color',[cm.Greens(i) for i in np.linspace(0, 1, settings["numberOfDataSets"])])


    #SAVE DATASETS FROM DARKCOUNTS TO A LIST AND CHANGES V TO mV
    #SCATTERPLOT OF ALL DATASETS WITH us TIME AXIS
    i = 1
    datasets = []
    while i <= settings["numberOfDataSets"]:
        tempor = [1E3 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/pulseCharge"+settings["biasVoltage"]+"/"+settings["fileName"]+settings["biasVoltage"]+"{0}".format(str(i)), 1)]
        #NOW [U] = mV
        datasets.append(tempor)
        ax1.plot([1E6 * point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/pulseCharge"+settings["biasVoltage"]+"/"+settings["fileName"]+settings["biasVoltage"]+"{0}".format(str(i)), 0)], tempor)
        i += 1

    #AVERAGE OF BACKGROUND FROM ALL DATASETS FROM START TO PULSE
    #AVERAGE OF THE AVERAGE: TO BE SUBTRACTED FROM PULSE DATA TO COMPENSATE BG
    BGaverage = av.averageData(settings["numberOfDataSets"], [dataset[:950] for dataset in datasets])
    

    BGcorrectiontemp = 0
    for point in BGaverage:
        BGcorrectiontemp = BGcorrectiontemp + point
    BGcorrection = BGcorrectiontemp / len(BGaverage)
    

    #AVERAGE PULSE DATA FROM ALL DATASETS AND SUBTRACT BG CORRECTION
    pulseaveragetemp = av.averageData(settings["numberOfDataSets"], [dataset[950:1500] for dataset in datasets])
    pulseaverage = [point - BGcorrection for point in pulseaveragetemp]
    timeAxis = [point for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/pulseCharge"+settings["biasVoltage"]+"/"+settings["fileName"]+settings["biasVoltage"]+"1", 0)[:550]]
    # INTEGRATION USING SIMPSON'S RULE
    pulaver = np.multiply(array("f", pulseaverage),1E-3) # NOW [U] = V
    area = integ.simps(pulaver, timeAxis, dx = 1, even = "avg")
    areaforimage = format(area, "e")


    print(f"Height from average image is {max(pulseaverage) - min(pulseaverage)}")

    # INTEGRATION FOR INDIVIDUAL PULSES
    areaList = []
    pulseChargeList = [] # List of charges counted from individual pulses
    pulseHeightList = [] # List of heights counted from individual pulses
    for dataset in datasets:
        dataAveg = [data - BGcorrection for data in dataset[950:1500]] # 275 ns window if time division = 100 ns
        pulaverSing = np.multiply(array("f", dataAveg),1E-3) # NOW [U] = V
        areaSing = integ.simps(pulaverSing, timeAxis, dx = 1, even = "avg")
        areaList.append(areaSing)
        pulseChargeSing = format(areaSing / (223.87*50*1.602*10**-19), "e")
        pulseChargeList.append(float(pulseChargeSing))
        pulseHeightList.append((max(dataAveg))*10**-3)

    
    
    print(f"Max height {max(dataAveg)} and min height {min(dataAveg)}")
    average = 0
    for charge in pulseChargeList:
        average += charge
    average /= len(pulseChargeList)
    variance = statistics.pvariance(pulseChargeList)
    print(f"Pulse charge is {average} with variance of {variance} and standard deviation of {np.sqrt(variance)}")

    outofbound = 0
    for charge in pulseChargeList:
        if charge - average > np.sqrt(variance) or average - charge > np.sqrt(variance):
            outofbound += 1

    print(f"Measurements higher or lower than one sigma: {outofbound}")
        
    
    average2 = 0
    for height in pulseHeightList:
        average2 += height
    average2 /= len(pulseHeightList)
    variance2 = statistics.variance(pulseHeightList)
    print(f"Pulse height is {average2} with variance of {variance2} and standard deviation of {np.sqrt(variance2)}")

    pulseCharge = format(area / (223.87*50*1.602*10**-19), "e")
    pulseCharge = float(pulseCharge)
    pulseCharge2 = f"{pulseCharge:.3e}"
    print(pulseCharge2+" e")

    pulseHeight = average2*10**3
    pulseHeight2 = f"{pulseHeight:.2f}"

    with open("./DataCollection/"+settings["pathNameDate"]+"/chargeAndHeightData.csv", "a") as file:
        # Saves pulse charge, variance, height, variance to csv file.
        file.write(str(average)+","+str(variance)+","+str(average2)+","+str(variance2)+"\n")
    
    ax2.plot([1E6 * point for point in timeAxis], pulseaverage, c="black", label=str(settings["numberOfDataSets"])+" pulse average")
    ax1.set_xlabel("$t$ / $\\mathrm{\\mu}$s")
    ax1.set_ylabel("$U$ / mV")
    ax1.set_title("$R_{\\mathrm{T}}$="+settings["temperature"]+", SiPM bias: "+settings["biasVoltage"])
    ax2.set_xlabel("$t$ / $\\mathrm{\\mu}$s")
    ax2.set_ylabel("$U$ / mV")
    ax2.legend()
    fig.tight_layout()
    ax2.text(0.155, 3/5*max(pulseaverage), f'Pulse\ncharge: {pulseCharge2} e', fontsize=10)
    ax2.text(0.155, 1/3*max(pulseaverage), f'Pulse\nheight: {pulseHeight2} mV', fontsize=10)
    plt.savefig("./dataCollection/"+str(settings["pathNameDate"])+"/Photos/"+settings["averagePlotName"]+settings["biasVoltage"]+".png")
    plt.show()

def runAnalyze(settings):

    if settings["setOscilloscopeDisplay"]:
        setOscilloscopeDisplay(settings)

    if settings["saveOscilloscopeData"]:
        saveOscilloscopeData(settings)

    if settings["captureSingleScreens"]:
        captureSingleScreens(settings)

    if settings["plotSinglePulse"]:
        plotSinglePulse(settings)

    if settings["pulseAveragePlot"]:
        pulseAveragePlot(settings)






runAnalyze(settings)

if settings["closeAfter"]:
    osc.close()