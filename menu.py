import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import pytesseract

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.image = None

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="选择图片", command=self.select_image)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)

        self.image_frame = tk.LabelFrame(root)
        self.image_frame.pack()

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        self.text_frame = tk.LabelFrame(root)
        self.text_frame.pack()

        self.text_box = tk.Text(self.text_frame, height=5, width=50)
        self.text_box.pack()

        self.image_label.bind("<ButtonPress-1>", self.start_capture)
        self.image_label.bind("<B1-Motion>", self.capture)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((400, 400))
            self.update_image(self.image)

    def start_capture(self, event):
        self.x = event.x
        self.y = event.y

    def capture(self, event):
        x = min(event.x, self.x)
        y = min(event.y, self.y)
        width = abs(event.x - self.x)
        height = abs(event.y - self.y)
        image_copy = self.image.copy()
        draw = ImageDraw.Draw(image_copy)
        draw.rectangle((x, y, x + width, y + height), outline="red")
        self.update_image(image_copy)

    def update_image(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        text = pytesseract.image_to_string(image)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, text)

root = tk.Tk()
app = ClientApp(root)
root.mainloop()
