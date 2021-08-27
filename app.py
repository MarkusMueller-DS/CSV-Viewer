from tkinter import *
from tkinter import ttk, filedialog
from numpy import index_exp
import pandas as pd
import os
import glob

def browse_button():
    global file_path
    cwd = os.getcwd()
    file_path= filedialog.askopenfilename(initialdir=cwd)
    # read the selected file into a pandas DataFrame
    tree_main.delete(*tree_main.get_children())             # delete previous tree
    tree_stats.delete(*tree_stats.get_children())
    insert_data()
    basic_stats()
    insert_tree_stats()

def insert_data():
    global data
    data = pd.read_csv(file_path)
    columns = data.columns.values
    columns_tupel = tuple(columns)
    # Define Columns
    tree_main['columns'] = columns_tupel
    # Formate Columns
    tree_main.column('#0', width=0, stretch=NO)
    for col in columns:
        tree_main.column(col, anchor=W, width=120)
    # Create Headings
    tree_main.heading('#0', text='')
    for col in columns:
        tree_main.heading(col, text=col, anchor=W)
    # Add Data
    records = data.to_records(index=False)
    result = list(records)
    for counter, row in enumerate(result):
        tree_main.insert(parent='', index='end', iid=str(counter), text='', values=tuple(row))

def basic_stats():
    numCols = data.shape[1]
    numRows = data.shape[0]
    statsContent.config(text=f"Rows: {numRows} / Cols: {numCols}")

def insert_tree_stats():
    tree_stats['columns'] = ('Column', 'Data Type')
    tree_stats.column('#0', width=0, stretch=NO)
    tree_stats.column('Column',anchor=W, width=50)
    tree_stats.column('Data Type',anchor=W, width=50)
    tree_stats.heading('#0', text='')
    tree_stats.heading('Column',text='Column', anchor=W)
    tree_stats.heading('Data Type',text='Data Type', anchor=W)
    df_types = pd.DataFrame(data.dtypes)
    df_records = df_types.to_records()
    for counter, row in enumerate(list(df_records)):
        tree_stats.insert(parent='', index='end', iid=str(counter), text='', values=tuple(row))

def select_item(a):
    global index
    index = tree_main.selection()[0]
    #print(data.iloc[[index]])
    # insert data into tree_focus
    tree_focus.column('#0', width=0, stretch=NO)
    tree_focus.column('Column',anchor=W, width=30)
    tree_focus.column('Content',anchor=W, width=120)
    tree_focus.heading('#0', text='')
    tree_focus.heading('Column',text='Column', anchor=W)
    tree_focus.heading('Content',text='Content', anchor=W)



## ININT GUI
root = Tk()
root.title("CSV Viewer")

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)

## STYLING
style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview.heading", 
    background = "silver",
    foreground = "black",
)
style.map('Treeview', background=[('selected', 'red')]) 

## WIDGETS
# Open Button
openButton = Button(root, text="Open File...", fg="black", command=browse_button)
# Statistics of the CSV-File
statsFrame = Frame(root)
statsHeader = Label(statsFrame, text="Basic stats of file", fg="black")
statsContent = Label(statsFrame, fg="black")
# TreeView Stats
tree_stats = ttk.Treeview(statsFrame)

# TreeView Main
tree_frame = Frame(root)
tree_scroll = Scrollbar(tree_frame)
tree_main = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree_main.yview)

# TreeView Focus
tree_focus = ttk.Treeview(root)

# add widgets
openButton.grid(column=0, row=0, sticky="N")
tree_frame.grid(column=1, row=0, sticky="NS")
tree_main.grid(column=0, row=0)
tree_scroll.grid(column=1, row=0, sticky="NS")
statsFrame.grid(column=0, row=1)
statsHeader.grid(column=0, row=0, sticky="N")
statsContent.grid(column=0, row=1, sticky="NW")
tree_stats.grid(column=0, row=2, sticky="NW")
tree_focus.grid(column=1, row=1)


## BINDINGS
tree_main.bind('<ButtonRelease-1>', select_item)

root.mainloop()