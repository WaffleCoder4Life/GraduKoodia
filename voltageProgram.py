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
                "UIcloseProgram" : f"{next(numbers)} Close program",
                "UIInfo" : f"{next(numbers)} Help and list of current settings"}
    
    instr.write(":SENS:RANG 0.00001") #CURRENT MEASURE RANGE FUTURE FEATURE
    instr.write(":TRIG:COUNT INF")

    help = "\nVoltage should be given as float\nVoltage range should be given as integer\nCurrent limit should be given as float\n"

    while True:
        info = f"\nSettings at the moment:\nVoltage range: {voltageRange}\nCurrnent limit: {currentLimit}"

        UIDispl = ""
        for key in settings:
            UIDispl += "\n" + settings[key]
        
        num = input("\nPick a number\n" + UIDispl + "\n")
        
        if num == settings["UIsetV"][0]:
            instr.write(":ABOR")
            try:
                volt = float(input("Give voltage: "))
            except:
                print("Something went wrong")
            #instr.write(":SYST:ZCH:STAT?")
            #check = instr.read()
            #if check == "+1": #NEEDS TROUBLESHOOTING
            instr.write(":SYST:ZCH OFF")
            setVoltageFine(instr, volt, currentLimit, voltageRange)
            instr.write(":INIT")

        
        if num == settings["UIsetVRan"][0]:
            instr.write(":ABOR")
            try:
                vRan = int(input("Possible values: 10, 50, 100\nGive voltage range: "))
            except:
                print("Something went wrong")
            voltageRange = vRan
            print(f"Voltage range set to {vRan}")
        
        if num == settings["UIsetILim"][0]:
            instr.write(":ABOR")
            try:
                iLim = float(input("Give current limit: ")) #NEED TO FIND POSSIBLE VALUES
            except:
                print("Something went wrong")
            currentLimit = iLim
            print(f"Current limit set to {iLim}")
        
        if num == settings["UIswitchOff"][0]:
            instr.write(":ABOR")
            instr.write(":SOUR:VOLT:STAT OFF")
        
        if num == settings["UIInfo"][0]:
            instr.write(":ABOR")
            print(info + help)
        
        if num == settings["UIcloseProgram"][0]:
            break

        

UI()