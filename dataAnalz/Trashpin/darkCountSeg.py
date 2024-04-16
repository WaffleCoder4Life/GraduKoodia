import pyvisa as visa
from deviceControl import setDisplay, setVoltageFine, saveData
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import struct
import time

settings = {



        # Oscilloscope display settings
        "timeRange" : 20E-6,
        "voltageRange" : 800E-3,

        # Main control
        "runTest" : 1,
        "readData" : 0,

        # Resource control
        "closeResources" : 1,
}


if settings["runTest"]:
    #VISA CONNECTIONS
    rm = visa.ResourceManager()
    osc = rm.open_resource('USB0::0x2A8D::0x1797::CN56396144::INSTR') # Connect oscilloscope
    
    """ sour = rm.open_resource("GPIB0::22::INSTR") # Connect source
    sour.write("*RST")  # Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
    sour.write("SYST:ZCH OFF") # Turn off zero corrections
    sour.write(":SENS:RANG 0.00001") # SET CURRENT MEASURE RANGE (not needed but stops the device from clicking) """
    print("Resources opened")


    # Display settings for oscilloscope
    setDisplay(osc, 1, settings["voltageRange"], settings["timeRange"], 0)
    sleep(1)

    osc.write(":ACQuire:MODE SEGM") # Aquire mode segmented
    osc.write(":ACQuire:MODE?")
    print("Acquire type "+osc.read())

    osc.write(":ACQuire:SEGMented:COUNt 50") # Set amount of segments to be aquired, max 50
    osc.write(":SAVE:WAVeform:SEGMented ALL") # Choose what segments to save, ALL
    data = osc.write(":SAVE:WMEMory:SOURce 1") # Choose channel to save from

    
    
    

    osc.write(":WAVeform:SEGMented:COUNt?")
    dimSegments = int(osc.read().strip("\n+"))
    print(f"Segments captured: {dimSegments}")
    osc.write("WAV:POIN 1000")


    """ osc.write(":SAVE:FILename 'testTEST'")
    osc.write(":SAVE:FILename?")
    print(osc.read()) """
    osc.write(":SAVE:WAV:FORMat BIN")
    osc.write(":SAVE:WAV:FORMat?")
    print(osc.read())
    osc.write(":SAVE:PWD '\\usb\\'")

    i = 0
    start = time.time()
    while i < 100:
        osc.write(":DIGitize")
        osc.write(f":SAVE:WMEMory 'testTEST{i}'")
        i += 1
    end = time.time()
    print(f"Measuring 5000 points took {end-start} seconds.")

    # 120 s to measure 5000 screens -> SLOWER THAN ORIGINAL

  
    









if settings["closeResources"]:
    osc.close()
    #sour.close()
    print("Resources closed")