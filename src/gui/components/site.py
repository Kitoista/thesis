import tkinter as tk
from .. import assets

class Site:
    def __init__(self, window):
        self.window = window

    def activate(self):
        if self.window.activeSite is not None:
            self.window.activeSite.deactivate()

        self.window.activeSite = self
        self.generate()

    def generate(self):
        self.content = tk.Frame(self.window.siteFrame)
        self.generateContent()
        self.content.pack()

    def generateContent(self):
        self.window.assets.loadImage(assets.content).place(self.content)

    def deactivate(self):
        for child in self.window.siteFrame.winfo_children():
            child.pack_forget()
