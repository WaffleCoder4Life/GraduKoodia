import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from sympy import Symbol
import logScatter as logplot

#Write all different laserIntensities to list and same amount of colors for plotting. 'today' needs to be changed (different file locations for each day)

 
laserIntensity = ["25uA", "50uA", "100uA", "200uA","500uA", "1mA", "5mA"]



colours = ["indigo","blue","lightseagreen","green","yellowgreen","gold", "darkorange", "red"]
colours1 = [cm.inferno(i) for i in np.linspace(0, 1, 10)]

#CHANGE PATH NAME BY CHANGING DATE
today = "15032024"

""" #CREATES dICTIONARY WITH KEY - VOLTAGE LIST
voltdic = {}
for amps in laserIntensity:
    voltdic["LED {0}".format(amps)] = [rsf.readSourceMeterDataFine("dataCollection/"+today+"/{0}_sweep".format(amps), 0)] #SAVE VOLTAGE LIST IN DICTIONARY


#CREATES DICTIONARY WITH KEY - CURRENT LIST.
curdic = {}
for amps in laserIntensity:
    curdic["LED {0}".format(amps)] = [1E6 * point for point in rsf.readSourceMeterDataFine("dataCollection/"+today+"/{0}_sweep".format(amps), 1)] #SAVE CURRENT LIST IN DICTIONARY


 """


""" i = 0
for key1, key2 in zip(curdic, voltdic):
    plt.scatter(voltdic[key2], curdic[key1], s=2, marker="d", color=colours1[i], cmap="inferno", label = str(key1))
    i+=1 """

for name, color in zip(laserIntensity, colours):
    logplot.logScatter("dataCollection/"+today+"/"+name+"_sweep", marker = "d", markerSize=2, color = color, label = name)


plt.xlabel("$U$ / V")
plt.ylabel("$I$ / $\\mathrm{\\mu}$A")
plt.legend()
plt.ylim((1E-4,10))
plt.tight_layout()
plt.savefig("./dataCollection/"+today+"/Photos/IVcurvesLog")
plt.show()