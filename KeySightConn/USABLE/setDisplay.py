#Display settings, Channel range 8 div, timebase range 10 div


def setDisplay(instrument, chan: int, voltageRange_V: float, timeRange_us: float, triggerLevel_V: float) -> str:
    """Sets voltage and time ranges, and DC trigger level for KeySight oscilloscope's display, 
    and returns these settings as a string. voltageRange allowed values [8mV - 40V]"""
    instrument.write(":TRIGger:SOURce CHANnel" + str(chan))
    instrument.write(":TRIGger:MODE EDGE") #NEEDS TESTING
    instrument.write(":TRIGger:COUPling DC") #NEEDS TESTING
    instrument.write(":CHANnel" + str(chan) + ":RANGe " + str(voltageRange_V))
    instrument.write(":TIMebase:RANGe " + str(timeRange_us) + "E-6")
    instrument.write(":TRIGger:LEVel " + str(triggerLevel_V))
    instrument.write(":CHANnel" + str(chan) + ":DISPlay 1")

    settings = "Voltage range: " + str(voltageRange_V) + " V, Time range: " + str(timeRange_us) + " us, Trigger level: " + str(triggerLevel_V) + "V"

    return settings