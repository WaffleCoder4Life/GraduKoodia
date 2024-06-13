import os
import tkinter as tk
import json
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import os



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
    root.destroy()
    # Return filenames as simple list
    return files

def ChooseFileMultiple(initdir = ".."):
    files = tk.filedialog.askopenfilenames(initialdir = initdir,title='Choose files')
    msgbox = tk.messagebox.askquestion ('Add files','add extra files',icon = 'warning')
    return list(files), msgbox

def ChooseFilesDifferentFolders(initdir = ".."):
    files, msbox = ChooseFileMultiple(initdir=initdir)
    allFiles = files
    while msbox == "yes":
        files2, msbox = ChooseFileMultiple(initdir = initdir)
        for file in files2:
            allFiles.append(file)
    return allFiles


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

