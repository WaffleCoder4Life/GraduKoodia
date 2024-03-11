import numpy
import matplotlib.pyplot as plt
import readSourceMeterData as rd






voltageup10mA = rd.readSourceMeterData("./dataCollection/11032024sweep_up_10mALED_wide", 0)
currentup10mA = [10**(6)*point for point in rd.readSourceMeterData("./dataCollection/11032024sweep_up_10mALED_wide", 1)]
voltageup20mA = rd.readSourceMeterData("./dataCollection/11032024sweep_up_20mALED_wide", 0)
currentup20mA = [10**(6)*point for point in rd.readSourceMeterData("./dataCollection/11032024sweep_up_20mALED_wide", 1)]
voltageup30mA = rd.readSourceMeterData("./dataCollection/11032024sweep_up_30mALED_wide", 0)
currentup30mA = [10**(6)*point for point in rd.readSourceMeterData("./dataCollection/11032024sweep_up_30mALED_wide", 1)]
voltageup40mA = rd.readSourceMeterData("./dataCollection/11032024sweep_up_40mALED_wide", 0)
currentup40mA = [10**(6)*point for point in rd.readSourceMeterData("./dataCollection/11032024sweep_up_40mALED_wide", 1)]
voltageup50mA = rd.readSourceMeterData("./dataCollection/11032024sweep_up_50mALED_wide", 0)
currentup50mA = [10**(6)*point for point in rd.readSourceMeterData("./dataCollection/11032024sweep_up_50mALED_wide", 1)]
voltageup60mA = rd.readSourceMeterData("./dataCollection/11032024sweep_up_60mALED_wide", 0)
currentup60mA = [10**(6)*point for point in rd.readSourceMeterData("./dataCollection/11032024sweep_up_60mALED_wide", 1)]

#voltagedn = rd.readSourceMeterData("./dataCollection/backwords", 0)
#currentdn = [1000*point for point in rd.readSourceMeterData("./dataCollection/backwords", 1)]

plt.scatter(voltageup10mA, currentup10mA, s=2, c="indigo", marker="d", label = "10 mA")
plt.scatter(voltageup20mA, currentup20mA, s=2, c="blue", marker="d", label = "20 mA")
plt.scatter(voltageup30mA, currentup30mA, s=2, c="green", marker="d", label = "30 mA")
plt.scatter(voltageup40mA, currentup40mA, s=2, c="gold", marker="d", label = "40 mA")
plt.scatter(voltageup50mA, currentup50mA, s=2, c="darkorange", marker="d", label = "50 mA")
plt.scatter(voltageup60mA, currentup60mA, s=2, c="red", marker="d", label = "60 mA")
#plt.scatter(voltagedn, currentdn, s=2, c="green", marker="s")
plt.xlabel("$U$ / V")
plt.ylabel("$I$ / $\\mathrm{\\mu}$A")
#plt.ylim(-0.5, 0.5)
#plt.title("")
plt.legend()
plt.tight_layout()
plt.savefig("./dataCollection/Photos/IVcurves1k")
plt.show()






