import pyvisa as visa




rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])

#FACTORY RESET TARVITTAESSA
instr.write("*RST")

instr.write(":SOUR:FUNC VOLT")
instr.write(":SOUR:VOLT:RANG 1")  # Set voltage range
instr.write(":SOUR:VOLT 0.001")     # Set voltage


# Set the maximum current limit
current_limit = 0.001  # Set the desired current limit in amperes
instr.write(":SENS:CURR:PROT "+str(current_limit))


instr.write(":SENS:FUNC 'CURR'")
instr.write(":SENS:CURR:RANG 0.001")

instr.write(":OUTP ON")

instr.write(":FORM:ELEM VOLT, CURR, RES")



print(instr.read())

#instr.write(":OUTP OFF")