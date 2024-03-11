import pyvisa as visa

def close(instr):
    instr.write(":OUTP OFF")