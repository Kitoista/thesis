import numpy as np

from gui import assets
from .start import Start

class ImageStart(Start):
    def __init__(self, shape, imagePath):
        super().__init__(shape)
        self.imagePath = imagePath

    def __call__(self):
        return assets.loadImage(self.imagePath)
