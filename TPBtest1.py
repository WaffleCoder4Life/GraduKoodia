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
import statistics
import os.path

#TOM PLS MEASURE FOR BOTH UV AND BLUE!!!!:
#-II CURVE OPEN HOLE FROM LIKE 10 uA LED TO LIKE 1 mA LED OR EVEN HIGHER IF YOU WANT TO AND OF COURSE YOU WANT TO :)
#-II CURVE PLEXIGLAS NO COAT SAME SHIT
#-II CURVE PLEXIGLAS WITH TPB SAME SHIT
#NO NEED TO MAKE COMBINATION PLOT JUST GET THAT DATA 


#work in progress
def generatePathTPB(date, shutter, temp):
    """Generates path to dataCollection for saving measurement data"""
    path = ''
    i = 1
    j = 1
    k = 1
    while True:
        if shutter == 0:
            path = f'./dataCollection/{str(date)}/{str(date)}UVnoSample{str(temp)}{i}.csv'
            if os.path.exists(path):
                i += 1
            else:
                return path
        elif shutter == 1:
            path = f'./dataCollection/{str(date)}/{str(date)}UVplexiglasNoTPB{str(temp)}{j}.csv'
            if os.path.exists(path):
                j += 1
            else:
                return path
        elif shutter == 2:
            path = f'./dataCollection/{str(date)}/{str(date)}UVplexiglasTPB{str(temp)}{k}.csv'
            if os.path.exists(path):
                k += 1
            else:
                return path
        elif shutter == 3:
            path = f'./dataCollection/{str(date)}/{str(date)}BLUEnoSample{str(temp)}{i}.csv'
            if os.path.exists(path):
                i += 1
            else:
                return path
        elif shutter == 4:
            path = f'./dataCollection/{str(date)}/{str(date)}BLUEplexiglasNoTPB{str(temp)}{j}.csv'
            if os.path.exists(path):
                j += 1
            else:
                return path
        elif shutter == 5:
            path = f'./dataCollection/{str(date)}/{str(date)}BLUEplexiglasTPB{str(temp)}{k}.csv'
            if os.path.exists(path):
                k += 1
            else:
                return path


if True:
    print("Test connection")
    rm = visa.ResourceManager()
    list = rm.list_resources()
    print(list)
    sour = rm.open_resource("GPIB0::22::INSTR")

#=====================SETTINGS=======================================================================================================

#THIS SHIT ONLY WORKS IF BOTH MEASUREAVERAGE[0] AND PLOTII ARE 1 :))))))))))))))))))

reset = 0
#measureAverage: [execute, measurement range, SiPM voltage, current limit, average]
measureAverage = [1, 0.021, 22.5, 25e-3, 20]
plotII = 1

#0 hole, 1 plexiglas no tpb, 2 plexiglas with tpb, 3 BLUE0, 4 BLUE1, 5 BLUE2
tempInOhm = '1'
shutter = 3

today = "13062024" #it's today
imageTitle = "1 K blue no sample"

path = generatePathTPB(date=today, shutter=shutter, temp=tempInOhm)

if reset:
    #RUN THESE AFTER START OR GET FUCKED
    sour.write("*RST")  #Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
    sour.write("SYST:ZCH OFF")

if measureAverage[0]:
    sour.write(f":SENS:RANG {measureAverage[1]}")
    currLim = 2.5e-3
    if measureAverage[3] is not None:
        currLim = measureAverage[3]
    setv.setVoltageFine(sour, 50, measureAverage[2], currLim)
    time.sleep(1)
    #path = generatePathTPB(date=today, shutter=shutter)
    with open(path, "a") as file:
        file.write("asd\nasd\nasd\n")
        sour.write(":TRIG:COUNT 1")
        sour.write(":FORM:ELEM READ") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
        sour.write(":FORM:DATA ASCii") #CHOOSE DATA FORM
        while True:
            ledCurr = input("Give LED current (-1 to stop): ")
            if ledCurr == "-1":
                break
            i = 0
            temp = []
            while i < measureAverage[4]:
                sour.write(":INIT") #TRIGGER MEASUREMENT
                sour.write(":SENS:DATA?") #ASK FOR DATA
                data = float(sour.read()) #READ DATA
                temp.append(data)
                time.sleep(0.1)
                i += 1
            file.write(ledCurr + "," + str(statistics.mean(temp)) + "\n")
    sour.write(":SOUR:VOLT:STAT OFF")
    sour.close()


if plotII:
    ledI = [1e3 * point for point in rd.readSourceMeterDataFine(path, 0)]
    simping = [1e6 * point for point in rd.readSourceMeterDataFine(path, 1)]
    plt.scatter(ledI, simping, c="mediumorchid")
    plt.xlabel("$I_{\\mathrm{led}}$ / mA")
    plt.ylabel("$I_{\\mathrm{SiPM}}$ / $\\mu$A")
    plt.title(imageTitle)
    plt.tight_layout()
    plt.savefig(path + ".png")
    plt.show()