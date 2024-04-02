import readOscilloscopeData as rod
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pyvisa as visa
from deviceControl import setDisplay, setVoltageFine, saveData
import os
import time as t
from time import time
from datetime import date

# RUNTIME: measuring t second interval takes t*10000 seconds


settings = {
    "pathNameDate" : "02042024",
    "fileName" : "darkcountTemp",
    "numberOfDatasets" : 100, # Runtime is numberOfDatasets * timeRange * 10 000. Starts lagging with too big datasets.
    "biasVoltageRange" : 50,
    "biasVoltage" : 26.7,
    "biasCurrentLimit" : 2.5E-3,
    "timeRange" : 20E-6, # Sets oscilloscope screen width. 20E-6 is good value to use
    "peakHeight" : 0.06, # Check before measurement. Example if single peak height is 70 mV, then 0.05 is good value to use.
    "aquireData" : 0, # Aquires data and prints out dark count rate.
    "testSingleShot" : 1,
 


}


def testSingleShot(settings):
    """Used to test manually if counts correct amount of counts from single oscilloscope screen."""
    #VISA CONNECTIONS
    rm = visa.ResourceManager()
    list = rm.list_resources()
    osc = rm.open_resource(list[0])
    # Set all measurement options only once and before the while loop

    yIncrement = float(osc.query(":WAVeform:YINCREMENT?"))
    yOrigin = float(osc.query("WAVeform:YORIGIN?"))
    osc.write("WAV:POIN MAX")
    binaryDataList = []
    
  
    binaryDataList.append(osc.query_binary_values(":WAVeform:DATA?", datatype = "B")) # Creates a list of lists with binary data read from oscilloscope. Runtime < 0.1 s, 80 000 datapoints

    print(len(binaryDataList[0]))

    dataList = []
    
    for value in binaryDataList[0]:
        #Scales binary data to volts.
        dataList.append((value-128)*yIncrement+yOrigin) # Scales binary data to voltages
    distance = len(binaryDataList) / settings["timeRange"] * 100e-9 # Datapoints = len(binaryDataList[0]), pulse relaxation time to half amplitude = 100 ns (Onsemi), distance = datapoints / timerange * t_relax
    print(f"Peak finder distance is {distance}")
    peaks = find_peaks(dataList, settings["peakHeight"], distance = 1600) 
    darkCounts = len(peaks[0])
    print(str(darkCounts) + " dark counts in single screen")
    osc.close()


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

    setDisplay(osc, 1, 800E-3, settings["timeRange"], 0)
    print("Oscilloscope display set.")
    osc.write(":RUN")
    i = 1
    osc.write("CHAN1:DISP 1")



    # Set all measurement options only once and before the while loop
    t.sleep(2)

    yIncrement = float(osc.query(":WAVeform:YINCREMENT?"))
    yOrigin = float(osc.query("WAVeform:YORIGIN?"))
    osc.write("WAV:POIN MAX")
    binaryDataList = []
    
    before = time()
    while i <= settings["numberOfDatasets"]:
        #saveData(osc, settings["fileName"]+str(i), "Temp files for dark count rate", True) # Runtime 0.45 s for single save data

        # Trying optimized versions for saving data
        binaryDataList.append(osc.query_binary_values(":WAVeform:DATA?", datatype = "B")) # Creates a list of lists with binary data read from oscilloscope. Runtime < 0.1 s, 80 000 datapoints
        i += 1

    sour.write("SOUR:VOLT:STAT OFF")
    after = time()
    print(len(binaryDataList[0]))
    i = 0
    dataList = []
    while i < settings["numberOfDatasets"]:
        for value in binaryDataList[i]:
            #Scales binary data to volts.
            dataList.append((value-128)*yIncrement+yOrigin) # Scales binary data to voltages
        i += 1
    distance = len(binaryDataList[0]) / settings["timeRange"] * 100e-9 # Datapoints = len(binaryDataList[0]), pulse relaxation time to half amplitude = 100 ns (Onsemi), distance = datapoints / timerange * t_relax
    print(f"Peak finder distance is {distance}")
    peaks = find_peaks(dataList, settings["peakHeight"], distance = 1600) 
    darkCounts = len(peaks[0])
    after2 = time()
    print(str(darkCounts) + " dark counts in "+str(settings["numberOfDatasets"])+" datasets.")
    measurementTime = settings["numberOfDatasets"] * settings["timeRange"]
    darkCountRate = darkCounts / measurementTime
    print("Mesurement took " +str(after-before)+" seconds to measure an interval of " + str(measurementTime) + "seconds. Data analyse took "+str(after2-before)+" seconds.")
    print(f"Dark count rate is {darkCountRate} Hz and {darkCountRate/9.4249} Hz/mm\N{SUPERSCRIPT TWO}.")
    osc.close()
    sour.close()





def runAnalyze(settings):

    if settings["aquireData"]:
        aquireData(settings)

    if settings["testSingleShot"]:
        testSingleShot(settings)

runAnalyze(settings)