import pyvisa


def generatePulses(instrument, frequency_Hz: float, amplitude_V: float, pulseWidth_s: float) -> str:
    """Generates pulses on KeySight oscilloscope, and returns used settings as a string.\n
    Frequency between 100 mHz and 10 MHz, minimum pulse width between 20 ns."""

    instrument.write("WGEN:FUNCtion PULSe")
    instrument.write("WGEN:FUNCtion:PULSe:WIDTh " + str(pulseWidth_s))
    instrument.write("WGEN:FREQuency " + str(frequency_Hz))
    instrument.write("WGEN:VOLTage:HIGH " + str(amplitude_V))
    instrument.write("WGEN:VOLTage:LOW 0")

    instrument.write("WGEN:OUTPut1 1")

    settings = "Frequency: " + str(frequency_Hz) + " Hz, Amplitude: " + str(amplitude_V) + " V, Pulse width: " + str(pulseWidth_s) + " s"

    return settings