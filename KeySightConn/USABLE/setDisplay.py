#Display settings, Channel range 8 div, timebase range 10 div


def setDisplay(instrument, voltageRange_V: float, timeRange_us: float, triggerLevel_V: float) -> str:
    """Sets voltage and time ranges, and DC trigger level for KeySight oscilloscope's display, 
    and returns these settings as a string."""
    time = str(timeRange_us)
    volt = str(voltageRange_V)
    instrument.write(":TRIGger1:MODE EDGE") #NEEDS TESTING
    instrument.write(":TRIGger1:COUPling DC") #NEEDS TESTING
    instrument.write(":CHANnel1:RANGe " + volt)
    instrument.write(":TIMebase:RANGe " + time + "E-6")
    instrument.write(":TRIGger1:LEVel " + str(triggerLevel_V))
    instrument.write(":RUN")

    settings = "Voltage range: " + str(voltageRange_V) + " V, Time range: " + str(timeRange_us) + " us, Trigger level: " + str(triggerLevel_V) + "V"

    return settings