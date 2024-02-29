import time



def manualSweep(instr, start_voltage, end_voltage, sweep_points, current_limit, tiedosto):

    instr.write(":SOUR:FUNC VOLT")

    #MUISTA MUUTTAA
    range = 1
    instr.write(":SOUR:VOLT:RANG "+str(range))  # Set voltage range
    # Set the maximum current limit
    instr.write(":SENS:CURR:PROT "+str(current_limit))


    voltage_step = (end_voltage-start_voltage)/sweep_points

    voltage_step = voltage_step / range
    start_voltage = start_voltage / range
    end_voltage = end_voltage / range

    voltage = start_voltage


    voltage_data = []
    current_data = []
    resistance_data = []
    
    instr.write(":OUTP ON")

    
    with open(tiedosto+".csv", "a") as file:
        while voltage < end_voltage:
            instr.write(":SOUR:VOLT "+str(voltage))  # Set voltage
            #instr.write(":TRACe:DATA?")
            time.sleep(0.2)
            instr.write(":FORM:ELEM VOLT, CURR, RES")
            file.write(instr.read())
            
            voltage += voltage_step

    instr.write(":OUTP OFF")

        
        