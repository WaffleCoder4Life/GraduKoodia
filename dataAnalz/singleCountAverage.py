import numpy as np
import averagefrfr as av
import readOscilloscopeData as rod
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import scipy.integrate as integ
import array

numberOfSets = 10

#AVERAGE OF 10 SINGLE COUNTS IN ~1K WITH 24 V BIAS
#print(list(cm._colormaps)) #LIST OF COLORMAPS :)
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.set_prop_cycle('color',[cm.Greens(i) for i in np.linspace(0, 1, numberOfSets)])

#SAVE DATASETS FROM 10 DARKCOUNTS TO A LIST AND CHANGES V TO mV
#SCATTERPLOT OF ALL DATASETS WITH us TIME AXIS
i = 1
datasets = []
while i <= numberOfSets:
    tempor = [1E3 * point for point in rod.readOscilloscopeData("15032024/darkcount{0}".format(str(i)), 1)]
    datasets.append(tempor)
    ax1.plot([1E6 * point for point in rod.readOscilloscopeData("15032024/darkcount{0}".format(str(i)), 0)], tempor)
    i += 1

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
timeavg = [point for point in rod.readOscilloscopeData("15032024/darkcount1", 0)[:650]]

#INTEGRATION USING SIMPSON'S RULE
pulaver = array.array("f", pulseaverage)
area = 1E-3 * integ.simps(pulaver, timeavg, dx=1, even="avg")
areaforimage = 1E11 * area #MIGHT NEED ADJUSTMENT DEPENDING ON DATASETS
print(area)

ax2.plot([1E6 * point for point in rod.readOscilloscopeData("15032024/darkcount1", 0)[:650]], pulseaverage, c="black", label="Average\nArea: {:.5f}".format(areaforimage) + "e-11")
ax1.set_xlabel("$t$ / $\\mathrm{\\mu}$s")
ax1.set_ylabel("$U$ / mV")
ax1.set_title("$R_{\\mathrm{T}}$=1.666 k$\\Omega$, SiPM bias: 24 V")
ax2.set_xlabel("$t$ / $\\mathrm{\\mu}$s")
ax2.set_ylabel("$U$ / mV")
ax2.legend()
fig.tight_layout()
plt.savefig("./dataCollection/15032024/Photos/10singlecount_average1K.png")
plt.show()