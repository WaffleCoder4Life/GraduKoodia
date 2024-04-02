import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt
import numpy as np
from array import array
import statistics

def lnDerivative(fileName: str, averagePoints: int) -> np.ndarray:
    """Makes a scatterplot of d/dV ln(I) from sourcemeter data. 
    Returns doctionary of d/dV ln(I) as a function of voltage 
    with keys 'voltage' and 'logDeriv'."""

    voltage = rsf.readSourceMeterDataFine(fileName, 0)
    current = rsf.readSourceMeterDataFine(fileName, 1)
    i = 0
    while i < len(current):
        if current[i] <= 1e-10:
            current.remove(current[i])
            voltage.remove(voltage[i])
        else:
            i += 1
    i = 0
    currentAverage = []
    currentVariance = []
    voltAverage = []

    while i < len(current):
        av = statistics.mean(current[i:i+averagePoints-1])
        v = statistics.pvariance(current[i:i+averagePoints-1])
        va = statistics.mean(voltage[i:i+averagePoints-1])
        currentAverage.append(av)
        currentVariance.append(v)
        voltAverage.append(va)
        i += averagePoints
    logCurrent = [np.log(point) for point in currentAverage]
    

    logCurrentDeriv = []
    voltAver = []
    i=0
    while i < len(logCurrent) - 1:
        voltaver = statistics.mean([voltAverage[i],voltAverage[i+1]])
        currentDeriv = (logCurrent[i+1] - logCurrent[i]) / (voltage[i+1] - voltage[i])
        voltAver.append(voltaver)
        logCurrentDeriv.append(currentDeriv)
        i += 1
    first = np.array([voltAverage, logCurrent])
    result = np.array([voltAver, logCurrentDeriv])

    return result, first
