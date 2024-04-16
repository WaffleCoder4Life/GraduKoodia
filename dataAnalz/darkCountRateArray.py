import readOscilloscopeData as rod
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pyvisa as visa
from deviceControl import setDisplay, setVoltageFine, saveData
import os
import time as t
from time import time
from datetime import date
import numpy as np

# RUNTIME: measuring t second interval takes t*4200 seconds. t_interval = numberOfDatasets*runTimes*timeRange. E.g. 1 s time interval can be measured with 1000 datasets and 50 runTimes if timeRange is 20E-6. 


settings = {
    "pathNameDate" : "11042024",
    "fileName" : "darkcountTemp",
    "numberOfDatasets" : 1000, # Runtime is numberOfDatasets * timeRange * 10 000. Starts lagging with too big datasets.
    "runTimes" : 5, # Runs measurement this many times, used to avoid list overflows. Total measurement interval is
    "biasVoltageRange" : 50,
    "biasVoltage" : 23.5,
    "biasCurrentLimit" : 2.5E-3,
    "timeRange" : 20E-6, # Sets oscilloscope screen width. 20E-6 is good value to use in room temp.
    "peakHeight" : 0.04, # Check before measurement. Example if single peak height is 70 mV, then 0.05 is good value to use.
    "peakDistance" : 300, # Check before measurement with testSingleShot. 40 000 datapoints and 300 works fine.
    "aquireData" : 1, # Aquires data and prints out dark count rate.
    "testSingleShot" : 0,
 }


def testSingleShot(settings):
    """Used to test manually if counts correct amount of counts from single oscilloscope screen. Use to calibrate peak finder peak distance.
       Note that oscilloscope screen might not show the peaks just after the screen that still trigger the count."""
    #VISA CONNECTIONS
    rm = visa.ResourceManager()
    list = rm.list_resources()
    osc = rm.open_resource('USB0::0x2A8D::0x1797::CN56396144::INSTR') #Oscilloscope
    # Set all measurement options only once and before the while loop

    yIncrement = float(osc.query(":WAVeform:YINCREMENT?"))
    yOrigin = float(osc.query("WAVeform:YORIGIN?"))
    osc.write("WAV:POIN 40000")
    binaryDataList = []
    
  
    binaryDataList.append(osc.query_binary_values(":WAVeform:DATA?", datatype = "B")) # Creates a list of lists with binary data read from oscilloscope. Runtime < 0.1 s, 80 000 datapoints

    print(len(binaryDataList[0]))

    dataList = []
    
    for value in binaryDataList[0]:
        #Scales binary data to volts.
        dataList.append((value-128)*yIncrement+yOrigin) # Scales binary data to voltages
    peaks = find_peaks(dataList, settings["peakHeight"], distance = settings["peakDistance"]) 
    darkCounts = len(peaks[0])
    print(str(darkCounts) + " dark counts in single screen")
    print(f"Peak locations are {peaks[0]}")
    osc.close()


def aquireData(settings):
    """Takes numberOfDatasets times a single shot from oscilloscope and saves the data to pathNameData/Temp/ folder. (remember to make)"""

    #VISA CONNECTIONS
    rm = visa.ResourceManager()
    list = rm.list_resources()
    osc = rm.open_resource('USB0::0x2A8D::0x1797::CN56396144::INSTR') # Connect oscilloscope
    
    sour = rm.open_resource("GPIB0::22::INSTR") # Connect source
    sour.write("*RST")  # Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
    sour.write("SYST:ZCH OFF") # Turn off zero corrections
    sour.write(":SENS:RANG 0.00001") # SET CURRENT MEASURE RANGE (not needed but stops the device from clicking)
    setVoltageFine(sour, settings["biasVoltageRange"], settings["biasVoltage"], settings["biasCurrentLimit"])
    print("Bias voltage set.")

    setDisplay(osc, 1, 800E-3, settings["timeRange"], 0)
    print("Oscilloscope display set.")
    osc.write(":RUN")
    osc.write("CHAN1:DISP 1")



    # Set all measurement options only once and before the while loop
    t.sleep(2)
    j = 1
    averageDarkRate = 0
    
    yIncrement = float(osc.query(":WAVeform:YINCREMENT?"))
    yOrigin = float(osc.query("WAVeform:YORIGIN?"))
    osc.write("WAV:POIN 40000")

    
    
    while j <= settings["runTimes"]:
        before = time()
        i = 0
        arraySize = settings["numberOfDatasets"]
        binaryDataArray = np.empty((arraySize, 40000))
        while i < settings["numberOfDatasets"]:
            #saveData(osc, settings["fileName"]+str(i), "Temp files for dark count rate", True) # Runtime 0.45 s for single save data

            # Trying optimized versions for saving data
            binaryDataArray[i] = osc.query_binary_values(":WAVeform:DATA?", datatype = "B") # Creates a list of lists with binary data read from oscilloscope. Runtime < 0.1 s, 80 000 datapoints
            i += 1
        
        
        
        after = time()
        before2 = time()
        print(len(binaryDataArray[0]))
        
        binaryDataArray = ((binaryDataArray-128)*yIncrement+yOrigin)

        """ i = 0
        dataList = []
        while i < settings["numberOfDatasets"]:
            for value in binaryDataList[i]:
                #Scales binary data to volts.
                dataList.append((value-128)*yIncrement+yOrigin) # Scales binary data to voltages
            i += 1 """
        i = 0
        darkCounts = 0
        while i < arraySize:
            peaks = find_peaks(binaryDataArray[i], settings["peakHeight"], distance = settings["peakDistance"]) 
            darkCounts += len(peaks[0])
            i += 1
        after2 = time()
        print(str(darkCounts) + " dark counts in "+str(settings["numberOfDatasets"])+" datasets.")
        measurementTime = settings["numberOfDatasets"] * settings["timeRange"]
        darkCountRate = darkCounts / measurementTime
        print("Mesurement took " +str(after-before)+" seconds to measure an interval of " + str(measurementTime) + " seconds. Data analyse took "+str(after2-before2)+" seconds.")
        print(f"Dark count rate is {darkCountRate} Hz and {darkCountRate/9.4249} Hz/mm\N{SUPERSCRIPT TWO}.")
        averageDarkRate += darkCountRate
        j += 1
    averageDarkRate /= settings["runTimes"]
    totalMeasurementTime = measurementTime * settings["runTimes"]
    print("Dark count rate from "+str(settings["runTimes"])+" runs with "+str(settings["numberOfDatasets"])+" datasets each is "+str(averageDarkRate)+f" Hz and {averageDarkRate/9.4249} Hz/mm\N{SUPERSCRIPT TWO}.\nTime interval measured is {totalMeasurementTime} seconds.")
    sour.write("SOUR:VOLT:STAT OFF")

    osc.close()
    sour.close()





def runAnalyze(settings):

    if settings["aquireData"]:
        aquireData(settings)

    if settings["testSingleShot"]:
        testSingleShot(settings)

runAnalyze(settings)