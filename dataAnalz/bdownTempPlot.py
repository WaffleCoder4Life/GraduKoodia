import matplotlib.pyplot as plt



breakDown = [20.62, 20.81, 20.89, 20.91, 21.17, 21.36, 21.56, 24.43]
# Temperature with Pt resistor
temperature = [320, 360, 380, 400, 500, 550, 620, 1080]

plt.scatter(temperature, breakDown, s=10, color="indigo", label = "Breakdown voltages from IV-curves")
plt.xlabel("Temperature / Ohm")
plt.ylabel("Breakdown voltage / V")
plt.legend()
plt.savefig("./DataCollection/BVfunctionOfT")
plt.show()
