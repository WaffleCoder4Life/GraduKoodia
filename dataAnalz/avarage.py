import readSourceMeterDataFine as rsf
import numpy as np
import matplotlib.pyplot as plt
from array import array
from scipy.signal import savgol_filter
from scipy.signal import lfilter

voltage = array("f", rsf.readSourceMeterDataFine("dataCollection/14032024_FINE_sweep_up_1mALED_1", 0))

run = ["1", "2", "3", "4"]

curr = {}
for ind in run:
    curr[ind] = array("f", rsf.readSourceMeterDataFine("dataCollection/14032024_FINE_sweep_up_1mALED_{0}".format(ind), 1))

average = array("f", [])

i = 0
while i < len(curr["1"]):
    av = 0
    for key in curr:
        av = av + curr[key][i]
    average.append(av / len(curr))
    i += 1

w = savgol_filter(average, len(average), 6) # SAVGOL

n = 10
b = [1 / n] * n
a = 1
ww = lfilter(b, a, average[:60])

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.scatter(voltage, average, s=4, c="black")
ax1.scatter(voltage, array("f", curr["1"]), s=4, c="orange")
ax1.scatter(voltage, w, s=4, c="magenta")
ax1.scatter(voltage[:60], ww, s=4, c="green")
ax1.scatter(voltage[60:], average[60:], s=4, c="green")
ax2.set_yscale("log")
ax2.scatter(voltage, average, s=4, c="black")
ax2.scatter(voltage, w, s=4, c="magenta")
ax2.scatter(voltage[:60], ww, s=4, c="green")
ax2.scatter(voltage[60:], average[60:], s=4, c="green")
fig.tight_layout()
fig.savefig("dataCollection/Photos/testsmoothing.png")
fig.show()