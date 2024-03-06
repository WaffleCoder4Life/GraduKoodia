import pyvisa as visa
from Keithley import setVoltage as sv
import KeySightConn.setDisplay as sd


rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
osc.write("*IDN?")
print(osc.read())

sour = rm.open_resource(list[2])
sour.write("*IDN?")
print(sour.read())

sd.setDisplay(osc, 1, 0.05, 0.00000005, 0.005)

sv.setVoltage(sour, 1000, 25, 0.015)

