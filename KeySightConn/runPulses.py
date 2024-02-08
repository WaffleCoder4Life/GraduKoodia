import pyvisa as visa
import setDisplay as sd
import string
import struct
import sys
import plotData
import countPeaks
import setDisplay
import pulseGenerator as pg



rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
print(instr.read())



pg.generate_pulses(instr, "800E3", "5E-3", "120E-9")

