




def setVoltageFine(instrument, voltageRange: float, voltage_V: float, currentLimit_A: float):

    instrument.write(":SOUR:VOLT:RANG "+str(voltageRange))  # Set voltage range, 10 V, 50 V, 100 V
    instrument.write(":SOUR:VOLT:ILIM "+str(currentLimit_A)) #SET CURRENT LIMIT
    instrument.write(":SOUR:VOLT "+str(voltage_V)) #SET VOLTAGE
    instrument.write(":SOUR:VOLT:STAT ON") #OUTPUT ON 