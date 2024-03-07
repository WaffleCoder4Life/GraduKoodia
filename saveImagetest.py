import pyvisa as visa
from Keithley import setVoltage as sv
from KeySightConn import setDisplay as set


rm = visa.ResourceManager()
list = rm.list_resources()
print(list)

osc = rm.open_resource(list[0])
sour = rm.open_resource(list[2])
osc.write("*IDN?")
print(osc.read())




set.setDisplay(osc, 1, 0.2, 2, 0.03)
set.setDisplay(osc, 2, 20, 1, 1)

osc.write(":RUN")

#sv.setVoltage(sour, 1000, 27, 0.0150)


osc.write(":HARDcopy:INKSaver OFF")
sDisplay = osc.query_binary_values(":DISPlay:DATA? PNG", datatype = "B", header_fmt = "ieee", container = bytes)
#sDisplay = osc.read()
# Save display data values to file.
f = open("./Photos/testikuva1.png", "wb")
f.write(sDisplay)
f.close()
print("Screen image written to screen_image.png.")

#osc.write(":SAVE:FILename './'")
#osc.write(":SAVE:IMAGe:FORMat PNG")
#osc.write(":SAVE:IMAGe:STARt 'c:./kuva1.png'")
#osc.write(":SAVE:FILename?")
#print(osc.read())