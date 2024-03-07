import time



def voltageSweep(instrument, voltageRange: float, startVoltage_V: float, endVoltage_V: float, sweepPoints: int, currentLimit_A: float, fileName: str, testDescribtion: str):
    """Performs voltage step sweep with given settings, and saves the setting and measured voltage, current and resistance to 'fileName'.csv to DataCollection folder\n
    Data is appended to file and test describtion is written to the beginning of dataset."""


    instrument.write(":SOUR:FUNC VOLT")

    
    instrument.write(":SOUR:VOLT:RANG " + str(voltageRange))  # Set voltage range
    instrument.write(":SENS:CURR:PROT " + str(currentLimit_A)) # Set the maximum current limit

    voltage_step = (endVoltage_V-startVoltage_V)/sweepPoints

    

    voltage = startVoltage_V
    
    instrument.write(":OUTP ON")

    with open("./dataCollection/" + fileName + ".csv", "a") as file:
        file.write(testDescribtion + "\n Sweep settings: Start voltage: "+str(startVoltage_V)+" V, end voltage:  "+str(endVoltage_V)+" V, sweep points: "+str(sweepPoints)+", current limit: "+str(currentLimit_A)+" A\n U/V, I/A, R/Ohm\n")
        while voltage <= endVoltage_V:
            instrument.write(":SOUR:VOLT " + str(voltage))  # Set voltage
            time.sleep(0.2)
            instrument.write(":FORM:ELEM VOLT, CURR, RES")
            file.write(instrument.read())
            
            voltage += voltage_step

    instrument.write(":OUTP OFF")

        
        