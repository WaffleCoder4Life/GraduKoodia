import pyvisa as visa
import deviceControl as cont
from scipy.signal import find_peaks
import time as time
import readOscilloscopeData as rod

settings = {

    # File settings
    "pathNameDate" : "11042024",
    "fileName" : "photonStatistics",
    "testDescribtion" : "Photon counts in 3.77 kOhm",

    # Measurement settings
    "numberOfDatasets" : 1000, # How many pulses are recorded
    "biasVoltage" : 23.5,

    "peakHeight" : 0.0425, # Check before measurement from 1 P.E. height. Use around 80% of 1 P.E. height
    "peakDistance" : 20, # Check before measurement with testSingleShot. If photons not counted -> smaller. If single peaks counted multiple times -> larger

    # Pulse settings
    "pulseTrigger" : 4.7,
    "wgenFreq" : 10E3,
    "wgenFunc" : "PULse",

    # Oscilloscope screen settings
    "timeRange" : 1E-6, # Sets oscilloscope screen width. 20E-6 is good value to use in room temp.
    "photonVamplitude" : 400E-3,
    "pulseVamplitude" : 16,

    # Voltage source default settings
    "biasVoltageRange" : 50,
    "biasCurrentLimit" : 2.5E-3,
    
    # Visa resources
    "oscilloscope" : 'USB0::0x2A8D::0x1797::CN56396144::INSTR',
    "voltageSource" : 'GPIB0::22::INSTR',
    
    "initMes" : 0,
    "aquireData" : 1, # Aquires data and prints out dark count rate.
    "testSingleShot" : 1,
 }


def initializeMeasurement(settings):
    #VISA CONNECTIONS
    rm = visa.ResourceManager()
    osc = rm.open_resource(settings["oscilloscope"]) #Oscilloscope
    sour = rm.open_resource(settings["voltageSource"])
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
    osc.write(":TIMebase:POSition 300E-9")
    print("Oscilloscope display set.")
    # set wave generator
    osc.write(":WGEN:FREQuency "+str(settings["wgenFreq"]))
    osc.write(":WGEN:FUNCtion "+str(settings["wgenFunc"]))
    print("Wavegenerator running")


def testSingleShot(settings):
    """Used to test manually if counts correct amount of counts from single oscilloscope screen. Use to calibrate peak finder peak distance.
       Note that oscilloscope screen might not show the peaks just after the screen that still trigger the count."""
    #VISA CONNECTIONS
    rm = visa.ResourceManager()
    osc = rm.open_resource(settings["oscilloscope"]) #Oscilloscope


    
    cont.saveData(osc, settings["fileName"]+settings["biasVoltage"], settings["fileName"]+settings["biasVoltage"]+" "+settings["testDescribtion"], True) # Aquires data and saves to Temp folder as CSV file
    temp = rod.readOscilloscopeData(settings["pathNameDate"]+"/Temp/"+settings["fileName"]+settings["biasVoltage"], 1)
    

def run(settings):
    if settings["initMes"]:
        initializeMeasurement(settings)
    if settings["testSingleShot"]:
        testSingleShot(settings)

if __name__ == "__main__":
    run(settings)