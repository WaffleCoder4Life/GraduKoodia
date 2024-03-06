import pyvisa as visa
from Keithley import setVoltage as sv
from KeySightConn import setDisplay as sd
from KeySightConn import saveData as SD


def darkCountSweep(instrument, voltageRange_V: float, startVoltage_V: float, stopVoltage_V: float, sweepPoints: int, currentLimit_A: float, fileName: str, testDescription: str):
    instrument.write(":SOUR:FUNC VOLT")

    
    instrument.write(":SOUR:VOLT:RANG " + str(voltageRange_V))  # Set voltage range
    instrument.write(":SENS:CURR:PROT " + str(currentLimit_A)) # Set the maximum current limit

    voltage = startVoltage_V

    instrument.write(":OUTP ON")

    with open("./dataCollection/" + fileName + ".csv", "a") as file:
        file.write(testDescription + "\n Sweep settings: Start voltage: "+str(startVoltage_V)+" V, end voltage:  "+str(stopVoltage_V)+" V, sweep points: "+str(sweepPoints)+", current limit: "+str(currentLimit_A)+" A\n t/s, U/V\n")
        
