import tkinter as tk
from ... import assets, defaults
from .. import site

class Gallery(site.Site):
    def generateContent(self):
        title = tk.Label(self.content, text = 'Gallery', fg = "#555555")
        title.config(font=(None, 44))
        title.grid(row = 0, column = 1)

        container = tk.Label(self.content)
        self.window.assets.loadImage(assets.arrowLeft, width = defaults.arrowSize["width"], height = defaults.arrowSize["height"]).place(container)
        container.grid(row = 1, column = 0)

        container = tk.Label(self.content)
        self.window.assets.loadImage(assets.placeholder).place(container)
        container.grid(row = 1, column = 1)

        container = tk.Label(self.content)
        self.window.assets.loadImage(assets.arrow, width = defaults.arrowSize["width"], height = defaults.arrowSize["height"]).place(container)
        container.grid(row = 1, column = 2)
