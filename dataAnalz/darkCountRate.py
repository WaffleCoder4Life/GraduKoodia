import readOscilloscopeData as rod
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pyvisa as visa
from deviceControl import setDisplay, setVoltageFine, saveData
import os

settings = {
    "pathNameDate" : "20032024",
    "fileName" : "darkcountTemp",
    "numberOfDatasets" : 1000,
    "biasVoltageRange" : 50,
    "biasVoltage" : 24,
    "biasCurrentLimit" : 2.5E-3,
    "timeRange" : 100E-6,
    "peakHeight" : 0.002,
    "aquireData" : 1,
    "countPeaks" : 1,
    "deleteTempAfter" : 1


}




def aquireData(settings):
    """Takes numberOfDatasets times a single shot from oscilloscope and saves the data to pathNameData/Temp/ folder. (remember to make)"""

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

    setDisplay(osc, 1, 16E-3, settings["timeRange"], 0)
    print("Oscilloscope display set.")
    osc.write(":RUN")
    i = 1
    osc.write("CHAN1:DISP 1")
    while i <= settings["numberOfDatasets"]:
        saveData(osc, settings["fileName"]+str(i), "Temp files for dark count rate", True)
        i += 1
    sour.write("SOUR:VOLT:STAT OFF")
    #osc.close()
    #sour.close()


def deleteTemp(settings):
    i = 1
    while i <= settings["numberOfDatasets"]:
        os.remove("./dataCollection/"+str(settings["pathNameDate"])+"/Temp/"+str(settings["fileName"])+str(i)+".csv")
        i += 1

def peakCounter(settings):

    timedic = {}
    voltdic = {}
    i = 1
    while i <= settings["numberOfDatasets"]:
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
    print(f"{darkCounts} dark counts in "+str(settings["numberOfDatasets"])+" datasets.")
    darkCountRate = darkCounts / (10*settings["timeRange"]*settings["numberOfDatasets"])
    print(f"Dark count rate {darkCountRate} Hz")
    #plt.show()


def runAnalyze(settings):

    if settings["aquireData"]:
        aquireData(settings)

    if settings["countPeaks"]:
        peakCounter(settings)

    if settings["deleteTempAfter"]:
        deleteTemp(settings)


runAnalyze(settings)