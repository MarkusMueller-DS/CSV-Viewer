import tkinter as tk

root = tk.Tk()
root.geometry("600x400")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=2)

root.rowconfigure(0, weight=2)
root.rowconfigure(1, weight=1)

frame_left= tk.Frame(root)

openFolder = tk.Label(frame_left, text="Open Folder...", bg="green", fg="black")
listBox = tk.Label(frame_left, text="ListBox", bg="red", fg="black")

openFolder.grid(row=0, column=0, sticky="EW", pady=3)
listBox.grid(row=1, column=0, sticky="EW")

frame_left.grid(row=0, column=0, sticky="ns")

treeView = tk.Label(root, text="TreeView", bg="blue", fg="white")
treeView.grid(column=1, row=0, columnspan=2, sticky="NESW")

stats = tk.Label(root, text="stats", bg="orange", fg="white")
stats.grid(column=1, row=1, sticky="NESW")

viewContent = tk.Label(root, text="content", bg="deep pink", fg="white")
viewContent.grid(column=2, row=1, sticky="NESW")


root.mainloop()