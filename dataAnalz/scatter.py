import readSourceMeterData as rd
import readOscilloscopeData as readosc
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sympy.solvers import solve
from sympy import Symbol


voltageup = rd.readSourceMeterData("./dataCollection/sweepasdasdasdasd", 0)
currentup = [1000*point for point in rd.readSourceMeterData("./dataCollection/sweepasdasdasdasd", 1)]

#voltagedn = rd.readSourceMeterData("./dataCollection/backwords", 0)
#currentdn = [1000*point for point in rd.readSourceMeterData("./dataCollection/backwords", 1)]

plt.scatter(voltageup, currentup, s=2, c="red", marker="d")
#plt.scatter(voltagedn, currentdn, s=2, c="green", marker="s")
plt.xlabel("$U$ / V")
plt.ylabel("$I$ / mA")
#plt.title("")
plt.tight_layout()
plt.savefig("./dataCollection/Photos/asdasdasdasd")
plt.show()
