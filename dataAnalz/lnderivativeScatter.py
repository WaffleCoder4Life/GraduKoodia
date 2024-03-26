import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt
import numpy as np
from array import array

def lnDerivativeScatter(fileName: str, 
                        markerSize: str = None, 
                        marker: str = None, 
                        color: str = None) -> dict:
    """Makes a scatterplot of d/dV ln(I) from sourcemeter data. 
    Returns doctionary of d/dV ln(I) as a function of voltage 
    with keys 'voltage' and 'logDeriv'."""

    voltageIn = rsf.readSourceMeterDataFine(fileName, 0)
    current = [float(point) for point in rsf.readSourceMeterDataFine(fileName, 1)]
    i = 0
    while i < len(current):
        if current[i] <= 1e-9:
            current.remove(current[i])
        else:
            i += 1
    logCurrent = [np.log(point) for point in current]

    voltage = array("f", [])
    logCurrentDeriv = array("f", [])
    i=0
    while i < len(logCurrent) - 1:
        voltaver = (voltageIn[i] + voltageIn[i+1])/2
        currentDeriv = (logCurrent[i+1] - logCurrent[i]) / (voltageIn[i+1] - voltageIn[i])
        voltage.append(voltaver)
        logCurrentDeriv.append(currentDeriv)
        i += 1
    
    plt.scatter(voltage, logCurrentDeriv, s=markerSize, marker=marker, color=color)
    dic = {"voltage": voltage, "logDeriv": logCurrentDeriv}

    return dic
