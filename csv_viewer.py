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
root.geometry('500x500')

# Add some style
style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview.heading", 
    background = "silver",
    foreground = "black",
)

# Change selected colr
style.map('Treeview', background=[('selected', 'red')]) 

my_tree = ttk.Treeview(root)

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

my_tree.pack(pady=20)

tk_sum_rows = Label(root, text=f"Number of rows: {sum_rows}", fg="black").pack()
tk_sum_cols = Label(root, text=f"Number of col: {sum_cols}", fg="black").pack()

root.mainloop()



# usefull Links
# https://stackoverflow.com/questions/30614279/python-tkinter-tree-get-selected-item-values/30615520