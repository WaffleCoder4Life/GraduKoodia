import time
import os
from datetime import date

def voltageSweepFine(instrument, voltageRange: float, startVoltage_V: float, endVoltage_V: float, currentLimit_A: float, fileName: str, testDescribtion: str, reverse: bool = False):
    """Performs voltage step sweep with given settings, and saves the setting and measured voltage, current and resistance to 'fileName'.csv to DataCollection folder\n
    Data is appended to file and test describtion is written to the beginning of dataset. Voltage range allowed 10 V, 50 V, 100 V. Use 50 V for 1 mV sweep steps."""
    i = 1

    dateAsList = str(date.today()).split("-")
    today = ""
    j = 2
    while j >= 0:
        today += dateAsList[j]
        j -= 1
    #Check if filename taken
    path = "./dataCollection/"+str(today)+str(fileName)+".csv"
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

        
        voltage_step = 0.05 #SMALLEST ALLOWED VALUE 0.001 FOR 50 V RANGE

        instrument.write(":SENS:RANG 0.00001")
        
        

        sweepPoints = (endVoltage_V-startVoltage_V)/voltage_step




    
        instrument.write(":SOUR:VOLT:STAT ON") #OUTPUT ON
        time.sleep(1) 
        
        with open("./dataCollection/" + today +"/" + fileName + ".csv", "a") as file:
            file.write(testDescribtion + "\n Sweep settings: Start voltage: "+str(startVoltage_V)+" V, end voltage:  "+str(endVoltage_V)+" V, sweep points: "+str(sweepPoints)+", current limit: "+str(currentLimit_A)+" A\n U/V, I/A, R/Ohm\n")
            if reverse:
                voltage = endVoltage_V
                temp = []
                while voltage >= startVoltage_V:
                    instrument.write(":SOUR:VOLT " + str(voltage))  # Set voltage
                    time.sleep(0.2)
                    instrument.write(":FORM:ELEM READ") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
                    instrument.write(":FORM:DATA ASCii") #CHOOSE DATA FORMAT
                    instrument.write(":INIT") #TRIGGER MEASUREMENT
                    instrument.write(":SENS:DATA?") #ASK FOR DATA
                    temp.append(str(voltage)+","+instrument.read()) #READ DATA
                    voltage -= voltage_step
                temp.reverse()
                for t in temp:
                    file.write(t)
            else:
                voltage = startVoltage_V
                while voltage <= endVoltage_V:
                    instrument.write(":SOUR:VOLT " + str(voltage))  # Set voltage
                    time.sleep(0.2)
                    instrument.write(":FORM:ELEM READ") #IF 'ALL' -> CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE. 'READ,VSO' -> CURRENT, SOURCE VOLTAGE
                    instrument.write(":FORM:DATA ASCii") #CHOOSE DATA FORMAT
                    instrument.write(":INIT") #TRIGGER MEASUREMENT
                    instrument.write(":SENS:DATA?") #ASK FOR DATA
                    data = str(voltage)+","+instrument.read()
                    file.write(data) #READ DATA
                    voltage += voltage_step

        instrument.write(":SOUR:VOLT:STAT OFF") #OUTPUT OFF
    

        
        