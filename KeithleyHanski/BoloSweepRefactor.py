# -*- coding: utf-8 -*-
"""
17/12/2021

@author: Otto H
This script is for measuring IV curves of bolometers on the old setup using Keithley2614 current source

"""

import numpy as np
import os
import sys
import json

import pyvisa as visa
import time
from datetime import date


def WriteJson(filepath, dict):
    # Writes metadata to a json file
    with open(filepath, "w") as json_file:  
        json.dump(dict, json_file, indent = 4, sort_keys = True)

def init_keithley(settings):
    keithley = settings["instr"]
    averaging = settings["averaging"]
    
    #Initialize Keithley for applying a current:
    
    keithley.write('smua.reset()')
    keithley.write('smua.source.offmode = smua.OUTPUT_NORMAL')
    keithley.write('smua.source.func = smua.OUTPUT_DCAMPS')
    keithley.write('smua.source.autorangei = smua.AUTORANGE_ON')
    keithley.write('smua.measure.autorangev = smua.AUTORANGE_ON')
    keithley.write(f"smua.measure.count = {averaging}")
    keithley.write('smua.source.limitv = 50')

    keithley.write('smub.reset()')
    keithley.write('smub.source.offmode = smub.OUTPUT_NORMAL')
    keithley.write('smub.source.func = smub.OUTPUT_DCAMPS')
    keithley.write('smub.source.autorangei = smub.AUTORANGE_ON')
    keithley.write('smub.measure.autorangev = smub.AUTORANGE_ON')
    keithley.write(f"smub.measure.count = {averaging}")
    keithley.write('smub.source.limitv = 12')
    
    # Set the measurement speed
    # 0.01, 0.1, 1, 10 for FAST, MED, NORMAL and HI-ACCURACY, respectively. 
    # Full range [0.001,25]
    speed = settings["speed"]
    keithley.write(f"smua.measure.nplc = {speed}")
    keithley.write(f"smub.measure.nplc = {speed}")

def SweepCurrent(settings):
    """
    Sweep current first in chan A, then chan B, from -Imax to Imax
    Imax_A: measurement[0]
    Imax_B: measurement[1]
    """
    # Imeas = [Imin_A, Imax_A, Imin_B, Imax_B]
    Imeas = settings["Imeas"]
    NumberOfPoints = settings["NumberOfPoints"]
    measpass = settings["measurePassive"]
    Ipass = settings["Ipassive"]
    keithley = settings["instr"]
    
    # Define the current sweep ranges and data arrays
    if settings["logmode"]:
        IcA = unEvenArray(NumberOfPoints,Imeas[0],Imeas[1],settings["measureNeg"])
        IcB = unEvenArray(NumberOfPoints,Imeas[2],Imeas[3],settings["measureNeg"])
        print("Logarithmic measurement")
    else:
        IcA = EvenArray(NumberOfPoints,Imeas[0],Imeas[1],settings["measureNeg"])
        IcB = EvenArray(NumberOfPoints,Imeas[2],Imeas[3],settings["measureNeg"])
        print("Linear measurement")
    data_Ua = np.zeros((len(IcA)), float)
    data_Ub = np.zeros((len(IcB)), float)
    
    # Sweep A if needed
    if settings["SweepA"]:
        FileName = settings["measfolder"]+"\\"+settings["measname"]+"SweepA.dat"
        with open(FileName, "w") as write:
            write.write("Ia, Ib, A\tUa,V\tUb,V, Ua_avg,V,\t Ub_avg,V\n")
    
        # Sweep current in channel A, constant current in B
        for i, current in enumerate(IcA):
            data_Ua[i], data_Ub[i] = four_probe_measurement_U(settings,keithley, [current, Ipass], A=True, B=measpass)
            if i%2 != 0:
                with open(FileName, "a") as write:
                    write.write(f"{IcA[i-1]}\t{measpass*Ipass}\t{data_Ua[i-1]}\t{data_Ub[i-1]}\t{(data_Ua[i]+data_Ua[i-1])/2}\t{(data_Ub[i]+data_Ub[i-1])/2}\n")
                    write.write(f"{IcA[i]}\t{measpass*Ipass}\t{data_Ua[i]}\t{data_Ub[i]}\t{(data_Ua[i]+data_Ua[i-1])/2}\t{(data_Ub[i]+data_Ub[i-1])/2}\n")
            ct = time.strftime("%H:%M",time.localtime())
            print(ct+f":: Sweep A point {i+1} out of {len(IcA)} done")
        
        # If also measuring sweep back, create second meas file for it
        if settings["measHyst"]:
            FileName = settings["measfolder"]+"\\"+settings["measname"]+"hystSweepA.dat"
            with open(FileName, "w") as write:
                write.write("Ia, Ib, A\tUa,V\tUb,V, Ua_avg,V,\t Ub_avg,V\n")
        
            # Sweep back for hysteresis
            IcA = np.flip(IcA)
            for i, current in enumerate(IcA):
                data_Ua[i], data_Ub[i] = four_probe_measurement_U(settings,keithley, [current, Ipass], A=True, B=measpass)
                if i%2 != 0:
                    with open(FileName, "a") as write:
                        write.write(f"{IcA[i-1]}\t{measpass*Ipass}\t{data_Ua[i-1]}\t{data_Ub[i-1]}\t{(data_Ua[i]+data_Ua[i-1])/2}\t{(data_Ub[i]+data_Ub[i-1])/2}\n")
                        write.write(f"{IcA[i]}\t{measpass*Ipass}\t{data_Ua[i]}\t{data_Ub[i]}\t{(data_Ua[i]+data_Ua[i-1])/2}\t{(data_Ub[i]+data_Ub[i-1])/2}\n")
                ct = time.strftime("%H:%M",time.localtime())
                print(ct+f":: Hyst sweep A point {i+1} out of {len(IcA)} done")
        
        keithley.write('smua.source.output = smua.OUTPUT_OFF')
        keithley.write('smub.source.output = smub.OUTPUT_OFF')
        # Let system relax
        time.sleep(settings["sweepDelay"])
        
        
        
    # Sweep B if needed
    if settings["SweepB"]:
        FileName = settings["measfolder"]+"\\"+settings["measname"]+"SweepB.dat"
        with open(FileName, "w") as write:
            write.write("Ia, Ib, A\tUa,V\tUb,V, Ua_avg,V,\t Ub_avg,V\n")
        
        # Sweep current in channel B, constant current in A
        for i, current in enumerate(IcB):
            data_Ua[i], data_Ub[i] = four_probe_measurement_U(settings,keithley, [Ipass,current], A=measpass, B=True)
            if i%2 != 0:
                with open(FileName, "a") as write:
                    write.write(f"{measpass*Ipass}\t{IcB[i-1]}\t{data_Ua[i-1]}\t{data_Ub[i-1]}\t{(data_Ua[i]+data_Ua[i-1])/2}\t{(data_Ub[i]+data_Ub[i-1])/2}\n")
                    write.write(f"{measpass*Ipass}\t{IcB[i]}\t{data_Ua[i]}\t{data_Ub[i]}\t{(data_Ua[i]+data_Ua[i-1])/2}\t{(data_Ub[i]+data_Ub[i-1])/2}\n")
            ct = time.strftime("%H:%M",time.localtime())
            print(ct+f":: Sweep B point {i+1} out of {len(IcB)} done")
        
        if settings["measHyst"]:
            FileName = settings["measfolder"]+"\\"+settings["measname"]+"hystSweepB.dat"
            with open(FileName, "w") as write:
                write.write("Ia, Ib, A\tUa,V\tUb,V, Ua_avg,V,\t Ub_avg,V\n")
            
            # Sweep back for hysteresis
            IcB = np.flip(IcB)
            for i, current in enumerate(IcB):
                data_Ua[i], data_Ub[i] = four_probe_measurement_U(settings,keithley, [Ipass,current], A=measpass, B=True)
                if i%2 != 0:
                    with open(FileName, "a") as write:
                        write.write(f"{measpass*Ipass}\t{IcB[i-1]}\t{data_Ua[i-1]}\t{data_Ub[i-1]}\t{(data_Ua[i]+data_Ua[i-1])/2}\t{(data_Ub[i]+data_Ub[i-1])/2}\n")
                        write.write(f"{measpass*Ipass}\t{IcB[i]}\t{data_Ua[i]}\t{data_Ub[i]}\t{(data_Ua[i]+data_Ua[i-1])/2}\t{(data_Ub[i]+data_Ub[i-1])/2}\n")
                ct = time.strftime("%H:%M",time.localtime())
                print(ct+f":: Hyst sweep B point {i+1} out of {len(IcB)} done")
        
        keithley.write('smua.source.output = smua.OUTPUT_OFF')
        keithley.write('smub.source.output = smub.OUTPUT_OFF')
        time.sleep(settings["sweepDelay"])

def four_probe_measurement_U(settings,keithley,current, A = False, B = False):
    """
    Reads voltage corresponding to current[0] and current[1]
    from channels A and B, respectively.
    """
    
    if A:
        #MEASUREMENT A:
        keithley.write(f'smua.source.leveli = {current[0]}')
        keithley.write('smua.source.output = smua.OUTPUT_ON')
    if B:
        # MEASUREMENT B:
        keithley.write(f'smub.source.leveli = {current[1]}')
        keithley.write('smub.source.output = smub.OUTPUT_ON')
    
    if A:
        time.sleep(settings["measTime"])
        
        # Read int(averaging) voltage points, channel A
        keithley.write("smua.measure.v(smua.nvbuffer1)")
        volt = keithley.query("printbuffer(1,smua.nvbuffer1.n,smua.nvbuffer1.readings)")
        keithley.write("smua.nvbuffer1.clear()")
        # Average the measured points
        if settings["averaging"] > 1:
            volt = volt.split(", ")
            volt = [float(v) for v in volt]
            Ua = sum(volt)/len(volt)
        else:
            Ua = float(volt)
    else:
        Ua = 0
    
    if B:
        if not A:
            time.sleep(settings["measTime"])
        # Read int(averaging) voltage points, channel B
        keithley.write("smub.measure.v(smub.nvbuffer1)")
        volt = keithley.query("printbuffer(1,smub.nvbuffer1.n,smub.nvbuffer1.readings)")
        keithley.write("smub.nvbuffer1.clear()")
        # Average the measured points
        if settings["averaging"] > 1:
            volt = volt.split(", ")
            volt = [float(v) for v in volt]
            Ub = sum(volt)/len(volt)
        else:
            Ub = float(volt)
    else:
        Ub = 0
    
    if settings["pointDelay"] > 0:
        keithley.write('smua.source.output = smua.OUTPUT_OFF')
        keithley.write('smub.source.output = smub.OUTPUT_OFF')
        time.sleep(settings["pointDelay"])

    return Ua, Ub

def checkLimit(Imeas):
    """Check whether measurement currents might overheat the system"""
    Ilimit = 100E-6
    for current in Imeas:
        if current[0] > Ilimit or current[1] > Ilimit:
            sys.exit("Measurement current setting too high, exiting")
    
def unEvenArray(NumberOfPoints,Imin,Imax,measureNeg):
    # Create logarithmically spaced array of measurement currents
    Ipos = np.geomspace(Imin,Imax,NumberOfPoints)
    if measureNeg:
        IcArray = np.zeros(2*len(Ipos)+2)
        for i in range(len(Ipos)):
            IcArray[2*i+2] = Ipos[i]
            IcArray[2*i+3] = -Ipos[i]
    else:
        IcArray = Ipos
    
    return IcArray

def EvenArray(NumberOfPoints,Imin,Imax,measureNeg):
    # Create linearly spaced array of measurement currents
    Ipos = np.linspace(Imin,Imax,NumberOfPoints)
    if measureNeg:
        IcArray = np.zeros(2*len(Ipos)+2)
        for i in range(len(Ipos)):
            IcArray[2*i+2] = Ipos[i]
            IcArray[2*i+3] = -Ipos[i]
    else:
        IcArray = Ipos
        
    return IcArray

def reswithIV(test=False):
    
    # Set up GPIB connection to Keithley current source 
    rm = visa.ResourceManager()
    print(rm.list_resources())
    keithley = rm.open_resource('GPIB::26')
    
    folddate = date.today()
    scriptfolder = os.getcwd()
    measfolder = "D:\\dilution_experiments\\"+date.strftime(folddate,"%Y")+"\\"+date.strftime(folddate,"%Y-%m")+"\\"+date.strftime(folddate,"%Y-%m-%d")
    try:
        os.mkdir(measfolder)
    except:
        pass
    measname = input("Measurement name:\n")
    tempSC = input("Sample cell thermo R[kOhm]:")
    tempMC = input("MC thermo R[kOhm]:")
    
    
    #=================Settings=======================================
    # Settings are in dict format, easy to save as metadata.
    settings = {
                "Imeas": [3.5E-6,8.5E-6,4E-6,1E-5],                  # [Imin_A, Imax_A, Imin_B, Imax_B]
                "NumberOfPoints": 1500,                           # Number of points per sweep. 
                "measureNeg": False,                             # If true, also measures {NumberOfPoints} negative points
                "SweepA": True,                                 # Whether a sweep is done on bolo A
                "SweepB": True,                                 # Whether a sweep is done on bolo B
                "measurePassive": True,                         # Whether the data for the other bolometer is also recorded while sweeping the other
                "Ipassive": 10E-9,                                # Excitation for passive bolometer if measured
                "measTime": 5,                                   # Delay between setting meas current and recording measurement, to allow integration in device
                "speed": 1.5,                                      # Set the measurement time constant, recommended around 1/3 of measTime
                "pointDelay": 0,                                 # Extra delay between sweep points
                "sweepDelay": 1,                                 # Delay between sweeps, in seconds
                "averaging": 1,                                  # Recommend keeping at 1 on higher precision settings to avoid long measurements. Better to adjust time constant
                "logmode": False,                                # Whether measurement currents are scaled logarithmically or linearly
                "measHyst": True,                                # Whether measurement will run back in opposite direction
                "measname": measname,                            # Name given to measurement at start
                "measfolder": measfolder,                       # Measurement folder
                "T_SC": tempSC,                                  # Sample cell temp
                "T_MC": tempMC,                                  # Mixing chamber temp
                "instr": keithley,                               # VISA resource for keithley
                "date": date.strftime(folddate,"%Y-%m-%d"),      # Measurement date
                "time": time.strftime("%H:%M",time.localtime()) # Measurement time
                }
    #================================================================
    
    init_keithley(settings)
    Ua, Ub = four_probe_measurement_U(settings,keithley,[0,0], A=True,B=True)
    print("Test measurement: ok")
    measurementlength = (settings["SweepA"]+settings["SweepB"])*(1+settings["measHyst"])*settings["NumberOfPoints"]*(settings["measTime"]+settings["pointDelay"])/60
    print(f"Rough time until completion: {measurementlength:.2f} min")
    
    # List of keys to delete from metadata, compatibility reasons
    nonSerializable = ["instr"]
    metadata = settings.copy()
    for key in nonSerializable:
        metadata.pop(key, None)
    WriteJson(measfolder+"\\"+measname+"_meta.json", metadata)
    
    # Run the sweep
    SweepCurrent(settings)
    print("Measurement finished")


# Run if called from CMD
if __name__=='__main__':
    reswithIV()
    print(os.getcwd())
