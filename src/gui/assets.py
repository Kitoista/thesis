import numpy as np
import tkinter as tk
import tkinter.filedialog as fileDialog
from PIL import ImageTk, Image
from . import defaults
from app.imageLib import imageLib

arrow = 'assets/arrow-right.png'
arrowLeft = 'assets/arrow-left.png'
arrowRight = 'assets/arrow-right.png'
placeholder = 'assets/placeholder.png'
content = 'assets/content.png'

def toPhotoImage(input=None, width=None, height=None):
    width = width or defaults.imageSize["width"]
    height = height or defaults.imageSize["height"]

    if input is None:
        input = getFilename()
    elif type(input) == str:
        img = Image.open(input)
    elif type(input) is np.ndarray:
        img = imageLib.convertArrayToImage(input)
    elif type(input) is ImageTk.PhotoImage:
        return input
    else:
        img = input

    img = img.resize((width, height), Image.NEAREST)
    img = ImageTk.PhotoImage(img)

    return img

def loadImage(input=None):
    if input is None:
        return None
    elif type(input) == str:
        img = Image.open(input)
    else:
        img = input

    return imageLib.normalize(img)

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
