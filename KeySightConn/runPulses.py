import pyvisa as visa
import setDisplay as sd
import pulseGenerator as pg



rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
print(instr.read())

sd.setDisplay(instr, 1, 1, 0.3)


pg.generate_pulses(instr, "100", "0.5", "20E-9")



