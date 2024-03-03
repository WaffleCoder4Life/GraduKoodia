import readData as rd
import matplotlib.pyplot as plt
import numpy as np


voltageStr = rd.readData("./dataCollection/test1_1_3_24",0)
currentStr = rd.readData("./dataCollection/test1_1_3_24",1)

voltage = [float(volt) for volt in voltageStr]
current = [float(cur) for cur in currentStr]

""" i = 0
while i < len(current):
    print("U: " + voltage[i] + ", I: " + current[i])
    i+=1 """

fig, ax = plt.subplots()
ax.scatter(voltage,current, s=2, c="blue")

ax.set(xlim=(voltage[0], voltage[-1]), ylim=(min(current), current[-1]))


plt.show()


