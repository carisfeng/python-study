import tkinter as tk
from tkinter import filedialog

def select_directory():
    directory = filedialog.askdirectory()
    directory_label.config(text=directory)

def rename():
    pass

def auto_recognize():
    pass

def draw_recognize():
    pass

def row_column_display():
    pass

def parameter_setting():
    pass

root = tk.Tk()
root.geometry('800x600')

# 第一行
tk.Button(root, text='选择目录', command=select_directory).grid(row=0, column=0, padx=5, pady=5)
tk.Button(root, text='自动改名', command=rename).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text='自动识别', command=auto_recognize).grid(row=0, column=2, padx=5, pady=5)
tk.Button(root, text='画框识别', command=draw_recognize).grid(row=0, column=3, padx=5, pady=5)
tk.Button(root, text='行列显示', command=row_column_display).grid(row=0, column=4, padx=5, pady=5)
tk.Button(root, text='参数设置', command=parameter_setting).grid(row=0, column=5, padx=5, pady=5)

# 第二行
tk.Label(root, text='当前目录：').grid(row=1, column=0, sticky='e', padx=5, pady=5)
directory_label = tk.Label(root, text='')
directory_label.grid(row=1, column=1, columnspan=5, sticky='w', padx=5, pady=5)

# 第三行
tk.Label(root, text='当前文件：').grid(row=2, column=0, sticky='e', padx=5, pady=5)
file_label = tk.Label(root, text='')
file_label.grid(row=2, column=1, columnspan=2, sticky='w', padx=5, pady=5)
tk.Label(root, text='票据好号码：').grid(row=2, column=3, sticky='e', padx=5, pady=5)
entry = tk.Entry(root)
entry.grid(row=2, column=4, padx=5, pady=5)
tk.Button(root, text='改名', command=rename).grid(row=2, column=5, padx=5, pady=5)

# 第四行
listbox = tk.Listbox(root)
listbox.grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky='nsew')
root.grid_rowconfigure(3, weight=1)
root