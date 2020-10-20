import tkinter as tk
import tkinter.filedialog as fileDialog
from PIL import ImageTk, Image
from . import defaults

arrow = '../assets/arrow-right.png'
arrowLeft = '../assets/arrow-left.png'
arrowRight = '../assets/arrow-right.png'
placeholder = '../assets/placeholder.png'
content = '../assets/content.png'

def loadImage(filename=None, width=None, height=None):
    width = width or defaults.imageSize["width"]
    height = height or defaults.imageSize["height"]

    if filename is None:
        filename = getFilename()

    img = Image.open(filename)
    img = img.resize((width, height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    return img

def getFilename():
    filename = fileDialog.askopenfilename(title='open')
    return filename

def getFilenames():
    filenames = fileDialog.askopenfilenames(title='open')
    return filenames

def getImage():
    filename = fileDialog.askopenfilename(title='open', filetypes=[("Images", ".jpg .png")])
    return filename

def getImages():
    filenames = fileDialog.askopenfilenames(title='open', filetypes=[("Images", ".jpg .png")])
    return filenames
