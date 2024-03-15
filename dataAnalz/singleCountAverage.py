import numpy as np
import averagefrfr as av
import readOscilloscopeData as rod
import matplotlib.pyplot as plt

#SAVE DATASETS FROM 10 DARKCOUNTS TO A LIST
i = 1
datasets = []
while i <= 10:
    temp = rod.readOscilloscopeData("15032024/darkcount{0}".format(str(i)), 1)
    datasets.append(temp)
    plt.scatter(rod.readOscilloscopeData("15032024/darkcount{0}".format(str(i)), 0), temp, s=2)
    i += 1



#AVERAGE OF BACKGROUND FROM ALL DATASETS FROM START TO PULSE
#AVERAGE OF THE AVERAGE: TO BE SUBTRACTED FROM PULSE DATA TO COMPENSATE BG
BGaverage = av.averageData(10, [dataset[:95] for dataset in datasets]) # 

BGcorrectiontemp = 0
for point in BGaverage:
    BGcorrectiontemp = BGcorrectiontemp + point
BGcorrection = BGcorrectiontemp / len(BGaverage)
print(BGcorrection)

#AVERAGE PULSE DATA FROM ALL DATASETS AND SUBTRACT BG CORRECTION
pulseaveragetemp = av.averageData(10, [dataset[95:160] for dataset in datasets])
pulseaverage = [point - BGcorrection for point in pulseaveragetemp]


time = rod.readOscilloscopeData("15032024/darkcount1", 0)[:65]

#print(time[95])
#print(time[160])

#plt.scatter(time, pulseaveragetemp, s=4, c="black")
plt.show()