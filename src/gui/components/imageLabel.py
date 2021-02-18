import tkinter as tk
from .. import assets, defaults

class ImageLabel(tk.Label):
    def __init__(self, container, **kwargs):
        icon = kwargs["icon"]
        del kwargs["icon"]

        width = kwargs.get("width") or defaults.imageSize["width"]
        height = kwargs.get("height") or defaults.imageSize["height"]

        kwargs["image"] = assets.toPhotoImage(icon, width = width, height = height)

        tk.Label.__init__(self, container, **kwargs)

        self.image = kwargs["image"]
