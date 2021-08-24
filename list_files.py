import tkinter as tk
import os
import glob
from tkinter.constants import ANCHOR
from tkinter import StringVar, filedialog
from tkinter import ttk
import csv


def showContent(envent):
    x = fr_lbox.curselection()[0]
    file = fr_lbox.get(x)
    with open(file) as file:
        file = file.read()
    text.delete("1.0", tk.END)
    text.insert(tk.END, file)


def browse_button():
    global folder_path
    filename = filedialog.askdirectory()
    folder_path = filename
    print(filename)
    files_list = []
    for name in glob.glob(f"{folder_path}/*.py"):
        files_list.append(name)
    for item in files_list:
        fr_lbox.insert(tk.END, item)


win = tk.Tk()
win.title("file viewer")
win["bg"] = "dark slate blue"
folder_path = StringVar()

win.rowconfigure(0, minsize=800, weight=1)
win.columnconfigure(1, minsize=800, weight=1)

fr_open_files = tk.Frame(win)

fr_open = tk.Button(fr_open_files, text="Open Folder", fg="black", command=browse_button)
fr_lbox = tk.Listbox(fr_open_files)

fr_open.grid(row=0, column=0, sticky="ew", padx=3, pady=3)
fr_lbox.grid(row=1, column=0, sticky="ew", padx=3)

text = tk.Text(win, bg="azure", fg="black")

fr_open_files.grid(row=0, column=0, sticky="ns")
text.grid(row=0, column=1, sticky="nsew")

fr_lbox.bind("<<ListboxSelect>>", showContent)

win.mainloop()