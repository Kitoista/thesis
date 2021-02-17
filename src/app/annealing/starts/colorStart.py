import numpy as np

from .start import Start

class ColorStart(Start):
    def __init__(self, shape, color):
        super().__init__(shape)
        self.color = color

    def __call__(self):
        return np.full(self.shape, self.color, dtype=float)
