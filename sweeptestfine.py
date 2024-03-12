import pyvisa as visa
import Keithley6487.voltageSweepFine as vsf
import time
import keyboard


print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

sour = rm.open_resource(list[1])

#RUN THESE AFTER START OR GET FUCKED
sour.write("*RST")  #Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
sour.write("SYST:ZCH OFF")

sour.write(":SOUR:VOLT:RANG 10")  # Set voltage range, 10 V, 50 V, 100 V
sour.write(":SOUR:VOLT:ILIM 25e-3") #SET CURRENT LIMIT

fileName = "sweeptestfine"
sour.write(":FORM:DATA ASCii")
sour.write(":SOUR:VOLT 1")
sour.write(":SOUR:VOLT:STAT ON") #OUTPUT ON 
with open("./dataCollection/" + fileName + ".csv", "a") as file:
            file.write("THIS IS FINE\n")
            voltage = 1
            endVoltage = 2
            voltage_step = 0.1
            while voltage <= endVoltage:
                sour.write(":SOUR:VOLT " + str(voltage))  # Set voltage
                time.sleep(0.2)
                sour.write(":FORM:ELEM ALL")
                sour.write(":INIT")
                sour.write(":SENS:DATA?")
                file.write(sour.read())

                voltage += voltage_step


#sour.write(":SOUR:VOLT:ILIM?")
#print(sour.read())

#sour.write(":SOUR:VOLT:RANG?")
#print(sour.read())


#sour.write(":SENS:FUNC CURR")

sour.write(":SOUR:VOLT:STAT OFF") #OUTPUT OFF
#sour.write(":SENS:CURR:PROT " + str(currentLimit_A)) # Set the maximum current limit
#sour.write(":SENS:CURR:RANG 1E-5") #set current measurement range


sour.close()