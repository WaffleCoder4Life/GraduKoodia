import readData as rd
import matplotlib.pyplot as plt
import numpy as np


voltageStr = rd.readData("./dataCollection/test1_1_3_24",0)
currentStr = rd.readData("./dataCollection/test1_1_3_24",1)

voltage = [float(volt) for volt in voltageStr]
current = [float(cur) for cur in currentStr]

voltage2 = [float(volt) for volt in rd.readData("./dataCollection/test2_1_3_24",0)]
current2 = [float(curr) for curr in rd.readData("./dataCollection/test2_1_3_24",1)]


#Tää riittää kun fixas floatiks suoraan readDatan
current3 = rd.readData("./dataCollection/test3_1_3_24", 1)

currAvag = [float((cur1+cur2)/2) for (cur1,cur2) in zip(current,current2)]


""" i = 0
while i < len(current):
    print("U: " + voltage[i] + ", I: " + current[i])
    i+=1 """

fig, ax = plt.subplots()
ax.scatter(voltage, current, s=2, c="blue")
ax.scatter(voltage2, current2, s=2, c="red")
ax.scatter(voltage, current3, s=2, c="yellow")


ax.set(xlim=(voltage[0], voltage[-1]), ylim=(min(current), current[-1]))


plt.show()


