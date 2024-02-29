import pyvisa as visa
import KeySightConn.USABLE.generatePulses as gen
import KeySightConn.USABLE.saveData as save
import KeySightConn.USABLE.setDisplay as set
import Keithley.voltageSweep as vs



print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
osc.write("*IDN?")
print(osc.read())

set.setDisplay(osc, 2, 4, 5000000, 0.25)
set.setDisplay(osc, 1, 4, 5000000, 0.25)

osc.write(":RUN")

gen.generatePulses(osc, 1, 3, 0.5)



sour = rm.open_resource(list[2])

