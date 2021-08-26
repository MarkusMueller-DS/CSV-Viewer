import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import os
import glob

# functions
def browse_button():
    global file_path
    cwd = os.getcwd()
    file_path= filedialog.askopenfilename(initialdir=cwd)
    print(file_path)
    # read the selected file into a pandas DataFrame
    data = pd.read_csv(file_path)
    print(data.shape)


# Creat root
root = tk.Tk()
root.geometry("600x400")

# Grid congig
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=2)

root.rowconfigure(0, weight=2)
root.rowconfigure(1, weight=1)

# Open File Button
openFile = tk.Button(root, text="Open File", fg="black", command=browse_button)
openFile.grid(row=0, column=0, sticky="N")

# Create TeeView Frame
tree_frame = tk.Frame(root)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.grid(column=2, row=0)

# Create TreeView
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
my_tree.grid(column=1, row=0, columnspan=2)

# Configure the scrollbar
tree_scroll.config(command=my_tree.yview)

root.mainloop()