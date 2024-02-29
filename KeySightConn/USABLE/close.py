import pyvisa as visa


def close(instr: str):
    

    instr.write("WGEN:OUTPut1 0")
    instr.write(":CHANnel1:DISPlay 0")
    instr.write(":CHANnel2:DISPlay 0")
    instr.write(":STOP")
    instr.close()