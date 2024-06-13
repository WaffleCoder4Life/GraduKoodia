import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from sympy import Symbol
import logScatter as logplot
import readOscilloscopeData as rosc


#Write all different laserIntensities to list and same amount of colors for plotting. 'today' needs to be changed (different file locations for each day)

 
laserIntensity = ["100uA", "200uA"]



colours = ["indigo","blue","lightseagreen","green","yellowgreen","gold", "darkorange", "red"]
colours1 = [cm.inferno(i) for i in np.linspace(0, 1, 6)]
colours2 = [cm.inferno(i) for i in np.linspace(1, 2, 6)]

#CHANGE PATH NAME BY CHANGING DATE
fileDate1 = "04042024"
bdvoltage1 = 24.5
fileDate2 = "05062024"
bdvoltage2 = 24.5

# Image save settings
fileDateImag = "06062024"
name = "IVcompareRoomTempDiffSetups"


def bdvoltageIndex(fileDate, bdvolt, index):
    data = [round(point,1) for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate+"/{0}_sweep".format(laserIntensity[index]), 0)]
    return data.index(bdvolt)

print(bdvoltageIndex(fileDate2, bdvoltage2, 0))


#CREATES dICTIONARY WITH KEY - VOLTAGE LIST
voltdic1 = {}
i = 0
for amps in laserIntensity:
    voltdic1["LED {0}".format(amps)] = [point-bdvoltage1 for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate1+"/{0}_sweep".format(amps), 0)[bdvoltageIndex(fileDate1, bdvoltage1, i):bdvoltageIndex(fileDate1, bdvoltage1+2.4, i)]] #SAVE VOLTAGE LIST IN DICTIONARY
    i += 1
i = 0
voltdic2 = {}
for amps in laserIntensity:
    voltdic2["LED {0}".format(amps)] = [point - bdvoltage2 for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate2+"/{0}_sweep".format(amps), 0)[bdvoltageIndex(fileDate2, bdvoltage2, i):bdvoltageIndex(fileDate2, bdvoltage2+2.4, i)]] #SAVE VOLTAGE LIST IN DICTIONARY
    i += 1

#CREATES DICTIONARY WITH KEY - CURRENT LIST.
curdic1 = {}
i = 0
for amps in laserIntensity:
    curdic1["LED {0}".format(amps)] = [1E6 * point for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate1+"/{0}_sweep".format(amps), 1)[bdvoltageIndex(fileDate1, bdvoltage1, i):bdvoltageIndex(fileDate1, bdvoltage1+2.4, i)]] #SAVE CURRENT LIST IN DICTIONARY
    i += 1
curdic2 = {}
i = 0
for amps in laserIntensity:
    curdic2["LED {0}".format(amps)] = [1E6 * point for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate2+"/{0}_sweep".format(amps), 1)[bdvoltageIndex(fileDate2, bdvoltage2, i):bdvoltageIndex(fileDate2, bdvoltage2+2.4, i)]]
    i += 1


fig, ax1 = plt.subplots()
# Plots all IV-curves to same image
i = 0
for key1, key2 in zip(curdic1, voltdic1):
    ax1.scatter(voltdic1[key2], curdic1[key1], s=8, facecolors='none', edgecolors=colours[i], cmap="inferno", label = "Original setup "+str(key1))
    i+=1
ax1.set_xlabel("Overvoltage / V")
ax2 = ax1.twinx()

i += 1
for key3, key4 in zip(curdic2, voltdic2):
    ax2.scatter(voltdic2[key4], curdic2[key3], s=4, marker="d", color=colours[i], cmap="Greens", label = "New setup "+str(key3))
    i+=1

""" for name, color in zip(laserIntensity, colours):
    logplot.logScatter("dataCollection/"+today+"/"+name+"_sweep", marker = "d", markerSize=2, color = color, label = name) """

""" voltage = rosc.readOscilloscopeData("03042024/oscTest1", 1)
time = rosc.readOscilloscopeData("03042024/oscTest1", 0)
plt.scatter(time, voltage, s=2, marker="d", color="red", cmap="inferno") """

ax1.legend()
ax2.legend(loc = "upper right")
ax1.set_ylabel("$I$ / $\\mathrm{\\mu}$A") # Check that scaling corresponds to correct unit (1E-6 = uA etc.)
ax2.set_ylabel("$I$ / $\\mathrm{\\mu}$A")
fig.tight_layout()
plt.savefig("./dataCollection/"+fileDateImag+"/Photos/"+name)
plt.show()