import pyvisa as visa
import KeySightConn.generatePulses as gen
import KeySightConn.saveData as save
import KeySightConn.setDisplay as set
import Keithley.voltageSweep as vs
import Keithley.setVoltage as sv
import dataAnalz.readSourceMeterData as rd
import matplotlib.pyplot as plt
import keyboard



print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

#osc = rm.open_resource(list[0])
sour = rm.open_resource(list[1])
#osc.write("*IDN?")
#print(osc.read())

#set.setDisplay(osc, 1, 0.008, 0.5, 0)
#set.setDisplay(osc, 2, 24, 5000000, 1)

#osc.write(":RUN")


fileName = "11032024sweep_down_60mALED_wide"



#sv.setVoltage(sour, 50, 24, 0.0150)

vs.voltageSweep(sour, 1000, 19.5, 23, 0.0150, fileName, "", True)
#vs.voltageSweep(sour, 1000, 19, 23, 100, 0.0150, "backwords", "After nitrogen cooling, Dark, BIAS 18V-24V", True)









voltageup = rd.readSourceMeterData("./dataCollection/" + fileName, 0)
currentup = [10**(6)*point for point in rd.readSourceMeterData("./dataCollection/" + fileName, 1)]

#voltagedn = rd.readSourceMeterData("./dataCollection/backwords", 0)
#currentdn = [1000*point for point in rd.readSourceMeterData("./dataCollection/backwords", 1)]

plt.scatter(voltageup, currentup, s=2, c="red", marker="d")
#plt.scatter(voltagedn, currentdn, s=2, c="green", marker="s")
plt.xlabel("$U$ / V")
plt.ylabel("$I$ / $\\mu$A")
#plt.ylim(-0.5, 0.5)
#plt.title("")
plt.tight_layout()
plt.savefig("./dataCollection/Photos/" + fileName)
plt.show()


