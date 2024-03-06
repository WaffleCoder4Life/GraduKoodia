import pyvisa as visa
from Keithley import setVoltage as sv
import KeySightConn.generatePulses as gen
import KeySightConn.saveData as save
import KeySightConn.setDisplay as set
import Keithley.voltageSweep as vs


print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
sour = rm.open_resource(list[2])
osc.write("*IDN?")
print(osc.read())

set.setDisplay(osc, 1, 0.008, 0.5, 0)
#set.setDisplay(osc, 2, 16, 10000000, 0)

osc.write(":RUN")

#gen.generatePulses(osc, 1, 5, 0.5)



sv.setVoltage(sour, 1000, 25, 0.0150)