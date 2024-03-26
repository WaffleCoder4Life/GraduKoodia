import lnDerivativeScatter as lds
import matplotlib.pyplot as plt

plot = lds.lnDerivativeScatter("./dataCollection/15032024/10mA_sweep", markerSize=4, marker=".", color="mediumorchid")
#plt.ylim(-10, 200)
plt.show()