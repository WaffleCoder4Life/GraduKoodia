import pyvisa as visa
from tkinter import Tk
from tkinter.ttk import *
from tkinter import simpledialog
from PIL import Image, ImageTk

class GUI:
    def __init__(self, master) -> None:
        self.style = Style()
        self.style.configure(style='my.TButton', font=('Helvetica', 15))
        self.master = master
        self.instr = None
        self.isOn = None
        self.on = None
        self.off = None
        self.master.title("Keithley 220 Current Source")

        self.canvas = Frame(self.master, padding='1i')
        self.canvas.grid()

        
        self.conBut = Button(self.canvas, text="Connect", command=self.connect, style='my.TButton')
        self.conBut.grid(column=0, row=0)

        self.destruction = Button(self.canvas, text="Quit", command=self.master.destroy, style='my.TButton')
        self.destruction.grid(column=0, row=1)
        
    
    def secondPage(self):
        style = Style()
        style.configure(style='my.TButton', font=('Helvetica', 15))
        onImage = Image.open("./AppsNshit/on.png")
        onIm = onImage.resize((50, 50))
        self.on = ImageTk.PhotoImage(onIm)
        offImage = Image.open("./AppsNshit/off.png")
        offIm = offImage.resize((50, 50))
        self.off = ImageTk.PhotoImage(offIm)

        self.master.destroy()

        self.master = Tk()
        self.canvas = Frame(self.master, padding='1i')
        self.canvas.grid()

        self.vLimBut = Button(self.canvas, text="Set voltage limit", command=self.setVoltageLimit, style='my.TButton')
        self.vLimBut.grid(column=0, row=1)

        self.currBut = Button(self.canvas, text="Set current", command=self.setCurrent, style='my.TButton')
        self.currBut.grid(column=0, row=2)

        #Label(self.canvas, text="Don't use this :)").grid(column=1, row=3)
        #self.rangBut = Button(self.canvas, text="Set measurement range", command=self.setMeasRange).grid(column=0, row=3)

        #self.light = Label(self.canvas, image=self.off)
        #if self.isOn is None:
        #    self.instr.write("F0X")
        #    self.light.config(image = self.off)
        #    self.isOn = False
        #self.light.grid(column=0, row=5)
        
        self.onOffBut = Button(self.canvas, text="Output On/Off", command=self.onOff, style='my.TButton')
        self.onOffBut.grid(column=0, row=4)

        self.destruction = Button(self.canvas, text="Quit", command=quit, style='my.TButton')
        self.destruction.grid(column=0, row=6)

        
        


    def quit(self):
        self.instr.close()
        self.master.destroy()
    
    def onOff(self):
        if self.isOn:
            self.instr.write("F0X")
            #self.light.config(image = self.off)
            self.isOn = False
        else:
            self.instr.write("F1X")
            #self.light.config(image = self.on)
            self.isOn = True

    def setVoltageLimit(self):
        """Sets voltage limit"""
        vLim = simpledialog.askfloat(title="Voltage limit", prompt="Enter voltage limit")
        self.instr.write(f"V{vLim}X")
    
    def setCurrent(self):
        """Sets current"""
        curr = simpledialog.askfloat(title="Current", prompt="Enter current")
        self.instr.write("R0X")
        self.instr.write(f"I{curr}X")
    
    def setMeasRange(self):
        """Sets measurement range"""

        coolDict = {
            "Auto": "R0X",
            "1 nA": "R1X",
            "10 nA": "R2X",
            "100 nA": "R3X",
            "1 uA": "R4X",
            "10 uA": "R5X",
            "100 uA": "R6X",
            "1 mA": "R7X",
            "10 mA": "R8X",
            "100 mA": "R9X"
        }

        window = Tk()
        window.title("Set measurement range")

        def rang(self, window, rang: str):
            self.instr.write(coolDict[rang])
            window.destroy()

        
        for key in coolDict:
            Button(window, text=key, command=lambda: rang(self, window, key)).pack()
            
    
    def connect(self):
        rm = visa.ResourceManager()
        rList = rm.list_resources()
        #try:
        self.instr = rm.open_resource('GPIB0::12::INSTR')
        self.instr.write("F0X")
        self.secondPage()
        #except Exception as E:
        #    ip = simpledialog.askstring(title="Wrong resource", prompt=str(rList) + "\nWrong resource, type new resource")
        #    self.instr = rm.open_resource(str(ip))

def main():
    root = Tk()
    GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()