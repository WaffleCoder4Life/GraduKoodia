import pyvisa as visa
import Keithley6487.voltageSweepFine as vsf
import Keithley6487.setVoltageFine as setv
import Keithley6487.voltageSweepAverage as vsa
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

sour = rm.open_resource("GPIB0::22::INSTR")

#sour.write("*IDN?")
#print(sour.read())



reset = 0
singleTest = 1
sweepTest = 0
sweepAverageTest = 0
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
    


filename = "darkCurrentAverage10PointsShutterOpened"
dateFolder = "19032024" #CHANGE AND CReATE NEW FOLDER TO dataCollection

if sweepTest:
    print("Executing sweep test...")
    vsf.voltageSweepFine(sour, 50, 25, 26.6, 2.5E-6, filename, "Keithley6487, temperature 1.132 kOhm, IV-curve for dark current with open shutter and LED power off, voltage step 0.01")
    sour.close()

if sweepAverageTest:
    print("Executing average sweep test...")
    vsa.voltageSweepAverage(sour, 50, 26, 26.6, 2.5E-6, filename, 10, 0.005, "Keithley 6487, temperature 1.132 kOhm, IV-curve with average sweep, 10 points per voltage, dark current with open lid, voltage step 0.005")


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


