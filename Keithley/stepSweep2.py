

def step_sweep2(instr):



    instr.write(":SOUR:VOLT:MODE LIST")
    instr.write(":SOUR:LIST:VOLT 0.1,0.2,0.3,0.4,0.5")

    instr.write(":TRIG:COUN 4")

    instr.write(":SOUR:DEL 0.1")

    instr.write(":OUTP ON")

    instr.write("READ?")

    instr.write(":CABORT LATE")

    instr.write(":OUTP OFF")

    