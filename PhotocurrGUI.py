import tkinter as tk
import threading
import time

GUIval = 0
GUItimer = None

def iScreen(Keithley6487):
    polling_rate = None
    device = Keithley6487

    def func():
        # Replace this with your actual function
        global GUIval
        GUIval+=1
        return GUIval

    def fetch_i(device = device):
        global GUIval
        device.write(":FORM:ELEM READ") #IF 'ALL' -> CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE. 'READ,VSO' -> CURRENT, SOURCE VOLTAGE
        device.write(":FORM:DATA ASCii") #CHOOSE DATA FORMAT
        device.write(":INIT") #TRIGGER MEASUREMENT
        device.write(":SENS:DATA?") #ASK FOR DATA
        GUIval = 1
        return GUIval


    def update_text():
        global GUItimer
        global submit_pressed
        if device is None:
            number = func()
        else:
            number = fetch_i()
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, str(number), 'center')
        global GUItimer
        global polling_rate
        if GUItimer is not None:
            GUItimer.cancel()
        if submit_pressed:
            GUItimer = threading.Timer(float(polling_rate), update_text)
            GUItimer.start()

    def submit():
        global submit_pressed
        global polling_rate
        polling_rate = float(polling_rate_entry.get())
        submit_pressed = True
        update_text()

    def resize_text(event):
        # Calculate new font size based on window size
        new_font_size = int((event.height) / 1.6)
        text_box.configure(font=("TkDefaultFont", new_font_size))

    def stop_timer():
        global timer
        if GUItimer is not None:
            GUItimer.cancel()

    def on_exit():
        stop_timer()
        root.destroy()

    root = tk.Tk()
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(1, weight=1)

    polling_rate_entry = tk.Entry(root)
    polling_rate_entry.grid(row=0, column=0)
    polling_rate_entry.insert(0, '1')  # Default polling rate

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=0, column=1)

    stop_button = tk.Button(root, text="Stop", command=stop_timer)
    stop_button.grid(row=0, column=2)

    text_box = tk.Text(root)
    text_box.grid(row=1, column=0, columnspan=2, sticky='nsew')
    text_box.tag_configure('center', justify='center')

    global GUItimer
    GUItimer = None
    submit_pressed = False

    root.bind('<Configure>', resize_text)
    root.protocol("WM_DELETE_WINDOW", on_exit)

    root.mainloop()

if __name__ == "__main__":
    iScreen(None)