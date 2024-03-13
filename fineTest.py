import pyvisa as visa
import Keithley6487.voltageSweepFine as vsf
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

sour = rm.open_resource(list[1])

#sour.write("*IDN?")
#print(sour.read())



reset = 1
singleTest = 0
sweepTest = 1
plotSweep = 1

if reset:
    #RUN THESE AFTER START OR GET FUCKED
    sour.write("*RST")  #Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
    sour.write("SYST:ZCH OFF")


if singleTest:
    print("Executing single test...")
    sour.write(":SOUR:VOLT:RANG 50")  # Set voltage range, 10 V, 50 V, 100 V
    #sour.write(":SOUR:VOLT:RANG?")
    #print(sour.read())
    sour.write(":SOUR:VOLT:ILIM 2.5e-3") #SET CURRENT LIMIT
    #sour.write(":SOUR:VOLT:ILIM?")
    #print(sour.read())
    sour.write(":SENS:RANG 0.00001") #SET CURRENT MEASURE RANGE
    sour.write(":SOUR:VOLT 8") #SET VOLTAGE
    sour.write(":SOUR:VOLT:STAT ON") #OUTPUT ON 
    sour.write(":FORM:ELEM READ, VSO") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
    sour.write(":FORM:DATA ASCii") #CHOOSE DATA FORM
    sour.write(":INIT") #TRIGGER MEASUREMENT
    time.sleep(1)
    sour.write(":SENS:DATA?") #ASK FOR DATA
    data = sour.read() #READ DATA
    print(data)
    sour.write(":SOUR:VOLT:STAT OFF") #OUTPUT OFF
    sour.close()


filename = "13032024_FINE_sweep_up_10mALED"
if sweepTest:
    print("Executing sweep test...")
    vsf.voltageSweepFine(sour, 50, 19, 23, 0.000025, filename, "Keithley6487, temperature 16620 kOhm, IV-curves with 0.01 mV voltage steps.")
    sour.close()


if plotSweep:
    for volt in rd.readSourceMeterDataFine("./dataCollection/" + filename, 1):
        print("original "+str(volt))
    voltageup = rd.readSourceMeterDataFine("./dataCollection/" + filename, 0) #VOLTAGE VAlUES ARE NOW JUST VALUES SEND TO SOURCE
    currentup = [10**(6)*point for point in rd.readSourceMeterDataFine("./dataCollection/" + filename, 1)]
    for volt in voltageup:
        print(volt)
    plt.scatter(voltageup, currentup, s=2, c="red", marker="d")
    plt.xlabel("$U$ / V")
    plt.ylabel("$I$ / $\\mu$A")
    plt.tight_layout()
    plt.savefig("./dataCollection/Photos/" + filename)
    plt.show()


