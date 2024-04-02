import lnDerivative as lds
import matplotlib.pyplot as plt

data= lds.lnDerivative("./dataCollection/15032024/1mA_sweep", 10)

plt.scatter(data[0][0], data[0][1], marker=".", s=15, color="mediumorchid")
plt.xlabel("$U$ / V")
plt.ylabel("$\dfrac{\mathrm{d}}{\mathrm{d}U}$ ln$I$")
plt.show()