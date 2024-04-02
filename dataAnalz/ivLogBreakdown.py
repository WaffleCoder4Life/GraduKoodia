import matplotlib.pyplot as plt
import numpy as np
from readSourceMeterDataFine import readSourceMeterDataFine
from scipy.optimize import curve_fit
import statistics

def s(x, a, b):
    return a * x + b

def ivLogBreakdown(fileName: str):
    voltage = readSourceMeterDataFine(fileName, 0)
    currentLin = readSourceMeterDataFine(fileName, 1)
    i = 0
    while i < len(currentLin):
        if currentLin[i] <= 1e-10:
            currentLin.remove(currentLin[i])
            voltage.remove(voltage[i])
        else:
            i += 1
    i = 0
    currentAverage = []
    currentVariance = []
    voltAverage = []

    while i < len(currentLin):
        av = statistics.mean(currentLin[i:i+5])
        v = statistics.pvariance(currentLin[i:i+5])
        va = statistics.mean(voltage[i:i+5])
        currentAverage.append(av)
        currentVariance.append(v)
        voltAverage.append(va)
        i += 5


    currentLog = [np.log10(point) for point in currentAverage]
    data = np.array([voltAverage, currentLog])
    return data


fileName = "./dataCollection/15032024/500uA_sweep"

data = ivLogBreakdown(fileName)

#popt, pcov = curve_fit(s, data[0][:110], data[1][:110])
#print("popt, pcov 1", popt, pcov)
#linV1 = np.linspace(20, 22, 10)
#line1 = s(linV1, *popt)

#popt, pcov = curve_fit(s, data[0][110:210], data[1][110:210])
#print("popt, pcov 2", popt, pcov)
#linV2 = np.linspace(21.1, 22.5, 10)
#line2 = s(linV2, *popt)

plt.scatter(data[0], data[1], color="mediumorchid", marker=".", s=4)
#plt.plot(linV1, line1)
#plt.plot(linV2, line2)
plt.xlabel("$U$ / V")
plt.ylabel("$\log_{10}(I)$")
plt.show()