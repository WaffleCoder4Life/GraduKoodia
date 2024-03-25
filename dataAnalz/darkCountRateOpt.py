import readOscilloscopeData as rod
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pyvisa as visa
from deviceControl import setDisplay, setVoltageFine, saveData
import os
from time import time, sleep

settings = {
    "pathNameDate" : "21032024",
    "fileName" : "darkcountTemp",
    "biasVoltageRange" : 50,
    "biasVoltage" : 25,
    "biasCurrentLimit" : 2.5E-3,

    "oscVoltageRange" : 16E-3,
    "timeRange" : 100E-9,
    "runTimeSeconds" : 100,
    "peakHeight" : 0.002,

    "aquireData" : 1,
    "countPeaks" : 0,
    "deleteTempAfter" : 0


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

    setDisplay(osc, 1, settings["oscVoltageRange"], settings["timeRange"], settings["peakHeight"])
    print("Oscilloscope display set.")
    osc.write(":RUN")

    runTime = settings["runTimeSeconds"]
    startTime = time()
    i = 1
    negtime = 0
    darkCounts = -1
    while (time() - startTime) < runTime:
        osc.write(":TER?")
        trigger = osc.read().strip()
        before = time()
        if trigger == "+1":
            darkCounts += 1
            
            #saveData(osc, settings["fileName"]+str(i), "Temp files for dark count rate", True)
            i += 1
        after = time()
        #if trigger == "+0":
        #    negtime -= after - before
        negtime += after - before
    negtime -= after - before
    numberOfDatasets = i
    sour.write("SOUR:VOLT:STAT OFF")
    print("dark counts:", darkCounts)
    print("dark count rate:", darkCounts / runTime)
    return [numberOfDatasets - 1, settings["runTimeSeconds"]]


def deleteTemp(settings, numberOfDatasets: list):
    i = 1
    try:
        while i <= numberOfDatasets[0]:
            os.remove("./dataCollection/"+str(settings["pathNameDate"])+"/Temp/"+str(settings["fileName"])+str(i)+".csv")
            i += 1
    except FileNotFoundError as e:
        print("File not found")
 


def peakCounter(settings, numberOfDatasets: list):

    timedic = {}
    voltdic = {}
    i = 1
    try:
        while i <= numberOfDatasets[0]:
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
            plt.plot(voltdic[key])
        print(f"{darkCounts} dark counts in "+str(numberOfDatasets[1])+" seconds.")
        darkCountRate = darkCounts / numberOfDatasets[1]
        print(f"Dark count rate {darkCountRate} Hz")
        plt.show()
    except FileNotFoundError as e:
        print("File not found")
        return


def runAnalyze(settings):

    if settings["aquireData"]:
        sets = aquireData(settings)

    if settings["countPeaks"]:
        peakCounter(settings, sets)

    if settings["deleteTempAfter"]:
        deleteTemp(settings, sets)


runAnalyze(settings)