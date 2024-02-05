


def printMenu():
    print("1. Start measurement")
    print("2. Set range and time")
    print("3. Quit")




while(True):

    printMenu()
    kysymys = input("Input (as a number): ")

    if kysymys == "1":
        continue

    if kysymys == "2":
        range = input("Set range in mV: ")
        time = input("Set time in ns: ")

    if kysymys == "3":
        break



