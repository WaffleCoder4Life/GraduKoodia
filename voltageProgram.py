import pyvisa as visa

#Usable on Keithley 6487 source-meter


id = "GPIB0::22::INSTR"

rm = visa.ResourceManager()
instr = rm.open_resource(id)

def setVoltageFine(instrument, voltage_V: float, currentLimit_A: float, voltageRange: float):
    """Set bias voltage range, voltage, current limit and turn output ON"""

    instrument.write(":SOUR:VOLT:RANG "+str(voltageRange))  # Set voltage range, 10 V, 50 V, 100 V
    instrument.write(":SOUR:VOLT:ILIM "+str(currentLimit_A)) #SET CURRENT LIMIT
    instrument.write(":SOUR:VOLT "+str(voltage_V)) #SET VOLTAGE
    instrument.write(":SOUR:VOLT:STAT ON") #OUTPUT ON 



def UI():
    instr.write("*RST")

    #predetermined values if not adjusted in settings
    currentLimit = 2.5e-3
    voltageRange = 50
    
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    numbers = iter(nums)
    settings = {"UIsetV" : f"{next(numbers)} Set voltage",
                "UIsetVRan" : f"{next(numbers)} Set voltage range",
                "UIsetILim" : f"{next(numbers)} Set current limit",
                "UIswitchOff" : f"{next(numbers)} Output off",
                "UIInfo" : f"{next(numbers)} Help and list of current settings",
                "UIcloseProgram" : f"{next(numbers)} Close program"}
    

    while True:
        info = f"Settings at the moment:\nVoltage range: {voltageRange}\nCurrnent limit: {currentLimit}"
        num = input("Pick a number\n"+settings["UIsetV"]+"\n"+settings["UIsetVRan"]+"\n"+settings["UIsetILim"]+"\n"+settings["UIInfo"])
        
        if num == settings["UIsetV"][0]:
            try:
                volt = float(input("Give voltage: "))
            except TypeError:
                print("Must be given as a float e.g. 24.5")
            instr.write(":SYST:ZCH:STAT?")
            if instr.read() == "1":
                instr.write(":SYST:ZCH OFF")
            setVoltageFine(instr, volt, currentLimit, voltageRange)
        
        if num == settings["UIsetVRan"][0]:
            try:
                vRan = int(input("Possible values: 10, 50, 100\nGive voltage range: "))
            except TypeError:
                print("Must be given as int e.g. 10")
            voltageRange = vRan
            print(f"Voltage range set to {vRan}")
        
        if num == settings["UIsetILim"][0]:
            try:
                iLim = float(input("Give current limit: "))
            except TypeError:
                print("Must be given as a float e.g. 2.5e-3")
            currentLimit = iLim
            print(f"Current limit set to {iLim}")
        
        if num == settings["UIswitchOff"][0]:
            instr.write(":SOUR:VOLT:STAT OFF")
        
        if num == settings["UIInfo"][0]:
            print(info)
        
        if num == settings["UIcloseProgram"][0]:
            break

        

UI()