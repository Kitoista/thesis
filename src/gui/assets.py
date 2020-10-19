import tkinter as tk
import tkinter.filedialog as fileDialog
from PIL import ImageTk, Image
from . import defaults

arrow = '../assets/arrow-right.png'
arrowLeft = '../assets/arrow-left.png'
arrowRight = '../assets/arrow-right.png'
placeholder = '../assets/placeholder.png'
content = '../assets/content.png'

class AssetLoader:
    def loadImage(self, filename=None, width=None, height=None):
        width = width or defaults.imageSize["width"]
        height = height or defaults.imageSize["height"]

        if filename is None:
            filename = self.openfn()

        img = Image.open(filename)
        img = img.resize((width, height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        return ImageAsset(img)

    def openfn(self):
        filename = fileDialog.askopenfilename(title='open')
        return filename


class ImageAsset:
    def __init__(self, image):
        self.image = image

    def place(self, container):
        for child in container.winfo_children():
            child.pack_forget()

        imageLabel = tk.Label(container, image = self.image)
        imageLabel.image = self.image
        imageLabel.pack(side = tk.LEFT)
