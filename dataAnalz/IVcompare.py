import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from sympy import Symbol
import logScatter as logplot
import readOscilloscopeData as rosc


#Write all different laserIntensities to list and same amount of colors for plotting. 'today' needs to be changed (different file locations for each day)

 
laserIntensity = ["100uA", "200uA","500uA", "1mA"]



colours = ["indigo","blue","lightseagreen","green","yellowgreen","gold", "darkorange", "red"]
colours1 = [cm.inferno(i) for i in np.linspace(0, 0.5, 6)]
colours2 = [cm.inferno(i) for i in np.linspace(0.5, 1, 6)]

#CHANGE PATH NAME BY CHANGING DATE
fileDate1 = "16042024"
bdvoltage1 = 21
fileDate2 = "19042024"
bdvoltage2 = 21

# Image save settings
fileDateImag = "19042024"
name = "IVcompare3_8kOhm"


def bdvoltageIndex(fileDate, bdvolt):
    data = [round(point,1) for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate+"/{0}_sweep".format(laserIntensity[0]), 0)]
    return data.index(bdvolt)

print(bdvoltageIndex(fileDate1, bdvoltage1))


#CREATES dICTIONARY WITH KEY - VOLTAGE LIST
voltdic1 = {}
for amps in laserIntensity:
    voltdic1["LED {0}".format(amps)] = [point-bdvoltage1 for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate1+"/{0}_sweep".format(amps), 0)[bdvoltageIndex(fileDate1, bdvoltage1):bdvoltageIndex(fileDate1, bdvoltage1+2.4)]] #SAVE VOLTAGE LIST IN DICTIONARY

voltdic2 = {}
for amps in laserIntensity:
    voltdic2["LED {0}".format(amps)] = [point - bdvoltage2 for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate2+"/{0}_sweep".format(amps), 0)[bdvoltageIndex(fileDate2, bdvoltage2):bdvoltageIndex(fileDate2, bdvoltage2+2.4)]] #SAVE VOLTAGE LIST IN DICTIONARY


#CREATES DICTIONARY WITH KEY - CURRENT LIST.
curdic1 = {}
for amps in laserIntensity:
    curdic1["LED {0}".format(amps)] = [1E6 * point for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate1+"/{0}_sweep".format(amps), 1)[bdvoltageIndex(fileDate1, bdvoltage1):bdvoltageIndex(fileDate1, bdvoltage1+2.4)]] #SAVE CURRENT LIST IN DICTIONARY
curdic2 = {}
for amps in laserIntensity:
    curdic2["LED {0}".format(amps)] = [1E6 * point for point in rsf.readSourceMeterDataFine("dataCollection/"+fileDate2+"/{0}_sweep".format(amps), 1)[bdvoltageIndex(fileDate2, bdvoltage2):bdvoltageIndex(fileDate2, bdvoltage2+2.4)]]



fig, ax1 = plt.subplots()
# Plots all IV-curves to same image
i = 0
for key1, key2 in zip(curdic1, voltdic1):
    ax1.scatter(voltdic1[key2], curdic1[key1], s=2, marker="d", color=colours1[i], cmap="inferno", label = "3.81 kOhm first"+str(key1))
    i+=1
ax1.set_xlabel("Overvoltage / V")
ax2 = ax1.twinx()

i = 0
for key3, key4 in zip(curdic2, voltdic2):
    ax2.scatter(voltdic2[key4], curdic2[key3], s=2, marker="d", color=colours2[i], cmap="Greens", label = "3.810 kOhm second"+str(key3))
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