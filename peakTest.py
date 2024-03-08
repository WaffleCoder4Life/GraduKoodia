from KeySightConn import countPeaks as cp
from dataAnalz import readOscilloscopeData as read
from KeySightConn import saveData as save
import pyvisa as visa
from Keithley.setVoltage import setVoltage
from KeySightConn.setDisplay import setDisplay
import os

print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
osc.write("*IDN?")
print(osc.read())

sour = rm.open_resource(list[2])

setVoltage(sour, 1000, 25, 0.015)

setDisplay(osc, 1, 0.04, 1, 0.0035)

save.saveData(osc, "countTest", "")
asd = read.readOscilloscopeData("./dataCollection/countTest", 1)
zxc = max(asd)/3.1
qwe = cp.countPeaks(asd, zxc, len(asd)/20)
print(qwe)
os.remove("./dataCollection/countTest.csv")