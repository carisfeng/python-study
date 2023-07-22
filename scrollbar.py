import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def select_directory():
    directory = filedialog.askdirectory()
    #directory_label.config(text=directory)
    file_list.delete(0, tk.END)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.insert(tk.END, file)

root = tk.Tk()

select_directory_button = tk.Button(root, text="选择目录", command=select_directory)
select_directory_button.grid(row=0, column=0)

file_list_frame = tk.Frame(root)
file_list_frame.grid(row=1, column=0, columnspan=2)

file_list_scrollbar_y = tk.Scrollbar(file_list_frame)
file_list_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

file_list_scrollbar_x = tk.Scrollbar(file_list_frame, orient=tk.HORIZONTAL)
file_list_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

file_list = tk.Listbox(file_list_frame, yscrollcommand=file_list_scrollbar_y.set, xscrollcommand=file_list_scrollbar_x.set)
file_list.pack(side=tk.LEFT, fill=tk.BOTH)

file_list_scrollbar_y.config(command=file_list.yview)
file_list_scrollbar_x.config(command=file_list.xview)

#file_list_scrollbar_x.config(width=20,bg="blue")
file_list_scrollbar_x.set(0,0)

root.mainloop()
