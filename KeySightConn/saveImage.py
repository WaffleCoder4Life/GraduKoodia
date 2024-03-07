import pyvisa as visa
import os

def saveImage(instrument, fileName: str):


    path = "./dataCollection/Photos/"+str(fileName)+".png"
    if os.path.isfile(path):
        print("Filename taken (png)")
    else:
        instrument.write(":HARDcopy:INKSaver OFF") #darkmode
        sDisplay = instrument.query_binary_values(":DISPlay:DATA? PNG", datatype = "B", header_fmt = "ieee", container = bytes)
        # Save display data values to file.
        f = open("./dataCollection/Photos/" + fileName + ".png", "wb")
        f.write(sDisplay)
        f.close()