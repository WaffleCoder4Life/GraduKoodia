import lnDerivativeScatter as lds
import matplotlib.pyplot as plt

plot = lds.lnDerivativeScatter("./dataCollection/15032024/1mA_sweep", markerSize=4, marker=".", color="mediumorchid")
plt.ylim(-100, 100)
plt.show()