import pyvisa as visa
import generatePulses as gen
import saveData as save
import setDisplay as set


print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
print(instr.read())

