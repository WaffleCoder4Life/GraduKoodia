import Keithley.close as kclose
import KeySightConn.close as uclose
import pyvisa as visa

rm = visa.ResourceManager()
list = rm.list_resources()


osc = rm.open_resource(list[0])
sour = rm.open_resource(list[1])


kclose.close(sour)
uclose.close(osc)