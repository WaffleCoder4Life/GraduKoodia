import time
import os
from datetime import date

def voltageSweepAverage(instrument, voltageRange: float, startVoltage_V: float, endVoltage_V: float, currentLimit_A: float, fileName: str, measurementsPerVoltage: int, voltageStep: float, testDescribtion: str, reverse: bool = False):
    """Performs voltage step sweep with given settings, and saves the setting and measured voltage, current and resistance to 'fileName'.csv to DataCollection folder\n
    Data is appended to file and test describtion is written to the beginning of dataset. Voltage range allowed 10 V, 50 V, 100 V. Use 50 V for 1 mV sweep steps."""
    i = 1

    #CHECK FILE NAME NOT TAKEN AND SAVE TO CORRECT FOLDER
    dateAsList = str(date.today()).split("-")
    today = ""
    j = 2
    while j >= 0:
        today += dateAsList[j]
        j -= 1
    #Check if filename taken
    path = "./dataCollection/"+str(today)+"/"+str(fileName)+".csv"
    if os.path.isfile(path):
        print("Filename taken (csv)")
        choice = input("Do you want to override? y/n")
        if choice == "y":
            os.remove(path)
        else:
            i = 0

    if i == 1:
        
        instrument.write(":SOUR:VOLT:RANG " + str(voltageRange))  # Set voltage range
        instrument.write(":SOUR:VOLT:ILIM " + str(currentLimit_A)) # Set the maximum current limit
        #instrument.write(":SENS:CURR:RANG 1E-5") #set current measurement range

        
        voltage_step = voltageStep #SMALLEST ALLOWED VALUE 0.001 FOR 50 V RANGE

        instrument.write(":SENS:RANG 0.00001")
        
        

        sweepPoints = (endVoltage_V-startVoltage_V)/voltage_step




    
        instrument.write(":SOUR:VOLT:STAT ON") #OUTPUT ON
        time.sleep(1) 
        
        with open("./dataCollection/" + today +"/" + fileName + ".csv", "a") as file:
            file.write(testDescribtion + "\n Sweep settings: Start voltage: "+str(startVoltage_V)+" V, end voltage:  "+str(endVoltage_V)+" V, sweep points: "+str(sweepPoints)+", current limit: "+str(currentLimit_A)+" A\n U/V, I/A, R/Ohm\n")
            if reverse:
                voltage = endVoltage_V
                instrument.write(":FORM:ELEM READ") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
                instrument.write(":FORM:DATA ASCii") #CHOOSE DATA FORMAT
                temp = []
                while voltage >= startVoltage_V:
                    instrument.write(":SOUR:VOLT " + str(voltage))  # Set voltage
                    time.sleep(3)
                    i = 0
                    tempCurr = []
                    while i < measurementsPerVoltage:
                        time.sleep(0.1)                    
                        instrument.write(":INIT") #TRIGGER MEASUREMENT
                        instrument.write(":SENS:DATA?") #ASK FOR DATA
                        tempCurr.append(float(instrument.read())) #READ DATA
                        i += 1
                    currAveg = 0
                    for curr in tempCurr:
                        currAveg += curr
                    currAveg = currAveg/len(tempCurr)
                    temp.append(str(voltage)+","+str(currAveg))
                    voltage -= voltage_step
                temp.reverse()
                for t in temp:
                    file.write(t+"\n")
            else:
                voltage = startVoltage_V
                instrument.write(":FORM:ELEM READ") #IF 'ALL' -> CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE. 'READ,VSO' -> CURRENT, SOURCE VOLTAGE
                instrument.write(":FORM:DATA ASCii") #CHOOSE DATA FORMAT
                while voltage <= endVoltage_V:
                    instrument.write(":SOUR:VOLT " + str(voltage))  # Set voltage
                    time.sleep(3) #Wait after setting voltage
                    i = 0
                    tempCurr = []
                    while i < measurementsPerVoltage:
                        time.sleep(0.1)
                        instrument.write(":INIT") #TRIGGER MEASUREMENT
                        instrument.write(":SENS:DATA?") #ASK FOR DATA
                        tempCurr.append(float(instrument.read()))
                        i += 1
                    currAveg = 0
                    for curr in tempCurr:
                        currAveg += curr
                    currAveg = currAveg/len(tempCurr)
                    file.write(str(voltage)+","+str(currAveg)+"\n")
                    voltage += voltage_step

        instrument.write(":SOUR:VOLT:STAT OFF") #OUTPUT OFF