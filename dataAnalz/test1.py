import readSourceMeterData as rd
import readOscilloscopeData as readosc
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sympy.solvers import solve
from sympy import Symbol

def f(x, a, b, c):
    return a*(np.exp(b*(x-c))-1) #diode eq

def g(x, a, b):
    return a*x+b

linV1 = np.linspace(14, 21.5, 100)
linV2 = np.linspace(21, 23, 100)
linV3 = np.linspace(14, 23, 1000)

voltage = rd.readSourceMeterData("./dataCollection/voltageSweep40K", 0)
current = [1000*point for point in rd.readSourceMeterData("./dataCollection/voltageSweep40K", 1)]

voltages1 = voltage[:40]
currents1 = current[:40]
voltages2 = voltage[-17:]
currents2 = current[-17:]

popt, pcov = curve_fit(g, voltages1, currents1)
popt1 = popt
pcov1 = pcov
print("popt1, pcov1:", popt1, pcov1)
fit1 = g(linV1, *popt)

popt, pcov = curve_fit(g, voltages2, currents2)
popt2 = popt
pcov2 = pcov
print("popt2, pcov2:", popt2, pcov2)
fit2 = g(linV2, *popt)

x = Symbol('x')
inters = solve(g(x, *popt1) - g(x, *popt2), x)
print(inters)

#voltages3 = voltage[50:]
#currents3 = current[50:]
#guess = [0.000000000000001, 10, 21]
#popt, pcov = curve_fit(f, voltages3, currents3, p0=guess)
#fit3 = f(linV3, *popt)

plt.scatter(voltage, current, s=2, c="black")
#plt.plot(linV3, fit3)
plt.plot(linV1, fit1)
plt.plot(linV2, fit2)
plt.xlabel("$U$ / V")
plt.ylabel("$I$ / mA")
plt.title("Room temp, LED 6 V")
plt.tight_layout()
plt.savefig("./dataCollection/Photos/IV-curve")
plt.show()
