import pyvisa
import keyboard


def generate_pulses(scope, frequency, amplitude, pulse_width):
    # Configure the signal source (replace with the correct SCPI command)
    scope.write("WGEN:FREQuency "+str(frequency))
    scope.write("WGEN:VOLTage "+str(amplitude))

    # Set the pulse parameters (replace with the correct SCPI command)
    scope.write("WGEN:FUNCtion:PULSe:WIDTh "+str(pulse_width))

    # Enable the output (replace with the correct SCPI command)
    scope.write("WGEN:OUTPut1 1")

    print("Generating pulses...")
    

    while True:
        if keyboard.is_pressed('q'):
            scope.write("WGEN:OUTPut1 0")
            print("Pulse generation stopped.")
            break

   
