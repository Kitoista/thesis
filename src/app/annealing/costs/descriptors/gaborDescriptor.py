# https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_gabor.html
from scipy import ndimage as ndi
from skimage.filters import gabor_kernel
import numpy as np

from .descriptor import Descriptor
from ....error import error

class GaborDescriptor(Descriptor):
    def __init__(self, thetas, sigmas, frequencies):

        self.kernels = []
        for theta in range(thetas):
            theta = float(theta) / thetas * np.pi
            for sigma in sigmas:
                for frequency in frequencies:
                    kernel = np.real(gabor_kernel(frequency, theta=theta,
                                                  sigma_x=sigma, sigma_y=sigma))
                    self.kernels.append(kernel)

    def __call__(self, image):
        feats = np.zeros(2 * (len(self.kernels)), dtype=np.float)
        for k, kernel in enumerate(self.kernels):
            filtered = ndi.convolve(image, kernel, mode='wrap')
            feats[2 * k] = filtered.mean()
            feats[2 * k + 1] = filtered.var()
        return feats

    def compare(self, goodValue, desc):
        return error.sumDiff(goodValue, desc)

    def show(self, img):
        epic = np.zeros(img.shape)
        for k, kernel in enumerate(self.kernels):
            epic = epic + ndi.convolve(img, kernel, mode='wrap')
        epic = epic / len(self.kernels)
        return epic
