import setVoltage as sv
import pyvisa as visa


rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instrument = rm.open_resource(list[2])



instrument.write(":SOUR:FUNC VOLT")

instrument.write(":SOUR:VOLT:RANG 1000" )  # Set voltage range
instrument.write(":SENS:CURR:PROT 0.015") # Set the maximum current limit



instrument.write(":SOUR:VOLT 20")  # Set voltage

instrument.write(":OUTP ON")