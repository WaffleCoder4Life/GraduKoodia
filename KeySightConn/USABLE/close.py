import pyvisa as visa

rm = visa.ResourceManager()
list = rm.list_resources()
instr = rm.open_resource(list[0])

instr.write("WGEN:OUTPut1 0")
instr.write(":CHANnel1:DISPlay 0")
instr.write(":CHANnel2:DISPlay 0")
instr.write(":STOP")
instr.close()