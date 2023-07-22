import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import pytesseract

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.image = None

        self.select_button = tk.Button(root, text="选择图片", command=self.select_image)
        self.select_button.pack()

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
        self.image_label.bind("<ButtonRelease-1>", self.img2text)

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
        
    def img2text(self,event):
        x = min(event.x, self.x)
        y = min(event.y, self.y)
        width = abs(event.x - self.x)
        height = abs(event.y - self.y)
        cropped_image = self.image.crop((x, y, x + width, y + height))
        
        self.update_image(cropped_image)
        
        text = pytesseract.image_to_string(cropped_image)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, text)

root = tk.Tk()
app = ClientApp(root)
root.mainloop()
