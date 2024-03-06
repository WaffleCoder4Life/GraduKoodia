import pyvisa as visa
from Keithley import setVoltage as sv
import KeySightConn.generatePulses as gen
import KeySightConn.saveData as save
import KeySightConn.setDisplay as set
import Keithley.voltageSweep as vs
import keyboard
import time


print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
sour = rm.open_resource(list[2])
osc.write("*IDN?")
print(osc.read())


set.setDisplay(osc, 1, 0.2, 2, 0.03)
set.setDisplay(osc, 2, 20, 1, 1)

osc.write(":RUN")

gen.generatePulses(osc, 5, 6, 0.000000125)


sv.setVoltage(sour, 1000, 27, 0.0150)

#while True:
#    if keyboard.is_pressed("q"):
#        break
#    time.sleep(0.1)
#    sour.write(":FORM:ELEM CURR")
#    sour.read()