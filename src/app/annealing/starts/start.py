import numpy as np

class Start:
    def __init__(self, shape):
        self.shape = shape

    def __call__(self):
        return np.random.rand(self.shape[0], self.shape[1])
