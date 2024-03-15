import numpy as np
import averagefrfr as av
import readOscilloscopeData as rod
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


#AVERAGE OF 10 SINGLE COUNTS IN ~1K WITH 24 V BIAS

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_prop_cycle('color',[plt.cm.jet(i) for i in np.linspace(0, 1, 10)])

#SAVE DATASETS FROM 10 DARKCOUNTS TO A LIST AND CHANGES V TO mV
#SCATTERPLOT OF ALL DATASETS WITH us TIME AXIS
i = 1
datasets = []
while i <= 10:
    tempor = [1E3 * point for point in rod.readOscilloscopeData("15032024/darkcount{0}".format(str(i)), 1)]
    datasets.append(tempor)
    ax1.plot([1E6 * point for point in rod.readOscilloscopeData("15032024/darkcount{0}".format(str(i)), 0)], tempor)
    i += 1

print(len(tempor))
print(len(rod.readOscilloscopeData("15032024/darkcount10", 0)))

#AVERAGE OF BACKGROUND FROM ALL DATASETS FROM START TO PULSE
#AVERAGE OF THE AVERAGE: TO BE SUBTRACTED FROM PULSE DATA TO COMPENSATE BG
BGaverage = av.averageData(10, [dataset[:950] for dataset in datasets])

BGcorrectiontemp = 0
for point in BGaverage:
    BGcorrectiontemp = BGcorrectiontemp + point
BGcorrection = BGcorrectiontemp / len(BGaverage)
print(BGcorrection)

#AVERAGE PULSE DATA FROM ALL DATASETS AND SUBTRACT BG CORRECTION
pulseaveragetemp = av.averageData(10, [dataset[950:1600] for dataset in datasets])
pulseaverage = [point - BGcorrection for point in pulseaveragetemp]

ax2.plot([1E6 * point for point in rod.readOscilloscopeData("15032024/darkcount1", 0)[:650]], pulseaverage, c="black")
ax1.set_xlabel("$t$ / $\\mathrm{\\mu}$s")
ax1.set_ylabel("$U$ / mV")
ax2.set_xlabel("$t$ / $\\mathrm{\\mu}$s")
ax2.set_ylabel("$U$ / mV")
#plt.set_cmap(colors)
fig.tight_layout()
plt.show()