import pyvisa as visa

def setVoltage(instrument,voltageRange: float, voltage_V: float, currentLimit_A: float):

    instrument.write(":SOUR:FUNC VOLT")

    instrument.write(":SOUR:VOLT:RANG " + str(voltageRange))  # Set voltage range
    instrument.write(":SENS:CURR:PROT " + str(currentLimit_A)) # Set the maximum current limit

    voltage = voltage_V / voltageRange

    instrument.write(":SOUR:VOLT " + str(voltage))  # Set voltage

    instrument.write(":OUTP ON")
