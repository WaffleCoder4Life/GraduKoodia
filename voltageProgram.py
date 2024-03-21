import pyvisa as visa

#========================SETTINGS========================

settings = {
            "voltageRange" : 50 #(possible values: 10 V, 50 V, 100 V)
            ,"currentLimit" : 2.5e-3
}

#========================================================







id = "GPIB0::22::INSTR"

rm = visa.ResourceManager()
instr = rm.open_resource(id)

#predetermined values if not adjusted in settings
currentLimit = 2.5e-3
voltageRange = 50

#set voltageRange and currentLimit if specified in settings
if settings["voltageRange"] != None:
    voltageRange = settings["voltageRange"]
if settings["currentLimit"] != None:
    currentLimit = settings["currentLimit"]


def setVoltageFine(instrument, voltage_V: float, currentLimit_A: float, voltageRange: float):
    """Set bias voltage range, voltage, current limit and turn output ON"""

    instrument.write(":SOUR:VOLT:RANG "+str(voltageRange))  # Set voltage range, 10 V, 50 V, 100 V
    instrument.write(":SOUR:VOLT:ILIM "+str(currentLimit_A)) #SET CURRENT LIMIT
    instrument.write(":SOUR:VOLT "+str(voltage_V)) #SET VOLTAGE
    instrument.write(":SOUR:VOLT:STAT ON") #OUTPUT ON 

def UI():
    while True:
        print("Voltage range set to 50 V, current limit set to 2.5 mA.\nThese can be changed in the code 'settings'.")
        volt = float(input("Set voltage e.g. 24.5: "))
        setVoltageFine(instr, volt, settings["currentLimit"], settings["voltageRange"])

        off = input("Press enter to switch off")
        if off == "":
            instr.write(":SOUR:VOLT:STAT OFF")
        shutdown = input("Do you want to continue? y/n")
        if shutdown == "n":
            break

UI()