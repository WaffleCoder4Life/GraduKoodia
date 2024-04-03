import pyvisa as visa
import KeySightConn.generatePulses as gen
import KeySightConn.saveData as save
import KeySightConn.setDisplay as set
import keyboard
import time
import KeySightConn.saveImage as si


print("Test connection")
rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
#sour = rm.open_resource(list[1])
#osc.write("*IDN?")
#print(osc.read())


#set.setDisplay(osc, 1, 0.2, 2, 0.03)
#set.setDisplay(osc, 2, 20, 0.01, 1)
#set.setDisplay(osc, 2, 20, 1000000, 1)

#osc.write(":RUN")

save.saveData(osc, "oscTest1", "Peak finder testing", False)


#gen.generatePulses(osc, 5, 7, 0.000000100)
#gen.generatePulses(osc, 0.5, 5, 1)


