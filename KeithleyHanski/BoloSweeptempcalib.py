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
import nidaqmx as nid

import pyvisa as visa
import time
from datetime import date


def WriteJson(filepath, dict):
    # Writes metadata to a json file
    with open(filepath, "w") as json_file:  
        json.dump(dict, json_file, indent = 4, sort_keys = True)
        
def measureTemp():
    # Read and return channel 3 and 4 from DAQ card, 3 for MC, 4 for SC
    with nid.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
        ai3 = task.read()
    with nid.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai4")
        ai4 = task.read()
    return ai3, ai4

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


def four_probe_measurement_U(settings,keithley, A = False, B = False):
    """
    Reads voltage corresponding to current[0] and current[1]
    from channels A and B, respectively.
    """
    
    if A:
        #MEASUREMENT A:
        keithley.write(f'smua.source.leveli = 500E-9')
        keithley.write('smua.source.output = smua.OUTPUT_ON')
    if B:
        # MEASUREMENT B:
        keithley.write(f'smub.source.leveli = 500E-9')
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
    
    T_MC, T_SC = measureTemp()
    
    

    return Ua, Ub, T_MC, T_SC

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
                "Imeas": [4E-6, 8E-6, 1E-6, 1E-5],                  # [Imin_A, Imax_A, Imin_B, Imax_B]
                "NumberOfPoints": 1500,                           # Number of points per sweep. 
                "measureNeg": False,                             # If true, also measures {NumberOfPoints} negative points
                "SweepA": True,                                 # Whether a sweep is done on bolo A
                "SweepB": True,                                 # Whether a sweep is done on bolo B
                "measurePassive": True,                         # Whether the data for the other bolometer is also recorded while sweeping the other
                "Ipassive": 10E-9,                                # Excitation for passive bolometer if measured    
                "measTime": 3,                                   # Delay between setting meas current and recording measurement, to allow integration in device
                "speed": 10,                                      # Set the measurement time constant, recommended around 1/3 of measTime
                "pointDelay": 300,                                 # Extra delay between sweep points
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
    measurementlength = (settings["SweepA"]+settings["SweepB"])*(1+settings["measHyst"])*settings["NumberOfPoints"]*(settings["measTime"]+settings["pointDelay"])/60
    print(f"Rough time until completion: {measurementlength:.2f} min")
    
    # List of keys to delete from metadata, compatibility reasons
    nonSerializable = ["instr"]
    metadata = settings.copy()
    for key in nonSerializable:
        metadata.pop(key, None)
    WriteJson(measfolder+"\\"+measname+"_meta.json", metadata)
    
    FileName = settings["measfolder"]+"\\"+settings["measname"]+"TempCalib.dat"
    with open(FileName, "w") as write:
        write.write("Ia, A\tIb, A\tUa,V\tUb,V\tT_MC,Ohm\t T_SC, Ohm\n")
    
    # Run the sweep
    while True:
        Ua, Ub, T_MC, T_SC = four_probe_measurement_U(settings,keithley, A = True, B = True)
        with open(FileName, "a") as write:
            write.write(f"20E-9\t20E-9\t{Ua}\t{Ub}\t{T_MC}\t{T_SC}\n")
        time.sleep(settings["pointDelay"])
    print("Measurement finished")


# Run if called from CMD
if __name__=='__main__':
    reswithIV()
    print(os.getcwd())
