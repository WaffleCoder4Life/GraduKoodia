import voltageSweep as vs
import pyvisa as visa

rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")


vs.voltageSweep(instr, 20, 29, 20, 0.015, "sweepdata1")