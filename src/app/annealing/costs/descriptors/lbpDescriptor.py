from skimage import feature
import numpy as np

from .descriptor import Descriptor
from ....error import error

class LbpDescriptor(Descriptor):
    def __init__(self, numPoints, radius):
        # store the number of points and radius
        self.numPoints = numPoints
        self.radius = radius
        self.eps = 1e-7

    def __call__(self, state):
        # compute the Local Binary Pattern representation
        # of the state, and then use the LBP representation
        # to build the histogram of patterns
        lbp = feature.local_binary_pattern(state, self.numPoints,
            self.radius, method="uniform")
        (hist, _) = np.histogram(lbp.ravel(),
            bins=np.arange(0, self.numPoints + 3),
            range=(0, self.numPoints + 2))
        # normalize the histogram
        hist = hist.astype("float")
        hist /= (hist.sum() + self.eps)
        # return the histogram of Local Binary Patterns
        return hist

    def compare(self, goodValue, desc):
        return error.maxDiff(goodValue, desc)

    def show(self, img):
        return feature.local_binary_pattern(img, self.numPoints,
            self.radius, method="uniform")
