import readOscilloscopeData as rod
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pyvisa as visa
from deviceControl import setDisplay, setVoltageFine, saveData
import os
from time import time

settings = {
    "pathNameDate" : "20032024",
    "fileName" : "darkcountTemp",
    "biasVoltageRange" : 50,
    "biasVoltage" : 24,
    "biasCurrentLimit" : 2.5E-3,
    "timeRange" : 100E-6,
    "runTimeSeconds" : 10,
    "peakHeight" : 0.002,
    "aquireData" : 1,
    "countPeaks" : 1,
    "deleteTempAfter" : 1


}

def aquireData(settings):
    """Acquires data :)"""

    #VISA CONNECTIONS
    rm = visa.ResourceManager()
    list = rm.list_resources()
    osc = rm.open_resource(list[0])
    
    sour = rm.open_resource("GPIB0::22::INSTR")
    sour.write("*RST")  #Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
    sour.write("SYST:ZCH OFF") #Turn off zero corrections
    sour.write(":SENS:RANG 0.00001") #SET CURRENT MEASURE RANGE (not needed but stops the device from clicking)
    setVoltageFine(sour, settings["biasVoltageRange"], settings["biasVoltage"], settings["biasCurrentLimit"])
    print("Bias voltage set.")

    setDisplay(osc, 1, 16E-3, settings["timeRange"], settings["peakHeight"])
    print("Oscilloscope display set.")
    osc.write(":RUN")

    runTime = settings["runTimeSeconds"]
    startTime = time()
    i = 1
    while (time() - startTime) < runTime:
        osc.write(":TER?")
        if osc.read() == 1:
            saveData(osc, settings["fileName"]+str(i), "Temp files for dark count rate", True)
            i += 1
    numberOfDatasets = i
    sour.write("SOUR:VOLT:STAT OFF")

    return numberOfDatasets


def deleteTemp(settings, numberOfDatasets):
    i = 1
    while i <= numberOfDatasets:
        os.remove("./dataCollection/"+str(settings["pathNameDate"])+"/Temp/"+str(settings["fileName"])+str(i)+".csv")
        i += 1

def peakCounter(settings, numberOfDatasets):

    timedic = {}
    voltdic = {}
    i = 1
    while i <= numberOfDatasets:
        voltage =  rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+str(i), 1)
        backround = 0
        for volt in voltage:
            backround += volt
        backround = backround / len(voltage)
        voltdic[settings["fileName"]+str(i)] = [volt - backround for volt in voltage]
        i += 1
    darkCounts = 0
    for key in voltdic:
        peaks = find_peaks(voltdic[key], settings["peakHeight"])
        darkCounts += len(peaks[0])
        #plt.plot(voltdic[key])
    print(f"{darkCounts} dark counts in "+str(settings["runTime"])+" seconds.")
    darkCountRate = darkCounts / settings["runTime"]
    print(f"Dark count rate {darkCountRate} Hz")
    #plt.show()


def runAnalyze(settings):

    if settings["aquireData"]:
        sets = aquireData(settings)

    if settings["countPeaks"]:
        peakCounter(settings, sets)

    if settings["deleteTempAfter"]:
        deleteTemp(settings, sets)


runAnalyze(settings)