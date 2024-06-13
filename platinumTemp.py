from sympy.solvers import solve
from sympy import Symbol
import scipy.optimize
import matplotlib.pyplot as plt
import numpy as np




""" temperatures = []
resistances = []
with open("./pt1kcalibration.txt", "r") as file:
    for row in file:
        entries = row.strip().split(" ")
        temperatures.append(float(entries[3]))
        resistances.append(float(entries[6]))
print(temperatures)
print(resistances) """

temp = [400.020277099609, 395.041312255859, 390.038676757812, 385.046361083984, 380.062662353516, 375.019366455078, 370.009592285156, 365.020009765625, 360.011071777344, 355.01404296875, 350.013121337891,345.022237548828, 340.0174609375, 335.014281005859, 330.011430664063, 325.014416503906, 320.010146484375, 315.015357666016, 310.010081787109, 305.011241455078, 300.010617675781, 295.010264892578, 290.005998535156, 285.002987060547, 280.007564697266, 275.006856689453, 270.007131347656, 265.006303710938, 260.004782714844, 255.006472167969, 250.003159790039, 245.004920043945, 240.002873535156, 235.005139160156, 230.004016113281, 225.005120239258, 220.005953369141, 215.006972045898, 210.005311889648, 205.005740966797, 200.006019287109, 195.005389404297, 190.005589599609, 185.003646240234, 180.00678894043, 175.005009155273, 170.016053466797, 165.019517211914, 160.01469543457, 155.012462158203, 150.012211914063, 145.010562133789, 140.008977661133, 135.009842529297, 130.00960144043, 125.00877532959, 120.009407958984,115.008800048828, 110.006312866211, 105.004488220215, 100.00764831543, 95.0074002075195, 90.0065811157227, 85.0080294799805, 80.006530456543, 75.0048837280273, 70.0034399414063, 65.0040237426758, 59.9982441711426, 54.994672088623, 50.0069758605957, 44.9751278686523, 40.0006675720215, 34.9850798034668, 29.9836520385742, 25.0162239074707, 20.0171919250488, 15.0000480651855, 10.0138879013062, 9.00003612518311, 7.99833600997925, 7.00099199295044, 5.99763198852539, 5.00038801193237, 3.99992800712585, 3.00001200675964, 1.99994398117065, 1.99995202064514, 3.00001998901367, 3.99995601654053, 5.00012395858765, 6.0000119972229, 6.9999239730835, 8.00002805709839, 9.00005992889404, 9.99981197357178, 15.000696105957, 20.0007399749756, 25.0039038848877, 30.0015560913086, 34.9997045898438, 40.0001878356934, 45.0002122497559, 50.001203918457, 55.0003565979004, 60.0013008117676, 65.0010125732422, 70.0027389526367, 75.0015753173828, 80.0023678588867, 85.0049362182617, 90.003024597168, 95.0037600708008, 100.004383239746, 105.004236450195, 110.00598815918, 115.005128173828, 120.00525177002, 125.005640563965, 130.005227050781, 135.005676879883, 140.006249389648, 145.006451416016, 150.006470947266, 155.008642578125, 160.006344604492, 165.007913818359, 170.009873046875, 175.004240722656, 180.007522583008, 185.008658447266, 190.009110717773, 195.008764038086, 200.00835144043, 205.008272094727, 210.009236450195, 215.00815246582,220.009072265625, 225.008485107422, 230.010086669922, 235.011936645508, 240.009556274414, 245.00919921875, 250.004583129883, 255.008529052734, 260.010317382813, 265.011108398438, 270.013190917969, 275.008408203125, 280.010557861328, 285.010511474609, 290.011317138672, 295.011721191406, 300.010921630859, 305.012243652344, 310.014978027344, 315.012658691406, 320.01794921875, 325.018171386719, 330.014097900391, 335.015446777344, 340.015617675781, 345.007629394531, 350.016052246094, 355.014714355469, 360.019805908203, 365.018857421875, 370.021993408203, 375.021634521484, 380.025277099609, 385.020765380859, 390.016727294922, 395.011662597656, 400.018210449219]
res = [1481.27724121094, 1462.59717773438, 1443.92951660156, 1425.18305664063, 1406.26022460938, 1387.26171386719, 1368.15971191406, 1349.61813476563, 1330.63189941406, 1311.70220703125, 1292.9644140625, 1273.78549804688, 1254.6583984375, 1235.95573730469, 1216.75053710938, 1197.47311523438, 1178.43755371094, 1159.59760253906, 1140.06073242187, 1120.85457519531, 1101.6659765625, 1082.47299316406, 1062.8390625,1043.41869628906, 1024.03907958984, 1004.32620117188, 984.852407226562, 965.52443359375, 945.833781738281, 926.020510253906, 906.463752441406, 886.815046386719, 866.969948730469, 847.272319335937, 827.52744140625, 807.648049316406, 787.850871582031, 767.782736816406, 747.8809765625, 727.807648925781, 707.833828125, 687.689306640625, 667.515983886719, 647.319443359375, 627.101870117187, 606.812819824219, 586.500930175781, 566.189267578125, 545.768234863281, 525.112788085938, 504.469439697266, 483.863479003906, 463.123238525391, 442.353820800781, 421.455258789063, 400.549125976562, 379.425571289062, 358.167462158203, 336.989926757813, 315.712387695312, 294.389097900391, 272.913718261719, 251.394663696289, 229.946502075195, 208.533012084961, 187.060284423828, 165.764436645508, 144.744315795898, 124.110209960938, 104.23236541748, 85.2372131347656, 67.5636004638672, 51.761124420166, 37.9707052612305, 27.1354758453369, 19.1682431030273, 13.9293816375732, 11.0135137176514, 9.75444835662842, 9.63499584197998, 9.54901790618896, 9.49821887969971, 9.45538570404053, 9.41879375457764, 9.405149269104, 9.39461929321289, 9.39425392150879, 9.39236778259277, 9.39666889190674, 9.40825954437256, 9.41748615264893, 9.4632576370, 9.48680862426758, 9.5491198348999, 9.64172470092773, 9.75095600128174, 11.0118360900879, 13.9514977645874, 19.1842777252197, 27.3050124359131, 38.2111366271973, 51.7647532653809, 67.5719604492188,85.1590969848633, 104.088715515137, 123.981336669922, 144.429897460938, 165.422544555664, 186.723554077148, 208.11637878418, 229.504206542969, 250.812660522461, 272.189473876953, 293.636119384766, 314.892947998047, 336.080421142578, 357.22451171875, 378.249567871094, 399.247857666016, 420.184660644531, 440.968983154297, 461.721507568359, 482.318911132813, 503.036134033203, 523.520600585937, 543.961638183594, 564.465837402344, 584.698620605469, 604.905698242188, 625.113686523438, 645.443696289062, 665.589904785156, 685.645788574219, 705.573979492188, 725.674450683594, 745.580576171875, 765.621003417969, 785.484453125, 805.337331542969, 825.221000976563, 845.026875, 864.555400390625, 884.364809570312, 904.008530273437, 923.882270507812, 943.034323730469, 962.915078125, 982.569084472656, 1001.85396484375, 1021.40110839844, 1040.84533691406, 1060.33766601563, 1079.97627929688, 1099.11645507813, 1118.17407226563, 1137.66942382813, 1157.06244628906, 1175.97073242188, 1195.25087402344, 1214.21754882813, 1233.38984863281, 1252.33526367188, 1271.32970703125, 1290.37221191406, 1309.2846484375, 1328.31673828125, 1347.25217773438, 1366.47543457031, 1385.23615722656, 1404.12802246094, 1423.16200195312, 1442.07961914063, 1460.80369140625, 1479.71447265625]


def line(x,a,b):
    return a*x + b

lineParams = scipy.optimize.curve_fit(line, xdata = temp[:71], ydata = res[:71])

aa = lineParams[0][0]
bb = lineParams[0][1]

def lineRev(y, a, b):
    return (y-b)/a

while True:
    comand = input("Select number:\n1. Ohm to Kelvin\n2. Kelvin to Ohm\n3. Quit\n")
    if comand == "1":
        while True:
            res = input("Give resistance (Q - go back to main menu):\n")
            if res == "Q":
                break
            else:
                try:
                    res = float(res)
                    temp = round(lineRev(res, aa, bb),3)
                    print("Temperature is "+str(temp)+" K\n")
                except ValueError as E:
                    print(E)
                    print("Use floats plz :(")
    if comand == "2":
        while True:
            temp = input("Give temperature (Q - go back to main menu):\n")
            if temp == "Q":
                break
            else:
                try:
                    temp = float(temp)
                    res = round(line(temp, aa, bb),3)
                    print("Resistance is "+str(res)+" Ohm\n")
                except ValueError as E:
                    print(E)
                    print("Use floats plz :(")
                
    if comand == "3":
        break