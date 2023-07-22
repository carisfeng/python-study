import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog


def select_directory():
    directory = tk.filedialog.askdirectory()
    directory_label.config(text=directory)
    new_name = new_name_entry.get()
    directory = directory_label.cget("text")
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, new_name)
            os.rename(file_path, new_file_path)

def identify():
    directory = directory_label.cget("text")
    file_list.delete(0, tk.END)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.insert(tk.END, file)

def rename():
    selected_file = file_list.get(file_list.curselection())
    new_name = new_name_entry.get()
    directory = directory_label.cget("text")
    file_path = os.path.join(directory, selected_file)
    new_file_path = os.path.join(directory, new_name)
    os.rename(file_path, new_file_path)
    file_list.delete(file_list.curselection())
    file_list.insert(tk.END, new_name)

def batch_rename():
    new_name = new_name_entry.get()
    directory = directory_label.cget("text")
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, new_name)
            os.rename(file_path, new_file_path)

def show_image():
    selected_file = file_list.get(file_list.curselection())
    directory = directory_label.cget("text")
    file_path = os.path.join(directory, selected_file)
    image = Image.open(file_path)
    image = image.resize((200, 200))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

root = tk.Tk()

select_directory_button = tk.Button(root, text="选择目录", command=select_directory)
select_directory_button.grid(row=0, column=0)

identify_button = tk.Button(root, text="识别", command=identify)
identify_button.grid(row=0, column=1)

rename_button = tk.Button(root, text="改名", command=rename)
rename_button.grid(row=0, column=2)

batch_rename_button = tk.Button(root, text="批量改名", command=batch_rename)
batch_rename_button.grid(row=0, column=3)

directory_label = tk.Label(root)
directory_label.grid(row=1, columnspan=4)

new_name_label = tk.Label(root, text="新文件名:")
new_name_label.grid(row=2, column=0)

new_name_entry = tk.Entry(root)
new_name_entry.grid(row=2, column=1)

file_list = tk.Listbox(root)
file_list.grid(row=3, column=0, rowspan=4)

image_label = tk.Label(root)
image_label.grid(row=3, column=1, rowspan=4)

file_list.bind('<<ListboxSelect>>', lambda event: show_image())

root.mainloop()