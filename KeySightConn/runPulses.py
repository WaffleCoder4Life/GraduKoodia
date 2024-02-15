import pyvisa as visa
import setDisplay as sd
import pulseGenerator as pg
import saveData


rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
print(instr.read())

#sd.setDisplay(instr, 1, 1000, 0.3)

pg.generate_pulses(instr, "10000", "5", "10E-6")


#MUISTA OTTAA POIS PÄÄLTÄ!! Testi1 file kohta täynnä.
#saveData.saveData(instr, "testi1.csv", "CustomBySlava, pulse, 10 kHz, 5 V, 10E-6 s, mittaus2")



