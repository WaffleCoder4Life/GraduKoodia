import matplotlib.pyplot as plt



breakDown = [21, 21, 21, 20.85, 20.6, 20.64, 20.7, 20.81, 20.89, 20.91, 21.17, 21.36, 21.56, 24.47]
# Temperature with Pt resistor
# temperature = [320, 360, 380, 400, 500, 550, 620, 1080]
temperature = [0.18, 1, 7.07, 15.2, 34.5, 45.7, 83.9, 115.4, 120.1, 124.9, 148.9, 161.1, 178.3, 294.4]

plt.scatter(temperature, breakDown, marker="x", s=10, color="indigo", label = "Breakdown voltages from IV-curves")
plt.xlabel("Temperature / K")
plt.ylabel("Breakdown voltage / V")
plt.legend()
plt.savefig("./DataCollection/BVfunctionOfT")
plt.show()
