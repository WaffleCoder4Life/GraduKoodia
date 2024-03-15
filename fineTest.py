import pyvisa as visa
import Keithley6487.voltageSweepFine as vsf
import Keithley6487.setVoltageFine as setv
import time
import keyboard
import matplotlib.pyplot as plt
import dataAnalz.readSourceMeterDataFine as rd


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

sour = rm.open_resource(list[2])

#sour.write("*IDN?")
#print(sour.read())



reset = 1
singleTest = 1
sweepTest = 0
plotSweep = 0
closeAfter = 0

if reset:
    #RUN THESE AFTER START OR GET FUCKED
    sour.write("*RST")  #Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
    sour.write("SYST:ZCH OFF")


if singleTest:
    print("Executing single test...")
    #sour.write(":SOUR:VOLT:RANG 50")  # Set voltage range, 10 V, 50 V, 100 V
    #sour.write(":SOUR:VOLT:RANG?")
    #print(sour.read())
    #sour.write(":SOUR:VOLT:ILIM 2.5e-3") #SET CURRENT LIMIT
    #sour.write(":SOUR:VOLT:ILIM?")
    #print(sour.read())
    sour.write(":SENS:RANG 0.00001") #SET CURRENT MEASURE RANGE
    #sour.write(":SOUR:VOLT 24") #SET VOLTAGE
    #sour.write(":SOUR:VOLT:STAT ON") #OUTPUT ON 
    setv.setVoltageFine(sour, 50, 24, 2.5e-3)
    sour.write(":FORM:ELEM READ, VSO") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
    sour.write(":FORM:DATA ASCii") #CHOOSE DATA FORM
    sour.write(":INIT") #TRIGGER MEASUREMENT
    time.sleep(1)
    sour.write(":SENS:DATA?") #ASK FOR DATA
    data = sour.read() #READ DATA
    print(data)
    


filename = "10mAsweep"
dateFolder = "15032024"

if sweepTest:
    print("Executing sweep test...")
    vsf.voltageSweepFine(sour, 50, 19, 23, 2.5E-6, filename, "Keithley6487, temperature 1.735 kOhm, IV-curve for 10 mA, voltage step 0.05")
    sour.close()


if closeAfter:
    sour.write(":SOUR:VOLT:STAT OFF") #OUTPUT OFF
    sour.close()

if plotSweep:
    voltageup = rd.readSourceMeterDataFine("./dataCollection/"+ dateFolder +"/" + filename, 0) #VOLTAGE VAlUES ARE NOW JUST VALUES SEND TO THE SOURCE
    currentup = [10**(9)*point for point in rd.readSourceMeterDataFine("./dataCollection/" + dateFolder +"/" + filename, 1)]
    plt.scatter(voltageup, currentup, s=2, c="red", marker="d")
    plt.xlabel("$U$ / V")
    plt.ylabel("$I$ / nA")
    plt.tight_layout()
    plt.savefig("./dataCollection/"+dateFolder+"/Photos/" + filename)
    plt.show()


