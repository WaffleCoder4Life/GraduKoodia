import numpy as np
import os


def saveData(instrument, fileName: str, testDescribtion: str, measSettings: str = ""):
    """Reads binary data from instrument, and formats it to voltages. 
    Appends measurement data and used settings to file 'fileName'.csv. 
    Adds test describtion and settings to beginning of each dataset.\n
    Measurement settings must be defined in program (setDisplay and generatePulses return their settings as str)."""
    path = "./dataCollection/"+str(fileName)+".csv"
    if os.path.isfile(path):
        print("Filename taken (csv)")
    else:
        timeScale = float(instrument.query(":TIMebase:RANGE?"))
        yIncrement = float(instrument.query(":WAVeform:YINCREMENT?"))
        yOrigin = float(instrument.query("WAVeform:YORIGIN?"))
        dataList = []
        #instrument.write(":DIGitize") #The :DIGitize command is a specialized RUN command. Stops when data aqusition is complete.
        values = instrument.query_binary_values(":WAVeform:DATA?", datatype = "B") #The :WAVeform:DATA query returns the binary block of sampled data points transmitted using the IEEE 488.2 arbitrary block data format.
        for value in values:
            #Scales binary data to volts.
            dataList.append((value-128)*yIncrement+yOrigin)
        time = np.linspace(0, timeScale, len(dataList)) #Time axis
        with open("./dataCollection/"+fileName + ".csv", "a") as file:
            #Saves voltage [V] and time [s] values to file as string separated by ';'.
            i=0
            file.write(testDescribtion + "\n" + "Measurement settings: " + measSettings + "\n"
                    +"Timescale: " + str(timeScale) + " s, y-increment: " + str(yIncrement)
                    + ", y-origin: " + str(yOrigin) + "\nVoltage = (value-128)*yIncrement+yOrigin, [value] = byte\n Time [s], Voltage [V]")
            while i < len(dataList):
                file.write(str(time[i])+";"+str(dataList[i])+"\n")
                i+=1