import pyvisa as visa
import KeySightConn.USABLE.generatePulses as gen
import KeySightConn.USABLE.saveData as save
import KeySightConn.USABLE.setDisplay as set
import Keithley.voltageSweep as vs
import Keithley.setVoltage as sv



print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
sour = rm.open_resource(list[2])
#osc.write("*IDN?")
#print(osc.read())

set.setDisplay(osc, 1, 0.008, 5000000, 0.001)
set.setDisplay(osc, 2, 24, 5000000, 1)

osc.write(":RUN")

gen.generatePulses(osc, 1, 3, 0.5)





sv.setVoltage(sour, 1000, 27, 0.015)