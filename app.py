# CSV-Viewer by Markus Müller

from tkinter import *
from tkinter import ttk, filedialog
from numpy import index_exp
import pandas as pd
import os
import pyperclip3 as pc

# Functions
def main_window():
    # alomost everything gets managed here
    global file_path
    cwd = os.getcwd()
    file_path= filedialog.askopenfilename(initialdir=cwd, filetypes=[("CSV file","*.csv")])
    root.withdraw()
    main_window = Toplevel(root)
    main_window.title("CSV Viewer")
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    main_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def new_file():
        # exit current window and unhide root window to select new file
        main_window.destroy()
        root.deiconify()
    
    def exit():
        main_window.destroy()
        root.destroy()
        
    # menubar
    menubar = Menu(main_window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=new_file)
    filemenu.add_command(label="Exit", command=exit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    ## FRAMES
    # Main Frame where the CSV-Viever is palced
    main_frame = LabelFrame(main_window, text="Main View", fg="black", bd=3, pady=5, padx=5)
    main_frame.pack(fill='both', expand=True, padx=5, pady=5)
    # PLACEHOLDER frmae where text information is placed
    txt_frame = LabelFrame(main_window, text="File Information", fg="black", bd=3, pady=5, padx=5, height=50)
    txt_frame.pack(fill='both', expand=FALSE, padx=5, pady=5)
    # Stats Frame where more Information about the file and row is placed
    stats_frame = LabelFrame(main_window, text="More Information", fg="black",bd=3, pady=5, padx=5)
    stats_frame.pack(fill='both', expand=True, padx=5, pady=5)

    ## READ DATA
    data = pd.read_csv(file_path)

    ### WIDGETS
    ## Main Treeview 
    main_tree = ttk.Treeview(main_frame)
    main_tree.place(rely=0, relx=0, relwidth=1, relheight=1)

    scroll_Y = Scrollbar(main_frame, orient="vertical", command=main_tree.yview)
    scroll_X = Scrollbar(main_frame, orient="horizontal", command=main_tree.xview)
    main_tree.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
    scroll_Y.pack(side=RIGHT, fill=Y)
    scroll_X.pack(side=BOTTOM, fill=X) 

    columns = data.columns.values
    columns_tupel = tuple(columns)
    main_tree['columns'] = columns_tupel
    main_tree.column('#0', width=0, stretch=NO)
    for col in columns:
        main_tree.column(col, anchor=W, width=100, stretch=True)
    main_tree.heading('#0', text='')
    for col in columns:
        main_tree.heading(col, text=col, anchor=W)
    records = data.to_records(index=False)
    result = list(records)
    for counter, row in enumerate(result):
        main_tree.insert(parent='', index='end', iid=str(counter), text='', values=tuple(row))

    ## Text area
    text_content = Label(txt_frame, fg="black")
    text_content.pack()
    def update_text_content():
        numCols = data.shape[1]
        numRows = data.shape[0]
        dups = data.duplicated().sum() 
        if dups > 0 : x = 'yes' 
        else : x = 'no'
        text_content.config(text=f"Rows: {numRows} / Cols: {numCols} / Duplicates: {x}")
    update_text_content()
    
    ## Stats Treeviews (multiple Treeviews in one row)
    # Tree with data types and missing values
    stats_tree = ttk.Treeview(stats_frame)
    stats_tree.place(rely=0, relx=0, relwidth=0.33, relheight=1)

    """ Add later 
    stats_scroll_Y = Scrollbar(stats_tree, orient="vertical", command=stats_tree.yview)
    stats_scroll_X = Scrollbar(stats_tree, orient="horizontal", command=stats_tree.xview)
    stats_tree.configure(yscrollcommand=stats_scroll_Y.set, xscrollcommand=stats_scroll_X.set)
    stats_scroll_Y.pack(side=RIGHT, fill=Y)
    stats_scroll_X.pack(side=BOTTOM, fill=X) 
    """

    stats_tree['columns'] = ('Column', 'Data Type', 'Missing Values')
    stats_tree.column('#0', width=0, stretch=NO)
    stats_tree.column('Column',anchor=W, width=100, stretch=True)
    stats_tree.column('Data Type',anchor=W, width=100, stretch=True)
    stats_tree.column('Missing Values', anchor=W, width=100, stretch=True)
    stats_tree.heading('#0', text='')
    stats_tree.heading('Column',text='Column', anchor=W)
    stats_tree.heading('Data Type',text='Data Type', anchor=W)
    stats_tree.heading('Missing Values',text='Missing Values', anchor=W)
    df_types = pd.DataFrame(data.dtypes)
    df_types['missing'] = data.isnull().sum(axis=0).values.tolist()
    df_records = df_types.to_records()
    for counter, row in enumerate(list(df_records)):
        stats_tree.insert(parent='', index='end', iid=str(counter), text='', values=tuple(row))

    # Tree with data from column and missing values
    focus_tree = ttk.Treeview(stats_frame)
    focus_tree.place(rely=0, relx=0.33, relwidth=0.33, relheight=1)
    def select_item(event):
        global index
        index = main_tree.selection()[0]
        focus_tree.delete(*focus_tree.get_children())       # delete prev tree
        # insert data into focus_tree
        focus_tree['columns'] = ('Column', 'Content')
        focus_tree.column('#0', width=0, stretch=NO)
        focus_tree.column('Column',anchor=W, width=80)
        focus_tree.column('Content',anchor=W, width=80)
        focus_tree.heading('#0', text='')
        focus_tree.heading('Column',text='Column', anchor=W)
        focus_tree.heading('Content',text='Content', anchor=W)
        # create DataFrame to query data
        select_data = data.iloc[[index]]
        columns = select_data.columns.values.tolist()
        values = select_data.values.tolist()[0]
        df_dict = {'columns': columns, 'content': values}
        df_select = pd.DataFrame(df_dict)
        df_records = df_select.to_records()
        for counter, row in enumerate(list(df_records)):
            lst = [row[1], row[2]]
            focus_tree.insert(parent='', index='end', iid=str(counter), text='', values=tuple(lst))

    # Text field for focused content
    txt = Text(stats_frame, bg="white", fg="black")
    txt.place(rely=0, relx=0.66, relwidth=0.33, relheight=1)
    def show_content(event):
        global index_focus
        index_focus = focus_tree.selection()[0]
        select_data = data.iloc[[index]]
        columns = select_data.columns.values.tolist()
        values_ = select_data.values.tolist()[0]
        str = values_[int(index_focus)]
        txt.delete("1.0", END)
        txt.insert(END, str)

    ## KEYBINDINGS
    main_tree.bind('<ButtonRelease-1>', select_item)
    focus_tree.bind('<ButtonRelease-1>', show_content)

    ## CLOSE ROOT when main window is closed
    main_window.protocol('WM_DELETE_WINDOW', lambda: onclose(main_window))

def onclose(event):
    # function to destroy the root window when main window is closed
    root.destroy()

# Init Tkinter
# Start-window
root = Tk()
root.title("CSV Viewer")
window_width = 200
window_height = 100
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(0,0)

# Styling
style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview.heading", 
background = "silver",
foreground = "black",
)
style.map('Treeview', background=[('selected', 'red')])

# Widgets
open_frame = LabelFrame(root, text="Select a CSV-File to view", fg="black", bd=4)
open_frame.pack(fill="both", expand="yes", padx=10, pady=10)
open_button = Button(open_frame, text="Open File...", fg="black", command=main_window)
open_button.pack(pady=10)

root.mainloop()