# CSV-Viewer by Markus Müller

from tkinter import *
from tkinter import ttk, filedialog
import pandas as pd
import os
import pyclip as pc

# Flag for active search
search_bool = False


# Functions
def main_window():
    # almost everything gets managed here
    global file_path
    cwd = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir=cwd, filetypes=[("CSV file", "*.csv")])
    root.withdraw()
    main_window = Toplevel(root)
    main_window.title("CSV Viewer")
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    main_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def new_file():
        # exit current window and unhide root window to select new file
        main_window.destroy()
        root.deiconify()

    def root_exit():
        main_window.destroy()
        root.destroy()

    def search_data():
        # get data from entry
        search_str = search_entry.get()
        search_win.destroy()
        # delete treeview
        main_tree.delete(*main_tree.get_children())
        txt.delete("1.0", END)
        focus_tree.delete(*focus_tree.get_children())
        stats_tree.delete(*stats_tree.get_children())
        # check the format of the search string
        # if "=" in search_str:
        search_col = search_str.split("=")[0]
        search_str = search_str.split("=")[1]

        # query data
        # check dtype of column
        if data[search_col].dtype != 'object':
            if "." in search_str:
                search_str = float(search_str)
            else:
                search_str = int(search_str)

        global data_query
        data_query = data.loc[data[search_col] == search_str]
        global search_bool
        search_bool = True
        populatemaintree(data_query)
        update_text_content(data_query)
        update_types_content(data_query)

    def search():
        global search_entry, search_win
        search_win = Toplevel(main_window)
        search_win.title("Search")
        search_win.geometry("350x150")
        search_frame = LabelFrame(search_win, text="Search", fg="black", bd=3, pady=5, padx=5)
        search_frame.pack(pady=5, padx=5)
        search_help_txt = Text(search_frame, height=2, fg="black", bg="white")
        search_help_txt.pack()
        search_help_txt.insert(END, "write the name of the column and then the \n search string:  col=search_string")
        search_entry = Entry(search_frame, bg="white", fg="black")
        search_entry.pack(padx=5, pady=5)
        search_button = Button(search_frame, text="Search", fg="black", bg="white", command=search_data)
        search_button.pack()

    def resetsearch():
        global search_bool
        search_bool = False
        # delete every bit of content in each tree
        main_tree.delete(*main_tree.get_children())
        stats_tree.delete(*stats_tree.get_children())
        # draw tree with start content
        populatemaintree(data)
        update_text_content(data)
        update_types_content(data)

    def about():
        about_window = Toplevel(main_window)
        about_window.title("About")
        about_window.geometry("300x400")
        about_frame = LabelFrame(about_window, text="About", fg="black", bd=3, pady=5, padx=5)
        about_frame.pack(pady=5, padx=5)
        txt = Text(about_frame, bg="white", fg="black")
        txt.pack(fill='both', expand=True)
        str_ = "CSV-Viewer created by Markus Müller\n\nFunctions:\n- copy to clipboard \n" \
               "- search csv file \n- order columns when clicking on heading"
        txt.insert(END, str_)

    def clipboard(event):
        # allows user to save selected content to system clipboard (only in main_tree)
        try:
            m.tk_popup(event.x_root, event.y_root)
            col = main_tree.identify_column(event.x)
            col = col[1:]
            col = int(col) - 1
            index = main_tree.selection()[0]
            copy_to_clipboard = data.iloc[[index]].values[0][col]
            pc.copy(copy_to_clipboard)
        except pc.base.ClipboardException:
            pass
        finally:
            m.grab_release()

    def ordercolumn(c):
        # check if search_bool is True
        if search_bool:
            df_sorted = data_query.sort_values(by=[c])
        else:
            df_sorted = data.sort_values(by=[c])
        main_tree.delete(*main_tree.get_children())
        populatemaintree(df_sorted)

    # misc
    m = Menu(root, tearoff=0)
    m.add_command(label='Copy to Clipboard')

    # menubar
    menubar = Menu(main_window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=new_file)
    filemenu.add_command(label="Exit", command=root_exit)
    menubar.add_cascade(label="File", menu=filemenu)
    search_menu = Menu(menubar)
    menubar.add_cascade(label='Search', menu=search_menu)
    search_menu.add_command(label='Search', command=search)
    search_menu.add_separator()
    search_menu.add_command(label='Reset Search', command=resetsearch)
    aboutmenu = Menu(menubar)
    menubar.add_cascade(label="About", menu=aboutmenu)
    aboutmenu.add_command(label="About", command=about)
    root.config(menu=menubar)

    # FRAMES
    # Main Frame where the CSV-Viewer is placed
    main_frame = LabelFrame(main_window, text="Main View", fg="black", bd=3, pady=5, padx=5)
    main_frame.pack(fill='both', expand=True, padx=5, pady=5)
    # PLACEHOLDER frame where text information is placed
    txt_frame = LabelFrame(main_window, text="File Information", fg="black", bd=3, pady=5, padx=5, height=50)
    txt_frame.pack(fill='both', expand=FALSE, padx=5, pady=5)
    # Stats Frame where more Information about the file and row is placed
    stats_frame = LabelFrame(main_window, text="More Information", fg="black", bd=3, pady=5, padx=5)
    stats_frame.pack(fill='both', expand=True, padx=5, pady=5)

    # READ DATA
    data = pd.read_csv(file_path)

    # WIDGETS
    # Main Treeview
    main_tree = ttk.Treeview(main_frame)
    main_tree.place(rely=0, relx=0, relwidth=1, relheight=1)

    scroll_y = Scrollbar(main_frame, orient="vertical", command=main_tree.yview)
    scroll_x = Scrollbar(main_frame, orient="horizontal", command=main_tree.xview)
    main_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)

    def populatemaintree(data_frame):
        data = data_frame
        columns = data.columns.values
        columns_tuple = tuple(columns)
        main_tree['columns'] = columns_tuple
        main_tree.column('#0', width=0, stretch=NO)
        for col in columns:
            main_tree.column(col, anchor=W, width=100, stretch=True)
        main_tree.heading('#0', text='')
        for col in columns:
            main_tree.heading(col, text=col, anchor=W, command=lambda c=col: ordercolumn(c))
        records = data.to_records(index=False)
        result = list(records)
        for counter, row in enumerate(result):
            main_tree.insert(parent='', index='end', iid=str(counter), text='', values=tuple(row))

    populatemaintree(data)

    # Text area
    text_content = Label(txt_frame, fg="black")
    text_content.pack()

    def update_text_content(data_frame):
        data = data_frame
        numCols = data.shape[1]
        numRows = data.shape[0]
        dups = data.duplicated().sum()
        if dups > 0:
            x = 'yes'
        else:
            x = 'no'
        text_content.config(text=f"Rows: {numRows} / Cols: {numCols} / Duplicates: {x}")

    update_text_content(data)

    # Stats Treeviews (multiple Treeviews in one row)
    # Tree with data types and missing values
    stats_tree = ttk.Treeview(stats_frame)
    stats_tree.place(rely=0, relx=0, relwidth=0.40, relheight=1)

    stats_tree['columns'] = ('Column', 'Data Type', 'Missing Values', 'Unique Values')
    stats_tree.column('#0', width=0, stretch=NO)
    stats_tree.column('Column', anchor=W, width=100, stretch=True)
    stats_tree.column('Data Type', anchor=W, width=100, stretch=True)
    stats_tree.column('Missing Values', anchor=W, width=100, stretch=True)
    stats_tree.column('Unique Values', anchor=W, width=100, stretch=True)
    stats_tree.heading('#0', text='')
    stats_tree.heading('Column', text='Column', anchor=W)
    stats_tree.heading('Data Type', text='Data Type', anchor=W)
    stats_tree.heading('Missing Values', text='Missing Values', anchor=W)
    stats_tree.heading('Unique Values', text='Unique Values', anchor=W)

    def update_types_content(data_frame):
        data = data_frame
        df_types = pd.DataFrame(data.dtypes)
        df_types['missing'] = data.isnull().sum(axis=0).values.tolist()
        # calculate number of unique values
        nunique_list = []
        for col in data.columns:
            nunique_list.append(data[col].nunique())
        df_types['unique'] = nunique_list
        df_records = df_types.to_records()
        for counter, row in enumerate(list(df_records)):
            stats_tree.insert(parent='', index='end', iid=str(counter), text='', values=tuple(row))

    update_types_content(data)

    # Tree with data from column and missing values
    focus_tree = ttk.Treeview(stats_frame)
    focus_tree.place(rely=0, relx=0.40, relwidth=0.30, relheight=1)

    def select_item(event):
        global index
        index = main_tree.selection()[0]
        focus_tree.delete(*focus_tree.get_children())  # delete prev tree
        txt.delete("1.0", END)
        # insert data into focus_tree
        focus_tree['columns'] = ('Column', 'Content')
        focus_tree.column('#0', width=0, stretch=NO)
        focus_tree.column('Column', anchor=W, width=80)
        focus_tree.column('Content', anchor=W, width=80)
        focus_tree.heading('#0', text='')
        focus_tree.heading('Column', text='Column', anchor=W)
        focus_tree.heading('Content', text='Content', anchor=W)
        # create DataFrame to query data
        # check if Search is active to use different DataFrame
        if search_bool:
            select_data = data_query.iloc[[index]]
        else:
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
    txt.place(rely=0, relx=0.70, relwidth=0.30, relheight=1)

    def show_content(event):
        global index_focus
        index_focus = focus_tree.selection()[0]
        select_data = data.iloc[[index]]
        columns = select_data.columns.values.tolist()
        values_ = select_data.values.tolist()[0]
        index_str = values_[int(index_focus)]
        txt.delete("1.0", END)
        txt.insert(END, index_str)

    # KEYBINDINGS
    main_tree.bind('<ButtonRelease-1>', select_item)
    main_tree.bind('<ButtonRelease-2>', clipboard)
    focus_tree.bind('<ButtonRelease-1>', show_content)

    # CLOSE ROOT when main window is closed
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
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

# Styling
style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview.heading",
                background="silver",
                foreground="black",
                )
style.map('Treeview', background=[('selected', 'red')])

# Widgets
open_frame = LabelFrame(root, text="Select a CSV-File to view", fg="black", bd=4)
open_frame.pack(fill="both", expand="yes", padx=10, pady=10)
open_button = Button(open_frame, text="Open File...", fg="black", command=main_window)
open_button.pack(pady=10)

root.mainloop()
