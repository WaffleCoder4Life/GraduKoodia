import time

def step_sweep(instr, start_voltage, end_voltage, step_voltage):
    # Set sourcemeter to voltage source mode
    instr.write(":SOUR:FUNC VOLT")

    # Set voltage sweep parameters
    instr.write(":SOUR:VOLT:START "+str(start_voltage))
    instr.write(":SOUR:VOLT:STOP "+str(end_voltage))
    instr.write(":SOUR:VOLT:STEP "+str(step_voltage))

    instr.write(":SOUR:VOLT:MODE SWE")
    instr.write(":SOUR:SWE:RANG AUTO")
    instr.write(":SOUR:SWE:SPAC LIN")

    #Kuinka monta sweeppiä tekee. Aseta yhtä suureksi kuin mittauspisteitä niin ottaa yhden
    #mittauksen per voltage arvo
    points = ((end_voltage-start_voltage)/(step_voltage)+1)
    #points = instr.write("SOUR:SWE:POIN?")
    instr.write(":TRIG:COUN "+str(points))
    print("PISTEITÄ ON "+str(points))

    instr.write(":SOUR:DEL 0.1")



    #Output on
    instr.write(":OUTP ON")

    


    #Trigger sweep and request data
    instr.write(":INIT")

    time.sleep(0.15*(points))

    instr.write(":ABORT")
    


    data = [1,2]



    instr.write(":OUTP OFF")
    return data