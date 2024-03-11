import time
import os


def voltageSweep(instrument, voltageRange: float, startVoltage_V: float, endVoltage_V: float, currentLimit_A: float, fileName: str, testDescribtion: str, reverse: bool = False):
    """Performs voltage step sweep with given settings, and saves the setting and measured voltage, current and resistance to 'fileName'.csv to DataCollection folder\n
    Data is appended to file and test describtion is written to the beginning of dataset."""
    i = 1
    #Check if filename taken
    path = "./dataCollection/"+str(fileName)+".csv"
    if os.path.isfile(path):
        print("Filename taken (csv)")
        choice = input("Do you want to override? y/n")
        if choice == "y":
            os.remove(path)
        else:
            i = 0

    if i == 1:
        instrument.write(":SOUR:FUNC VOLT")

        
        instrument.write(":SOUR:VOLT:RANG " + str(voltageRange))  # Set voltage range
        instrument.write(":SENS:CURR:PROT " + str(currentLimit_A)) # Set the maximum current limit
        instrument.write(":SENS:CURR:RANG 1E-5") #set current measurement range

        voltage_step = 0.05
        sweepPoints = (endVoltage_V-startVoltage_V)/voltage_step

        


        
        instrument.write(":OUTP ON")
        time.sleep(1)

        with open("./dataCollection/" + fileName + ".csv", "a") as file:
            file.write(testDescribtion + "\n Sweep settings: Start voltage: "+str(startVoltage_V)+" V, end voltage:  "+str(endVoltage_V)+" V, sweep points: "+str(sweepPoints)+", current limit: "+str(currentLimit_A)+" A\n U/V, I/A, R/Ohm\n")
            if reverse:
                voltage = endVoltage_V
                temp = []
                while voltage >= startVoltage_V:
                    instrument.write(":SOUR:VOLT " + str(voltage))  # Set voltage
                    time.sleep(0.2)
                    instrument.write(":FORM:ELEM VOLT, CURR, RES")
                    temp.append(instrument.read())
                    voltage -= voltage_step
                temp.reverse()
                for t in temp:
                    file.write(t)
            else:
                voltage = startVoltage_V
                while voltage <= endVoltage_V:
                    instrument.write(":SOUR:VOLT " + str(voltage))  # Set voltage
                    time.sleep(0.2)
                    instrument.write(":FORM:ELEM VOLT, CURR, RES")
                    file.write(instrument.read())
                    
                    voltage += voltage_step

        instrument.write(":OUTP OFF")
    

        
        