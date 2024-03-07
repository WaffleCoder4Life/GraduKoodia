import readSourceMeterData as rd
import readOscilloscopeData as readosc
import matplotlib.pyplot as plt
import numpy as np



voltage = rd.readSourceMeterData("./dataCollection/voltageSweep1", 0)
current = [1000*point for point in rd.readSourceMeterData("./dataCollection/voltageSweep1", 1)]

plt.scatter(voltage, current, s=2, c="black")
plt.xlabel("U / V")
plt.ylabel("I / mA")
plt.title("Onsemi room temp demo curve")
plt.tight_layout()
plt.savefig("./dataCollection/Photos/IV-curve")
plt.show()
