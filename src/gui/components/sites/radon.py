import tkinter as tk
from ... import assets, defaults
from .. import site, imageLabel

class Radon(site.Site):
    def generateContent(self):
        self.workFrame = tk.Frame(self.content)
        self.workFrame.pack(side = tk.TOP, anchor = tk.NW)

        self.inputFrame = tk.Frame(self.workFrame)
        self.inputFrame.grid(row = 0, column = 0)

        self.arrowFrame = tk.Frame(self.workFrame)
        self.arrowFrame.grid(row = 0, column = 1)

        self.outputFrame = tk.Frame(self.workFrame)
        self.outputFrame.grid(row = 0, column = 2)

        self.input = imageLabel.ImageLabel(self.inputFrame, icon = assets.placeholder)
        self.input.pack()
        self.arrow = imageLabel.ImageLabel(self.arrowFrame, icon = assets.arrow, width = defaults.arrowSize["width"], height = defaults.arrowSize["height"])
        self.arrow.pack()
        self.output = imageLabel.ImageLabel(self.outputFrame, icon = assets.placeholder)
        self.output.pack()

        self.arrow.bind('<Button-1>', lambda x : print('TRANSFORM'))

    def showImageOnLeft(self):
        assets.loadImage().place(self.inputFrame)
