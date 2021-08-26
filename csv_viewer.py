from tkinter import *
from tkinter import ttk
import pandas as pd

data = pd.read_csv('test_data/tweets_22.08.2021_tweepy.csv')
columns = data.columns.values

# basic statistics about the csv
sum_rows = data.shape[0]
sum_cols = data.shape[1]

# convert columns-list to a tuple
columns_tupel = tuple(columns)

root = Tk()
root.title('CSV-Viewer')
root.geometry('600x400')

# Add some style
style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview.heading", 
    background = "silver",
    foreground = "black",
)

# Function to get the values of a row
def selectItem(a):
    #curItem = my_tree.focus()
    #lst = my_tree.item(curItem)['values']
    #length = len(my_tree.item(curItem))
    #for item in lst:
    #    Label(root, text=item, fg="black").pack()
    global index # set to global to use it in other functions
    index = my_tree.selection()[0]
    #print(index)
    printIndex()


def printIndex():
    print(index)

# Change selected cols
style.map('Treeview', background=[('selected', 'red')]) 

# Create TreeView Frame
tree_frame = Frame(root)
tree_frame.pack(pady=20)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create TreeView
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
my_tree.pack()

# Configure the scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Columns
my_tree['columns'] = columns_tupel

# Formate Columns
my_tree.column('#0', width=0, stretch=NO)
for col in columns:
    my_tree.column(col, anchor=W, width=120)

# Create Headings
my_tree.heading('#0', text='')
for col in columns:
    my_tree.heading(col, text=col, anchor=W)

# Add Data
records = data.to_records(index=False)
result = list(records)

for counter, row in enumerate(result):
    my_tree.insert(parent='', index='end', iid=str(counter), text='', values=tuple(row))

my_tree.bind('<ButtonRelease-1>', selectItem)

tk_sum_rows = Label(root, text=f"Number of rows: {sum_rows}", fg="black").pack(side=LEFT)
tk_sum_cols = Label(root, text=f"Number of col: {sum_cols}", fg="black").pack(side=LEFT)

# add every colum as a lable to the gui
for col in columns:
    Label(root, text=col, fg='black').pack()


root.mainloop()