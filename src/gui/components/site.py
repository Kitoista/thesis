import tkinter as tk
from .. import assets
from . import imageLabel

class Site:
    def __init__(self, window):
        self.window = window
        self.app = window.app
        self.ready = False

    def activate(self):
        if self.window.activeSite is not None:
            self.window.activeSite.deactivate()

        self.window.activeSite = self
        self.generate()

    def generate(self):
        self.content = tk.Frame(self.window.siteFrame)
        self.generateContent()
        self.content.pack()
        self.ready = True

    def generateContent(self):
        image = imageLabel.ImageLabel(self.content, icon = assets.content)
        image.pack()

    def deactivate(self):
        for child in self.window.siteFrame.winfo_children():
            child.pack_forget()

    def onEvent(self, e):
        pass
