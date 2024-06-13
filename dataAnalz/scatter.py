import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from sympy import Symbol
import logScatter as logplot
import readOscilloscopeData as rosc

#Write all different laserIntensities to list and same amount of colors for plotting. 'today' needs to be changed (different file locations for each day)

 
laserIntensity = ["100uA", "200uA","400uA"]



colours = ["indigo","blue","lightseagreen","green","yellowgreen","gold", "darkorange", "red"]
colours1 = [cm.inferno(i) for i in np.linspace(0, 1, 6)]

#CHANGE PATH NAME BY CHANGING DATE
today = "05062024"

#CREATES dICTIONARY WITH KEY - VOLTAGE LIST
voltdic = {}
for amps in laserIntensity:
    voltdic["LED {0}".format(amps)] = [rsf.readSourceMeterDataFine("dataCollection/"+today+"/UV{0}_roomtemp".format(amps), 0)] #SAVE VOLTAGE LIST IN DICTIONARY


#CREATES DICTIONARY WITH KEY - CURRENT LIST.
curdic = {}
for amps in laserIntensity:
    curdic["LED {0}".format(amps)] = [1E6 * point for point in rsf.readSourceMeterDataFine("dataCollection/"+today+"/UV{0}_roomtemp".format(amps), 1)] #SAVE CURRENT LIST IN DICTIONARY




# Plots all IV-curves to same image
i = 0
for key1, key2 in zip(curdic, voltdic):
    plt.scatter(voltdic[key2], curdic[key1], s=2, marker="d", color=colours1[i], cmap="inferno", label = str(key1))
    i+=1

""" for name, color in zip(laserIntensity, colours):
    logplot.logScatter("dataCollection/"+today+"/"+name+"_sweep", marker = "d", markerSize=2, color = color, label = name) """

""" voltage = rosc.readOscilloscopeData("03042024/oscTest1", 1)
time = rosc.readOscilloscopeData("03042024/oscTest1", 0)
plt.scatter(time, voltage, s=2, marker="d", color="red", cmap="inferno") """

plt.xlabel("$U$ / V")
plt.ylabel("$I$ / $\\mathrm{\\mu}$A") # Check that scaling corresponds to correct unit (1E-6 = uA etc.)
plt.legend()
plt.tight_layout()
plt.savefig("./dataCollection/"+today+"/Photos/UVIVcurves")
plt.show()