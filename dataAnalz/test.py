import readSourceMeterData as rd
import readOscilloscopeData as readosc
import matplotlib.pyplot as plt
import numpy as np
from array import array
from scipy import integrate

""" voltageStr = rd.readData("./dataCollection/test1_1_3_24",0)
currentStr = rd.readData("./dataCollection/test1_1_3_24",1)

voltage = [float(volt) for volt in voltageStr]
current = [float(cur) for cur in currentStr]

voltage2 = [float(volt) for volt in rd.readData("./dataCollection/test2_1_3_24",0)]
current2 = [float(curr) for curr in rd.readData("./dataCollection/test2_1_3_24",1)]


#Tää riittää kun fixas floatiks suoraan readDatan
current3 = rd.readSourceMeterData("./dataCollection/test3_1_3_24", 1)

currAvag = [float((cur1+cur2)/2) for (cur1,cur2) in zip(current,current2)]
 """

""" i = 0
while i < len(current):
    print("U: " + voltage[i] + ", I: " + current[i])
    i+=1 """

""" fig, ax = plt.subplots()
ax.scatter(voltage, current, s=2, c="blue")
ax.scatter(voltage2, current2, s=2, c="red")
ax.scatter(voltage, current3, s=2, c="yellow")


ax.set(xlim=(voltage[0], voltage[-1]), ylim=(min(current), current[-1])) """

time = readosc.readOscilloscopeData("./dataCollection/pulsetest_7V100ns4",0)
voltage = readosc.readOscilloscopeData("./dataCollection/pulsetest_7V100ns4",1)
voltagePulse = voltage[500:]
time2 = time[500:]
#TAUSTA
voltagePulseBack = voltage[:500]
voltageTimeBack = time[:500]

timeDark = readosc.readOscilloscopeData("./dataCollection/darkcount5",0)
voltageDark = readosc.readOscilloscopeData("./dataCollection/darkcount5",1)
voltageDarkPeak = voltageDark[1600:2400]
timeDarkPeak = timeDark[1600:2400]
#TAUSTA
voltageDarkBack = voltageDark[:800]
timeDarkBack = timeDark[:800]



plt.scatter(time2, voltagePulse, s=2, c="blue")
plt.scatter(timeDarkPeak, voltageDarkPeak, s=2, c="yellow")

plt.show()


voltArrPulse = array("f", voltagePulse)
voltArrPulseBack = array("f", voltagePulseBack)

voltArrayDark = array("f", voltageDarkPeak)
voltaArrayDarkBack = array("f", voltageDarkBack)

integrandPulse = integrate.simps(voltArrPulse, x=None, dx=1, axis=-1, even='avg')-integrate.simps(voltArrPulseBack, x=None, dx=1, axis=-1, even='avg')
integrandDark = integrate.simps(voltArrayDark, x=None, dx=1, axis=-1, even='avg')-integrate.simps(voltaArrayDarkBack, x=None, dx=1, axis=-1, even='avg')


print("pulssi",integrandPulse)
print("dark",integrandDark)
print("Photons; ",integrandPulse/integrandDark)
