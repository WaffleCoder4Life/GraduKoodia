def perform_voltage_sweep(instr, start_voltage, end_voltage, step_voltage):
    # Set sourcemeter to voltage source mode
    instr.write(":SOUR:FUNC VOLT")

    # Set voltage sweep parameters
    instr.write(":SOUR:VOLT:START "+str(start_voltage))
    instr.write(":SOUR:VOLT:STOP "+str(end_voltage))
    instr.write(":SOUR:VOLT:STEP "+str(step_voltage))
    
    # Enable output
    instr.write(":OUTP ON")

    # Initiate voltage sweep
    instr.write(":INIT")

    # Wait for the sweep to complete
    instr.query("*OPC?")

    # Query voltage and current data
    voltages = [float(v) for v in instr.query(":TRAC:DATA? 1, READ").split(',')]
    currents = [float(c) for c in instr.query(":TRAC:DATA? 2, READ").split(',')]

    # Disable output
    instr.write(":OUTP OFF")

    return voltages, currents