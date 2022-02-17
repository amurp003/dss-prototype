# imports
import tkinter as tk
from tkinter import ttk

# create instance
win = tk.Tk()

# add a title
win.title("Python GUI")

# adding a label
ttk.Label(win, text="A Label").grid(column=0, row=0)

# disable resizing the GUI (x,y)
#win.resizable(False, False)

# start GUI
win.mainloop()

