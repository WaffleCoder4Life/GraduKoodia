import numpy as np
import os
from datetime import date
from scipy.signal import find_peaks

def saveData(instrument, fileName: str, testDescribtion: str, temp: bool, measSettings: str = ""):
    """Reads binary data from instrument, and formats it to voltages. 
    Appends measurement data and used settings to file 'fileName'.csv. 
    Adds test describtion and settings to beginning of each dataset.\n
    Measurement settings must be defined in program (setDisplay and generatePulses return their settings as str)."""

    dateAsList = str(date.today()).split("-")
    today = ""
    j = 2
    while j >= 0:
        today += dateAsList[j]
        j -= 1
    if temp:
        today += "/Temp"
    path = "./dataCollection/"+str(today)+"/"+str(fileName)+".csv"
    if os.path.isfile(path):
        print("Filename taken (csv)")
    else:
        timeScale = float(instrument.query(":TIMebase:RANGE?"))
        yIncrement = float(instrument.query(":WAVeform:YINCREMENT?"))
        yOrigin = float(instrument.query("WAVeform:YORIGIN?"))
        instrument.write("WAV:POIN MAX")
        dataList = []
        #instrument.write(":DIGitize") #The :DIGitize command is a specialized RUN command. Stops when data aqusition is complete.
        values = instrument.query_binary_values(":WAVeform:DATA?", datatype = "B") #The :WAVeform:DATA query returns the binary block of sampled data points transmitted using the IEEE 488.2 arbitrary block data format.
        for value in values:
            #Scales binary data to volts.
            dataList.append((value-128)*yIncrement+yOrigin)
        time = np.linspace(0, timeScale, len(dataList)) #Time axis
        with open("./dataCollection/"+str(today)+"/"+fileName + ".csv", "a") as file:
            #Saves voltage [V] and time [s] values to file as string separated by ';'.
            i=0
            file.write(testDescribtion + "\n" + "Measurement settings: " + measSettings + "\n"
                    +"Timescale: " + str(timeScale) + " s, y-increment: " + str(yIncrement)
                    + ", y-origin: " + str(yOrigin) + "\nVoltage = (value-128)*yIncrement+yOrigin, [value] = byte\n Time [s], Voltage [V]")
            while i < len(dataList):
                file.write(str(time[i])+";"+str(dataList[i])+"\n")
                i+=1




#Display settings, Channel range 8 div, timebase range 10 div


def setDisplay(instrument, chan: int, voltageRange_V: float, timeRange_s: float, triggerLevel_V: float) -> str:
    """Sets voltage and time ranges, and DC trigger level for KeySight oscilloscope's display, 
    and returns these settings as a string. voltageRange allowed values [8mV - 40V]"""
    instrument.write(":TRIGger:SOURce CHANnel" + str(chan))
    instrument.write(":TRIGger:MODE EDGE") #NEEDS TESTING
    instrument.write(":TRIGger:COUPling DC") #NEEDS TESTING
    instrument.write(":CHANnel" + str(chan) + ":RANGe " + str(voltageRange_V))
    instrument.write(":TIMebase:RANGe " + str(timeRange_s))
    instrument.write(":TRIGger:LEVel " + str(triggerLevel_V))
    instrument.write(":CHANnel" + str(chan) + ":DISPlay 1")

    settings = "Voltage range: " + str(voltageRange_V) + " V, Time range: " + str(timeRange_s) + " s, Trigger level: " + str(triggerLevel_V) + "V"

    return settings


def countPeaks(data: list, h: float, d, p = 0.05) -> int:
    """data, peak height V -> number of peaks"""

    x = np.array(data)

    peaks, _ = find_peaks(x, height = h, distance=d, prominence=p)
    return len(peaks)








def setVoltageFine(instrument, voltageRange: float, voltage_V: float, currentLimit_A: float):
    """Set bias voltage range, voltage, current limit and turn output ON"""

    instrument.write(":SOUR:VOLT:RANG "+str(voltageRange))  # Set voltage range, 10 V, 50 V, 100 V
    instrument.write(":SOUR:VOLT:ILIM "+str(currentLimit_A)) #SET CURRENT LIMIT
    instrument.write(":SOUR:VOLT "+str(voltage_V)) #SET VOLTAGE
    instrument.write(":SOUR:VOLT:STAT ON") #OUTPUT ON 