import numpy as np


def saveData(instrument, fileName: str, testID: str, measSettings: str = None):
    """Reads binary data from instrument, and formats it to voltages. 
    Appends measurement data and used settings to file 'fileName'.csv. 
    Adds testID and settings to beginning of each dataset.\n
    Measurement settings must be defined in program (setDisplay and generatePulses return their settings as str)."""
    time_scale = float(instrument.query(":TIMebase:RANGE?"))
    yIncrement = float(instrument.query(":WAVeform:YINCREMENT?"))
    yOrigin = float(instrument.query("WAVeform:YORIGIN?"))
    dataList = []
    instrument.write(":DIGitize")
    values = instrument.query_binary_values(":WAVeform:DATA?", datatype = "B")
    for value in values:
        dataList.append((value-128)*yIncrement+yOrigin)
    print(len(dataList))
    time = np.linspace(0, time_scale, len(dataList))
    with open(fileName + ".csv", "a") as file:
        i=0
        file.write("\n\nNEW MEASUREMENT\n\n")
        file.write(testID + "\n" + "Measurement settings: " + measSettings + "\n"
                   +"Timescale: " + str(time_scale) + " s, y-increment: " + str(yIncrement)
                   + ", y-origin: " + str(yOrigin) + "\nVoltage = (value-128)*yIncrement+yOrigin, [value] = byte")
        while i < len(dataList):
            file.write(str(dataList[i])+";"+str(time[i])+"\n")
            i+=1