import matplotlib.pyplot as plt






# Temperature 3.710 kOhm, LED 5.5 V, 800 ns
meanPhotons1 = [1.3356, 1.9522, 2.6386, 3.2734, 3.8642, 4.7462, 6.0762, 8.2936, 10.9568]
overVoltage1 = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

# Temperature 3.770 kOhm, LED 5V, 800 ns
meanPhotons2 = [0.7032, 0.7394, 0.9822, 1.2442, 1.787, 2.321]
overVoltage2 = [2, 2.5, 3, 3.5, 4, 4.5]

# Temperature 1.85 kOhm, LED 5.5 V, 800 ns
meanPhotons3 = [2.2012, 2.6442, 3.299, 3.9522, 4.9606, 6.7454, 8.929, 11.2924]
overVoltage3 = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.0]

relativePDE1 = [point / meanPhotons1[1] for point in meanPhotons1]
relativePDE2 = [point / meanPhotons2[0] for point in meanPhotons2]
relativePDE3 = [point / meanPhotons3[0] for point in meanPhotons3]


plt.scatter(overVoltage3, relativePDE3, marker = "d", color = "blue", label = "1.85 kOhm, LED 5.5 V")
plt.scatter(overVoltage1, relativePDE1, marker = "s", color = "fuchsia", label = "3.71 kOhm, LED 5.5 V")
plt.scatter(1.5, 1, s = 90, facecolors = "none", edgecolors = "black", label = "Reference point")
plt.xlabel("Overvoltage / V")
plt.ylabel("Relative PDE")
plt.legend()
plt.savefig("./DataCollection/relativePDEtempCompare.png")
plt.show()