import pyvisa as visa
import voltageSweep as vs
import stepSweep as ss
import stepSweep2 as ss2
import stepSweepManual as manual



rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
#print(instr.read())





#FACTORY RESET TARVITTAESSA
instr.write("*RST")


# Configure Sourcemeter settings (example: set voltage source mode)
instr.write(":SOUR:FUNC VOLT")
instr.write(":SOUR:VOLT:RANG 1")  # Set voltage range
instr.write(":SOUR:VOLT 0.1")     # Set voltage


# Set the maximum current limit
current_limit = 0.001  # Set the desired current limit in amperes
instr.write(":SENS:CURR:PROT "+str(current_limit))

""" print(float(instr.query(":SOUR:VOLT?"))) """


#ss.step_sweep(instr, 0.1, 1.5, 0.1)


manual.manualSweep(instr, 0.001, 0.01, 10, 0.005, "testi1a")




#Keskeyttää kaiken
""" instr.write(":ABORt") """


#Tällä koodilla vaihdetaan lähteeksi virta ja asetetaan se
""" instr.write(":SOUR:FUNC CURR")
# Query current amplitude
current_amplitude = float(instr.query(":SOUR:CURR?"))

print("Current Amplitude:", current_amplitude, "A")

instr.write(":SOUR:CURR:RANG 0.001")#Set current range

# Set current amplitude limit to 1 mA
current_limit = 0.001  # 1 mA
instr.write(":SOUR:CURR:LEV "+str(current_limit))

# Query current amplitude limit to verify
query_result = instr.query(":SOUR:CURR:LEV?")
current_limit_set = float(query_result)

print("Current Limit Set:", current_limit_set, "A") """



#Lukee edellisen error viestin
instr.write(":SYST:ERR?")
print(instr.read())