import pyvisa
import keyboard


#Laite, pulssin taajuus, pulssin amplitude (vakiona pulssin low=0), pulssin leveys
def generate_pulses(scope, frequency:str, amplitude:str, pulse_width:str):
    # Configure the signal source
    scope.write("WGEN:FREQuency "+str(frequency))
    scope.write("WGEN:VOLTage:HIGH "+str(amplitude))
    scope.write("WGEN:VOLTage:LOW 0")


    scope.write("WGEN:FUNCtion PULSe")
    # Set the pulse parameters
    scope.write("WGEN:FUNCtion:PULSe:WIDTh "+str(pulse_width))

    # Enable the output
    scope.write("WGEN:OUTPut1 1")

    print("Generating pulses...")
    

    """ while True:
        if keyboard.is_pressed('q'):
            scope.write("WGEN:OUTPut1 0")
            print("Pulse generation stopped.")
            break """

   
