import numpy as np
import matplotlib.pyplot as plt

from skimage.transform import radon

class Radon:

    def __init__(self, image, theta):
        self.image = image
        self.theta = np.linspace(0., 180., theta, endpoint=False)

    def transform(self):
        sinogram = radon(self.image, theta=self.theta, circle=True)
        return sinogram
