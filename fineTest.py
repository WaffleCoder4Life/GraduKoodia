import pyvisa as visa
import Keithley6487.voltageSweepFine as vsf
import time
import keyboard

""" instrumentlist = {
    "picoammeter": {
        "IDN": "KEITHLEY INSTRUMENTS INC.,MODEL 6487",
        "address": "",
        "commands": {
            "get_voltage": "SOUR1:VOLT?"
        }
    }
} """

print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

#for id in rm.list_resources():
#    try:
#        instr = rm.open_resource(id)
#        IDN = instr.query("*IDN?")
#        if IDN in instrumentlist["picoammeter"]:
#            instrumentlist["picoammeter"]["address"] = id
#        instr.close()
#    except:
#        pass

sour = rm.open_resource(list[1])

#sour.write("*IDN?")
#print(sour.read())

#RUN THESE AFTER START OR GET FUCKED
sour.write("*RST")  #Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
sour.write("SYST:ZCH OFF")


sour.write(":SOUR:VOLT:RANG 10")  # Set voltage range, 10 V, 50 V, 100 V
sour.write(":SOUR:VOLT:ILIM 25e-3") #SET CURRENT LIMIT
#sour.write(":SOUR:VOLT:ILIM?")
#print(sour.read())

sour.write(":SOUR:VOLT 1") #SET VOLTAGE
#sour.write(":SOUR:VOLT:RANG?")
#print(sour.read())

sour.write(":SOUR:VOLT:STAT ON") #OUTPUT ON 
sour.write(":FORM:ELEM ALL") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
sour.write(":FORM:DATA ASCii")
#sour.write(":SENS:FUNC CURR")
sour.write(":INIT")
sour.write(":SENS:DATA?")
data = sour.read()
print(data)


#time.sleep(1)

sour.write(":SOUR:VOLT:STAT OFF") #OUTPUT OFF
#sour.write(":SENS:CURR:PROT " + str(currentLimit_A)) # Set the maximum current limit
#sour.write(":SENS:CURR:RANG 1E-5") #set current measurement range


sour.close()