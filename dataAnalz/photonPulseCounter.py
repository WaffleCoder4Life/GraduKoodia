import pyvisa as visa
import deviceControl as cont
from scipy.signal import find_peaks
import time as time
import readOscilloscopeData as rod
import os
import scipy.integrate as integ
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


settings = {

    # File settings
    "pathNameDate" : "26042024",
    "fileName" : "photonStatistics5V",
    "testDescribtion" : "Photon counts in 3.72 kOhm",
    "plotName" : "photonDistribution1_88kOhm5.5V",
    "fileNamePhotonDistribution" : "photonDistribution1_88kOhm5.5VLED",

    # Measurement settings
    "numberOfDatasets" : 50, # How many pulses are recorded
    "biasVoltage" : "23",

    "peakHeight" : 0.09, # Check before measurement from 1 P.E. height. Use around 80% of 1 P.E. height
    "peakDistance" : 15, # Check before measurement with testSingleShot. If photons not counted -> smaller. If single peaks counted multiple times -> larger
    "peakProminence" : 0.055, # How much peak must stand out from signal, use around 1/2 of peak height

    # Pulse settings
    "pulseTrigger" : 4,
    "wgenFreq" : 1E3,
    "wgenWidth" : 150E-9,
    "wgenVolt" : 6,
    "wgenFunc" : "PULse",

    # Oscilloscope screen settings
    "timeRange" : 0.5E-6, # Sets oscilloscope screen width. 20E-6 is good value to use in room temp.
    "photonVamplitude" : 800E-3,
    "pulseVamplitude" : 16,

    # Voltage source default settings
    "biasVoltageRange" : 50,
    "biasCurrentLimit" : 2.5E-3,
    
    # Visa resources
    "oscilloscope" : 'USB0::0x2A8D::0x1797::CN56396144::INSTR',
    "voltageSource" : 'GPIB0::22::INSTR',
    "connectVisa" : 1,
    "closeVisa" : 1,
    "outputOff" : 0,
    
    "initMes" : 1,
    "aquireData" : 0, # Aquires data and plots photon distribution.
    "aquireDataHeight" : 0,
    "testSingleShot" : 0, # Use to calibrate peak height and prominance before aquiering data
 }

    #VISA CONNECTIONS
if settings["connectVisa"]:
    rm = visa.ResourceManager()
    osc = rm.open_resource(settings["oscilloscope"]) #Oscilloscope
    sour = rm.open_resource(settings["voltageSource"])



def initializeMeasurement(settings):
    """Set oscilloscope screen, bias voltage and pulse generator settings and turn them on."""
    # set voltage source
    sour.write("*RST")  # Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
    sour.write("SYST:ZCH OFF") # Turn off zero corrections
    sour.write(":SENS:RANG 0.00001") # SET CURRENT MEASURE RANGE (not needed but stops the device from clicking)
    cont.setVoltageFine(sour, settings["biasVoltageRange"], settings["biasVoltage"], settings["biasCurrentLimit"])
    sour.write(":TRIG:COUNT INF") #Continuous measurement
    sour.write(":INIT") # Not needed but shows the continous current on source display
    print("Bias voltage set.")

    # set oscilloscope display
    cont.setDisplay(osc, 1, settings["photonVamplitude"], settings["timeRange"], 0)
    cont.setDisplay(osc, 2, settings["pulseVamplitude"], settings["timeRange"], settings["pulseTrigger"])
    osc.write(":TIMebase:POSition 150E-9")
    osc.write(":TRIG:MODE EDGE")
    print("Oscilloscope display set.")

    # set wave generator
    osc.write(":WGEN:FREQuency "+str(settings["wgenFreq"]))
    osc.write(":WGEN:FUNCtion "+str(settings["wgenFunc"]))
    osc.write(":WGEN:FUNCtion:PULSe:WIDTh "+str(settings["wgenWidth"]))
    osc.write(":WGEN:VOLTage:LOW 0")
    osc.write(":WGEN:VOLTage:HIGH "+str(settings["wgenVolt"]))
    osc.write(":WGEN:OUTPut 1")
    print("Wavegenerator running")

def closeAll(settings):
    if settings["outputOff"]:
        osc.write(":WGEN:OUTPut 0")
        sour.write(":SOUR:VOLT:STAT OFF")
    time.sleep(0.5)
    if settings["closeVisa"]:
        osc.close()
        sour.close()

def testSingleShot(settings):
    """Used to test manually if counts correct amount of counts from single oscilloscope screen. Use to calibrate peak finder peak distance.
       Note that oscilloscope screen might not show the peaks just after the screen that still trigger the count."""


    yIncrement = float(osc.query(":WAVeform:YINCREMENT?"))
    yOrigin = float(osc.query("WAVeform:YORIGIN?"))
    voltageData = [(point-128)*yIncrement+yOrigin for point in osc.query_binary_values(":WAVeform:DATA?", datatype = "B")]
    peaks = find_peaks(voltageData, settings["peakHeight"], distance = settings["peakDistance"], prominence=settings["peakProminence"])
    print(peaks[0])
    print(f"{len(peaks[0])} fotons detected")

    """Area testing, inaccurate results"""
    if False:
        cont.saveData(osc, settings["fileName"]+str(settings["biasVoltage"]), settings["fileName"]+str(settings["biasVoltage"])+" "+settings["testDescribtion"], True) # Aquires data and saves to Temp folder as CSV file
        temp = rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+str(settings["biasVoltage"]), 1)
        print(len(temp))
        timeAxis = rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+settings["biasVoltage"], 0)[200:]
        background = np.array(temp[:200])
        backAverag = np.mean(background)
        print(backAverag)
        voltage = [point-backAverag for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+str(settings["biasVoltage"]), 1)[200:]]
        area = integ.simps(voltage, timeAxis, dx = 1, even = "avg")
        totalCharge = area / (223.87*50*1.602*10**-19)
        print(f"total charge is {totalCharge}")
        print(f"{totalCharge/(3.832E6)} photons detected")

        os.remove("./dataCollection/" + settings["pathNameDate"]+"/Temp/"+settings["fileName"]+settings["biasVoltage"]+".csv")

def aquireData(settings):
    yIncrement = float(osc.query(":WAVeform:YINCREMENT?"))
    yOrigin = float(osc.query("WAVeform:YORIGIN?"))
    osc.write(":RUN")

    photonDistribution = np.empty((settings["numberOfDatasets"]))
    i = 0
    before = time.time()
    while i < settings["numberOfDatasets"]:
        voltageData = [(point-128)*yIncrement+yOrigin for point in osc.query_binary_values(":WAVeform:DATA?", datatype = "B")]
        peaks = find_peaks(voltageData, settings["peakHeight"], distance = settings["peakDistance"], prominence=0.02)
        photonNumber = int(len(peaks[0]))
        photonDistribution[i] = photonNumber
        i += 1
    after = time.time()
    print(str(settings["numberOfDatasets"])+f" meaurements took {after-before} seconds.")
    # Saves array to csv file incase something goes wrong with plotting and stuff
    with open("./dataCollection/"+settings["pathNameDate"]+"/"+settings["fileNamePhotonDistribution"]+str(settings["biasVoltage"])+".csv", "ab") as f:
        f.write(b"\n")
        np.savetxt(f, photonDistribution, delimiter=",")
        f.close()
   
    
    

    # Count mean value of photons
    photonCounts = Counter(photonDistribution)
    print(photonCounts)
    poisson_lambda = 0
    for key in photonCounts:
        poisson_lambda += int(key)*int(photonCounts[key])
    poisson_lambda /= settings["numberOfDatasets"]
    print(f"Mean value of photons {poisson_lambda}")
    poisdata = np.random.poisson(poisson_lambda, 10000*settings["numberOfDatasets"])

    labels, counts = np.unique(photonDistribution, return_counts=True)
    
    plt.bar(labels, counts, width = 1, color = "darkorange", edgecolor = "black", align='center', linestyle = "--", label = "measurement")
    labels = [point for point in range(-1, len(counts), 1)]
    plt.gca().set_xticks(labels)
    
    labels2, counts2 = np.unique(poisdata, return_counts=True)
    counts2 = [point/10000 for point in counts2[:18]]
    labels2 = [point for point in range(-1, len(counts2), 1)]
    counts2.insert(0, 0)
    plt.step(labels2, counts2, "k", linewidth = 1, where = "mid", label = "Poissonian fit $\\mathrm{\\lambda}$="+str(poisson_lambda))
    
    plt.xlabel("photoelectron")
    plt.ylabel("counts")
    plt.legend()
    plt.xlim(-0.5,len(counts))
    plt.savefig("./dataCollection/"+str(settings["pathNameDate"])+"/Photos/"+settings["plotName"]+str(settings["biasVoltage"])+".png")
    plt.show()

def aquireDataHeight(settings):
    i = 1
    chargeList = []
    osc.write(":MEASure:VAMPlitude MATH")
    osc.write(":RUN")
    time.sleep(1)
    while i < settings["numberOfDatasets"]:
        osc.write(":MEAS:VAMP?")
        data = osc.read()
        chargeList.append(data)
        # cont.saveData(osc, settings["fileName"]+str(settings["biasVoltage"]), settings["fileName"]+str(settings["biasVoltage"])+" "+settings["testDescribtion"], True) # Aquires data and saves to Temp folder as CSV file
        # temp = rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+str(settings["biasVoltage"]), 1)
        # timeAxis = rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+settings["biasVoltage"], 0)[200:]
        # background = np.array(temp[:200])
        # backAverag = np.mean(background)
        # voltage = [point-backAverag for point in rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+str(settings["biasVoltage"]), 1)[200:]]
        # height = max(voltage) - min(voltage)
        # chargeList.append(height)
        # os.remove("./dataCollection/" + settings["pathNameDate"]+"/Temp/"+settings["fileName"]+settings["biasVoltage"]+".csv")
        i += 1
    with open("./DataCollection/"+settings["pathNameDate"]+"/"+"HeightListMath"+settings["biasVoltage"]+".csv", "a") as file:
        for data in chargeList:
            file.write(f"{data}")

    

def run(settings):
    if settings["initMes"]:
        initializeMeasurement(settings)
    if settings["testSingleShot"]:
        testSingleShot(settings)
    if settings["aquireData"]:
        aquireData(settings)
    if settings["aquireDataHeight"]:
        aquireDataHeight(settings)
    
    closeAll(settings)

if __name__ == "__main__":
    run(settings)