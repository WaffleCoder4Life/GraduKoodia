import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt
import numpy as np
from sympy import Symbol


voltage = rsf.readSourceMeterDataFine("dataCollection/13032024_FINE_sweep_up_1mALED", 0) #SAME VOLTAGE VALUE FOR ALL

laserIntensity = ["1mA", "5mA", "10mA"]
colours = ["gold", "darkorange", "red"]


#CREATES DICTIONARY WITH KEY - CURRENT LIST.
d = {}
for amps in laserIntensity:
    d["LED {0}".format(amps)] = rsf.readSourceMeterDataFine("dataCollection/13032024_FINE_sweep_up_{0}LED".format(amps), 1) #SAVE CURRENT LIST IN DICTIONARY





i = 0
for key in d:
    plt.scatter(voltage, d[key], s=2, c=colours[i], marker="d", label = str(key))
    i+=1

plt.xlabel("$U$ / V")
plt.ylabel("$I$ / $\\mathrm{\\mu}$A")
plt.legend()
plt.tight_layout()
plt.savefig("./dataCollection/Photos/130324IVcurvesFINE")
plt.show()