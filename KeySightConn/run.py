import pyvisa as visa
import setDisplay as sd
import string
import struct
import sys
import plotData
import countPeaks




rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
print(instr.read())

#Kanava 1: päällä(0/1)
instr.write("CHAN1:DISP 1")


instr.write(":WAVeform:SOURce CHANnel1")

instr.write( ":WAVeform:FORMat byte")

darkCounts = 0
i = 0
while(i<1):
    instr.write(":DIGitize")
    #instr.write(":WAVeform:DATA?")
    values = instr.query_binary_values(":WAVeform:DATA?", datatype = "s")
    darkCounts += countPeaks.countPeaks(values, 150, 20)
    i+=1

print(darkCounts)
#values = instr.query_binary_values('CURV?', datatype='d', is_big_endian=True)

print(values)
yIncrement = float(instr.query(":WAVeform:YINCREMENT?"))
yOrigin = float(instr.query("WAVeform:YORIGIN?"))
print("Y-increment: ",yIncrement)
print("Y-origin: ",+yOrigin)
trueValue=[]
for value in values:
    trueValue.append(value*yIncrement+yOrigin)


plotData.plotData(trueValue, 10)