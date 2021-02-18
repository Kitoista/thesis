import tkinter as tk
from .. import defaults, assets
from . import site
from .sites import gallery, radon

class Menu:
    def __init__(self, window):
        self.window = window

    def generate(self):
        menubar = tk.Menu(self.window.gui)
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Open", command = self.window.openImage)

        menubar.add_cascade(label = "File", menu = filemenu)
        menubar.add_command(label = "Gallery", command = lambda : self.window.setActiveSite(gallery.Gallery))
        menubar.add_command(label = "Radon", command = lambda : self.window.setActiveSite(radon.Radon))

        self.window.gui.config(menu = menubar)
