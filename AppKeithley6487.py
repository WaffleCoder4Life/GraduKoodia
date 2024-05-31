import pyvisa as visa
import time
import PhotocurrGUI as pg

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
                "UIsetIRan" : f"{next(numbers)} Set current measurement range",
                "UIphotGUI": f"{next(numbers)} Start photocurrent UI",
                "UIswitchOff" : f"{next(numbers)} Output off",
                "UIcloseProgram" : f"{next(numbers)} Close program",
                "UIInfo" : f"{next(numbers)} Help and list of current settings"}
    
    instr.write(":SENS:RANG 0.00001") #Default measurement range to 10e-6 A

    info = "\nNo info available at the moment\n"
    help = "\nVoltage should be given as float\nVoltage range should be given as integer\nCurrent limit should be given as float\n"

    while True:
        #Asking current settings
        #instr.write(":SOUR:VOLT:RANG?")
        #voltRanNow = instr.read()
        #instr.write(":SENS:RANG?")
        #curRanNow = instr.read()
        #instr.write(":SOUR:VOLT:ILIM?")
        #curLimNow = instr.read()
        #info = f"\nPossible output voltage from -505 V to 505 V\n\nSettings at the moment:\nVoltage range: {voltRanNow}\nCurrnent limit: {curLimNow}\nCurrent measurement range: {curRanNow}"

        UIDispl = ""
        for key in settings:
            UIDispl += "\n" + settings[key]
        
        num = input("\nPick a number\n" + UIDispl + "\n")
        
        if num == settings["UIsetV"][0]:
            instr.write(":ABOR")
            try:
                volt = float(input("\nGive voltage: "))
            except:
                print("\nSomething went wrong")
            instr.write(":SYST:ZCH OFF")
            setVoltageFine(instr, volt, currentLimit, voltageRange)
            instr.write(":TRIG:COUNT INF") #Continuous measurement
            instr.write(":INIT")
        
        if num == settings["UIsetVRan"][0]:
            instr.write(":ABOR")
            try:
                vRan = int(input("\nPossible values: 10, 50, 100\nGive voltage range: "))
            except:
                print("\nSomething went wrong")
            voltageRange = vRan
            instr.write(":TRIG:COUNT INF") #Continuous measurement
            instr.write(":INIT")
            print(f"\nVoltage range set to {vRan}")
            time.sleep(2)
        
        if num == settings["UIsetILim"][0]:
            instr.write(":ABOR")
            try:
                iLim = float(input("\nPossible values (25e-6, 250e-6, 2.5e-3, 25e-3)\nGive current limit: ")) #NEED TO FIND POSSIBLE VALUES
            except:
                print("\nSomething went wrong")
            currentLimit = iLim
            instr.write(":TRIG:COUNT INF") #Continuous measurement
            instr.write(":INIT")
            print(f"\nCurrent limit set to {iLim}")
            time.sleep(2)
        
        if num == settings["UIsetIRan"][0]:
            instr.write(":ABOR")
            try:
                iRan = float(input("\nPossible values from -0.021 to 0.021\nGive current measurement range: "))
            except:
                print("\nSomething went wrong")
            instr.write(f":SENS:RANG {iRan}")
            instr.write(":TRIG:COUNT INF") #Continuous measurement
            instr.write(":INIT")
            print(f"Current measurement range set to {iRan}")
            time.sleep(2)
        
        if num == settings["UIphotGUI"][0]:
            try:
                instr.write(":ABOR")
                print("Aborted")
                pg.iScreen(instr)
            except:
                print("\nSomething went wrong, continuing anyway")

        
        if num == settings["UIswitchOff"][0]:
            instr.write(":ABOR")
            instr.write(":SOUR:VOLT:STAT OFF")
        
        if num == settings["UIInfo"][0]:
            instr.write(":ABOR")
            print(info + help)
            instr.write(":TRIG:COUNT INF") #Continuous measurement
            instr.write(":INIT")
        
        if num == settings["UIcloseProgram"][0]:
            print("\nHave a nice day!")
            time.sleep(3)
            break

        

UI()