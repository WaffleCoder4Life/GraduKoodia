import pyvisa as visa
import Keithley6487.voltageSweepFine as vsf
import Keithley6487.setVoltageFine as setv
import Keithley6487.voltageSweepAverage as vsa
import time
import keyboard
import matplotlib.pyplot as plt
import dataAnalz.readSourceMeterDataFine as rd
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
import scipy.optimize

""" instrumentlist = {
    "picoammeter": {
        "IDN": "KEITHLEY INSTRUMENTS INC.,MODEL 6487",
        "address": "",
        "commands": {
            "get_voltage": "SOUR1:VOLT?"
        }
    }
} """

# connect
if False:
    print("Test connection")
    rm = visa.ResourceManager()
    list = rm.list_resources()
    print(list)
    sour = rm.open_resource("GPIB0::22::INSTR")
#for id in rm.list_resources():
#    try:
#        instr = rm.open_resource(id)
#        IDN = instr.query("*IDN?")
#        if IDN in instrumentlist["picoammeter"]:
#            instrumentlist["picoammeter"]["address"] = id
#        instr.close()
#    except:
#        pass



#sour.write("*IDN?")
#print(sour.read())



reset = 0 # Reset source meter before starting measurements
singleTest = 0
sweepTest = 0
sweepAverageTest = 0 # Change sweep parameters from belowe
plotSweep = 0 # Plot IV curves from sweep
plotSweepSqrt = 1 # Plot sqrt(I)V curves from sweep
closeAfter = 0 # Close source meter and connection


filename = "100uA_sweepPt380Ohm"
#filename2 = "secoundBreakdown_openShutter_1169Ohm"
dateFolder = "26042024" #CHANGE 
ledInt = "100 uA"
temperature = "Pt 1100 Ohm"
startVoltage = 23.5
endVoltage = 27
voltageStep = 0.1
pointsPerVoltage = 5


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
    setv.setVoltageFine(sour, 50, 23, 2.5e-3)
    sour.write(":FORM:ELEM READ, VSO") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
    sour.write(":FORM:DATA ASCii") #CHOOSE DATA FORM
    sour.write(":INIT") #TRIGGER MEASUREMENT
    time.sleep(1)
    sour.write(":SENS:DATA?") #ASK FOR DATA
    data = sour.read() #READ DATA
    print(data)
    



if sweepTest:
    print("Executing sweep test...")
    vsf.voltageSweepFine(sour, 50, 25, 27, 2.5E-3, filename, "Keithley6487, temperature 1001 Ohm second resistor, IV-curve for LED 6V flat line, voltage step 0.1")
    sour.close()

if sweepAverageTest:
    print("Executing average sweep test...")
    vsa.voltageSweepAverage(sour, 50, startVoltage, endVoltage, 2.5E-3, filename, pointsPerVoltage, voltageStep, f"Keithley 6487, temperature {temperature} kOhm, IV-curve with average sweep from {startVoltage} V to {endVoltage} V, {pointsPerVoltage} points per voltage, LED {ledInt}, voltage step {voltageStep} V")


if closeAfter:
    sour.write(":SOUR:VOLT:STAT OFF") #OUTPUT OFF
    sour.close()

if plotSweep:
    voltageup = rd.readSourceMeterDataFine("./dataCollection/"+ dateFolder +"/" + filename, 0) #VOLTAGE VAlUES ARE NOW JUST VALUES SEND TO THE SOURCE
    currentup = [10**(6)*point for point in rd.readSourceMeterDataFine("./dataCollection/" + dateFolder +"/" + filename, 1)]
    #voltageup2 = rd.readSourceMeterDataFine("./dataCollection/"+ dateFolder +"/" + filename2, 0) #VOLTAGE VAlUES ARE NOW JUST VALUES SEND TO THE SOURCE
    #currentup2 = [10**(6)*point for point in rd.readSourceMeterDataFine("./dataCollection/" + dateFolder +"/" + filename2, 1)]
    plt.scatter(voltageup, currentup, s=2, c="red", marker="d", label = f"LED {ledInt}")
    #plt.scatter(voltageup2, currentup2, s=2, c="green", marker="d", label = "Shutter open")
    print(len(voltageup))
    plt.xlabel("$U$ / V")
    plt.ylabel("$I$ / uA")
    plt.legend()
    plt.tight_layout()
    plt.savefig("./dataCollection/"+dateFolder+"/Photos/" + filename)
    plt.show()

def line(x, a, b):
    return a*x + b

if plotSweepSqrt:
    voltage = rd.readSourceMeterDataFine("./dataCollection/"+ dateFolder +"/" + filename, 0)
    dataset = rd.readSourceMeterDataFine("./dataCollection/" + dateFolder +"/" + filename, 1)
    fixedDataset = []
    for data in dataset:
        if data < 0:
            fixedDataset.append(0)
        else:
            fixedDataset.append(data)
    currentSqrt = [np.sqrt(10**(6)*point) for point in fixedDataset]
    plt.scatter(voltage, currentSqrt, s=2, c="red", marker="d", label = str(ledInt)+" LED")
    print(len(voltage))
    voltResult = scipy.optimize.curve_fit(line, xdata = voltage[50:75], ydata = currentSqrt[50:75]) # Gives parameters for a line fit, check ctarting point from image
    print(voltResult) 
    x = Symbol("x")
    lineFit = line(x, voltResult[0][0], voltResult[0][1]) # arguments x, a (slope) and b (intercept)
    breakdownResult = solve(lineFit, x) # solves x from lineFit y = 0
    
    linSpace = np.linspace(20, 24, 1000) # Change linspace to match used voltage range in sweep
    linePlot = line(linSpace, voltResult[0][0], voltResult[0][1])
    plt.plot(linSpace, linePlot, color = "black", label = f"Linear fit, V_bd {breakdownResult[0]:.3f}")

    plt.xlabel("$U$ / V")
    plt.ylabel("$\sqrt{I}$ / $\sqrt{uA}$")
    plt.legend()
    plt.tight_layout()
    plt.savefig("./dataCollection/"+dateFolder+"/Photos/" + filename+"Sqrt")
    plt.show()