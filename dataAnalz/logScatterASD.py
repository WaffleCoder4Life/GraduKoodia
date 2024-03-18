import readSourceMeterDataFine as rsf
import matplotlib.pyplot as plt
import numpy as np

derivative = 0

voltage = rsf.readSourceMeterDataFine("dataCollection/13032024_FINE_sweep_up_1mALED", 0)

laserIntensity = ["1mA", "5mA", "10mA"]
colours = ["gold", "darkorange", "red"]

d = {}
if derivative == 0:
    for amps in laserIntensity:
        d["LED {0}".format(amps)] = [1E6 * point for point in rsf.readSourceMeterDataFine("dataCollection/13032024_FINE_sweep_up_{0}LED".format(amps), 1)]
elif derivative == 1:
    for amps in laserIntensity:
        read1 = rsf.readSourceMeterDataFine("dataCollection/13032024_FINE_sweep_up_{0}LED".format(amps), 1)
        read = []
        for value in read1:
            val = np.log(value)
            read.append(val)
        asd = []
        volt2 = []
        i = 0
        while i < len(read)-1:
            volt = (voltage[i+1] + voltage[i])/2
            qwe = (read[i+1] - read[i])/((voltage[i+1]-voltage[i]))
            asd.append(qwe)
            volt2.append(volt)
            i += 1
        d["LED {0}".format(amps)] = asd




if derivative == 0:
    i = 0
    for key in d:
        plt.scatter(voltage, d[key], s=2, c=colours[i], marker="d", label = str(key))
        i+=1
    plt.xlabel("$U$ / V")
    plt.ylabel("$I$ / $\\mathrm{\\mu}$A")
    plt.yscale("log")
    plt.ylim(1E-5,)
    plt.legend()
    plt.tight_layout()
    plt.savefig("./dataCollection/Photos/130324IVcurvesFINElog2")
    
else:
    i = 0
    for key in d:
        plt.scatter(volt2, d[key], s=2, c=colours[i], marker="d", label = str(key))
        i+=1
    plt.xlabel("$U$ / V")
    plt.ylabel("$d/dV\\ \\mathrm{\ln}I$")
    plt.legend()
    plt.tight_layout()
    plt.savefig("./dataCollection/Photos/130324IVcurvesFINEderiv")
    #plt.ylim(-1000, 1000)

plt.show()