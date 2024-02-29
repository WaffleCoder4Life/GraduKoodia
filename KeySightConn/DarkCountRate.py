import pyvisa as visa
import USABLE.setDisplay as sd
import countPeaks
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit



rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

instr = rm.open_resource(list[0])
instr.write("*IDN?")
print(instr.read())

#Kanava 1: päällä(0/1)
instr.write("CHAN1:DISP 1")

#MUISTA MUUTTAA OIKEIKSI
sd.setDisplay(instr, 0.4, 1)

instr.write(":WAVeform:SOURce CHANnel1")

instr.write( ":WAVeform:FORMat byte")

instr.write("WAVeform:POINTS 8000")

time_scale = float(instr.query(":TIMebase:RANGE?"))
#print(values)
yIncrement = float(instr.query(":WAVeform:YINCREMENT?"))
yOrigin = float(instr.query("WAVeform:YORIGIN?"))

darkCountRate = []
voltageList = []

while True:
  
    voltage = input("Give voltage: ")
    
    if voltage == "Q":
        break
    peakHeight = 0.034
    voltageList.append(float(voltage))

    darkCounts = 0
    i = 0

    #Muuta mittausten määrä tästä!!!!
    mittaukset = 500
    while(i<mittaukset):
        instr.write(":DIGitize")
        #instr.write(":WAVeform:DATA?")
        values = instr.query_binary_values(":WAVeform:DATA?", datatype = "B")
        trueValue=[]
        for value in values:
            # -128 jotta skaalaa binaarit oikein, samoin yincrement ja yorigin
            trueValue.append((value-128)*yIncrement+yOrigin)
        darkCounts += countPeaks.countPeaks(trueValue, peakHeight)
        i+=1
        
    trueTime = mittaukset*time_scale
    #Hz/mm^2, active area = 3.07mm*3.07mm
    dcr = darkCounts/(trueTime*3.07*3.07)


    darkCountRate.append(dcr)

def s(x, a, b):
    return a*x+b
popt, pcov = curve_fit(s,voltageList,darkCountRate)
linliasdas = np.linspace(min(voltageList), max(voltageList), 100)
fit = s(linliasdas, *popt)



plt.figure()
plt.scatter(voltageList, darkCountRate, marker = "s", s = 10, c = "mediumorchid")
plt.xlabel('$U$ / V')
plt.ylabel('$DCR$ / Hz/mm$^2$')
plt.plot(linliasdas, fit)
plt.tight_layout()
plt.show()



