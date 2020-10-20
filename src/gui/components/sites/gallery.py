import tkinter as tk
from ... import assets, defaults, event
from .. import site, imageLabel

class Gallery(site.Site):

    _index = 0

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if value <= 0:
            self._index = 0
        elif value >= len(self.window.app.images):
            self._index = len(self.window.app.images) - 1
        else:
            self._index = value

    def generateContent(self):
        title = tk.Label(self.content, text = 'Gallery', fg = defaults.gray)
        title.config(font=(None, 44))
        title.grid(row = 0, column = 1)

        left = imageLabel.ImageLabel(self.content, icon = assets.arrowLeft, width = defaults.arrowSize["width"], height = defaults.arrowSize["height"])
        left.grid(row = 1, column = 0)
        left.bind('<Button-1>', self.left)

        self.image = None
        self.reset()

        right = imageLabel.ImageLabel(self.content, icon = assets.arrowRight, width = defaults.arrowSize["width"], height = defaults.arrowSize["height"])
        right.grid(row = 1, column = 2)
        right.bind('<Button-1>', self.right)

    def step(self, modifier):
        old = self.index
        self.index = self.index + modifier
        new = self.index
        if old != new:
            self.redrawActiveImage()

    def left(self, *args):
        self.step(-1)

    def right(self, *args):
        self.step(1)

    def reset(self):
        self.index = 0
        self.redrawActiveImage()

    def redrawActiveImage(self):
        if self.image is not None:
            self.image.pack_forget()

        if len(self.window.app.images) == 0:
            self.image = imageLabel.ImageLabel(self.content, icon = assets.placeholder)
        else:
            self.image = imageLabel.ImageLabel(self.content, icon = self.window.app.images[self.index])

        self.image.grid(row = 1, column = 1)

    def onEvent(self, e):
        if e.type == event.ImagesUpdateEvent:
            self.reset()
