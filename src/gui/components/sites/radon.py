import tkinter as tk
from ... import assets, defaults
from .. import site

class Radon(site.Site):
    def generateContent(self):
        self.workFrame = tk.Frame(self.content)
        self.workFrame.pack(side = tk.TOP, anchor = tk.NW)

        self.inputFrame = tk.Frame(self.workFrame)
        self.inputFrame.grid(row = 0, column = 0)

        self.arrowFrame = tk.Frame(self.workFrame)
        self.workFrame.bind("<Button-1>", lambda a : print('clicked'))
        self.arrowFrame.grid(row = 0, column = 1)

        self.outputFrame = tk.Frame(self.workFrame)
        self.outputFrame.grid(row = 0, column = 2)

        self.window.assets.loadImage(assets.placeholder).place(self.inputFrame)
        self.window.assets.loadImage(assets.arrow, width = defaults.arrowSize["width"], height = defaults.arrowSize["height"]).place(self.arrowFrame)
        self.window.assets.loadImage(assets.placeholder).place(self.outputFrame)

    def showImageOnLeft(self):
        self.window.assets.loadImage().place(self.inputFrame)
