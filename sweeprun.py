import pyvisa as visa
import KeySightConn.generatePulses as gen
import KeySightConn.saveData as save
import KeySightConn.setDisplay as set
import Keithley.voltageSweep as vs
import Keithley.setVoltage as sv



print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
sour = rm.open_resource(list[2])
osc.write("*IDN?")
print(osc.read())

set.setDisplay(osc, 1, 0.008, 0.5, 0)
set.setDisplay(osc, 2, 24, 5000000, 1)

osc.write(":RUN")





sv.setVoltage(sour, 1000, 10, 0.0150)

vs.voltageSweep(sour, 1000, 20, 30, 100, 0.0150, "test3_1_3_24", "BoxNoCover")





