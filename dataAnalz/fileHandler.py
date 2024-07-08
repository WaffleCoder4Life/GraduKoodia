import os
import tkinter as tk
import json
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import os
from tkinter import ttk
from typing import Tuple
from tkinter import *
from datetime import date
import matplotlib.pyplot as plt


def ChooseFolder(initdir = "..", title = ""):
    # Initialise tkinter window
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    
    # Prompt to choose the files to process.
    datafolder = filedialog.askdirectory(initialdir = initdir, title = title, parent = root)
    
    root.destroy()
    return datafolder

def nameIsTaken(path, name):
    if os.path.isfile(path+"/"+name):
        print("Filename taken (csv)")
        return True
    else:
        return False
    
def inputText(title):
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.tk.eval(f'tk::PlaceWindow {root._w} center')
    root.withdraw()
    return simpledialog.askstring(title, f"Enter {title} below:")

def ChooseFiles(initdir = ".."):
    # Initialise tkinter window
    root = tk.Tk()
    root.wm_attributes('-topmost', 1) 
    root.withdraw()
    
    # Prompt to choose the files to process.
    files = filedialog.askopenfilenames(initialdir = initdir, parent = root)
    # Return filenames as simple list
    return files



def ChooseFileMultiple(initdir = "..", text = 'Choose files', filetypes = [('csv files', '*.csv')]) -> Tuple[list, str]:
    """Choose a file and ask wether to add more files. Returns tuple[list, string] where string = 'yes' or 'no'."""
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.tk.eval(f'tk::PlaceWindow {root._w} center')
    root.withdraw()
    files = filedialog.askopenfilenames(initialdir = initdir,title=text, filetypes = filetypes)
    msgbox = messagebox.askquestion ('Add files','add extra files',icon = 'warning')
    return list(files), msgbox

def ChooseFilesDifferentFolders(initdir = "..", text = "Choose files", filetypes = [('csv files', '*.csv')]):
    files, msbox = ChooseFileMultiple(initdir=initdir, text = text, filetypes = filetypes)
    allFiles = files
    while msbox == "yes":
        files2, msbox = ChooseFileMultiple(initdir = initdir, text = text, filetypes = filetypes)
        for file in files2:
            allFiles.append(file)
    return allFiles

class ButtonWindow:
    def __init__(self, title, text1, text2):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.wm_attributes('-topmost', 1)
        self.root.eval('tk::PlaceWindow . center')
        self.button_pressed = None
        
        label = Label(self.root, text = title)
        button1 = tk.Button(self.root, text=text1, command=lambda: self.on_button_press(1))
        button2 = tk.Button(self.root, text=text2, command=lambda: self.on_button_press(2))
        
        label.pack(pady=10)
        button1.pack(pady=10)
        button2.pack(pady=10)

    def on_button_press(self, button_id):
        self.button_pressed = button_id
        self.root.quit()

    def run(self):
        self.root.mainloop()
        self.root.destroy()
        return self.button_pressed


def returnToday():
    today = date.today()
    day = "{:02d}".format(today.day)
    month = "{:02d}".format(today.month)
    return day + month + str(today.year)


def messageWindowSelectOptions(title, message, button1, button2):
    # Initialise tkinter window
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.eval('tk::PlaceWindow . center')
    root.withdraw()
    def closeReturnValue1():
        root.destroy()
        return 1
    def closeReturnValue2():
        root.destroy()
        return 2
    win = Toplevel(root)
    win.title(title)
    Label(win, text=message).pack()
    Button(win, text=button1, command=closeReturnValue1()).pack()
    Button(win, text=button2, command=closeReturnValue2()).pack()
    root.mainloop()


def ChooseSingleFile(initdir = ".."):
    # Initialise tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Prompt to choose the files to process.
    file = filedialog.askopenfilename(initialdir = initdir)
    
    # Return filenames as simple list
    return file


def CheckFolder(folderpath):
    # Check whether folder exists, create it if not
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
        print("Folder created: " + folderpath)

def WriteJson(filepath, dict):
    # Writes a dictionary to a json file
    folderpath = filepath[:filepath.rfind("/")]
    CheckFolder(folderpath)
    
    with open(filepath, "w") as json_file:  
        json.dump(dict, json_file, indent = 4, sort_keys = True)
    
    return None

def ReadJson(filepath):
    # Reads a json file, returns the dictionary form of the file
    with open(filepath, "r") as json_file:
        dict = json.load(json_file)
    
    return dict

def ReadTXT(filepath):
    # Reads a txt into a string
    f = open(filepath,"r")
    string = f.read()
    return string
    

def WriteDat(filepath = None, string_to_write = "", writemode = "w"):
    # Writes a dictionary to a json file
    if filepath == None:
        filepath = filedialog.asksaveasfile(mode='w', defaultextension=".dat")
    folderpath = filepath[:filepath.rfind("/")]
    CheckFolder(folderpath)
    
    with open(filepath, writemode) as dat_file:  
        dat_file.write(string_to_write)
    
    return filepath

# Chat GPT generated stuff to pick a point
class PointPicker:
    def __init__(self, x, y, selection):
        self.x = x
        self.y = y
        self.selected_index = None
        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter(x, y)
        self.ax.set_title(selection)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        
        # Calculate the distances between the click and all points
        distances = np.hypot(self.x - event.xdata, self.y - event.ydata)
        self.selected_index = np.argmin(distances)
        
        print(f'Selected point index: {self.selected_index}')
        plt.close(self.fig)  # Close the plot window

def pick_point_from_scatter(x, y, title):
    picker = PointPicker(x, y, title)
    return picker.selected_index

