# https://www.thepythoncode.com/article/hog-feature-extraction-in-python#:~:text=The%20Histogram%20of%20Oriented%20Gradients,image%20or%20region%20of%20interest.
from skimage.transform import resize
from skimage.feature import hog
from skimage import exposure
import numpy as np

from .descriptor import Descriptor
from ....error import error

class HogDescriptor(Descriptor):
    def __init__(self, orientations, pixelsPerCell, cellsPerBlock):
        self.orientations = orientations
        self.pixelsPerCell = pixelsPerCell
        self.cellsPerBlock = cellsPerBlock

    def __call__(self, image):
        resized_img = resize(image, (128, 64))
        fd = hog(resized_img, orientations=self.orientations, pixels_per_cell=self.pixelsPerCell,
                	cells_per_block=self.cellsPerBlock)
        return fd

    def compare(self, goodValue, desc):
        return error.sumDiff(goodValue, desc)

    def show(self, img):
        resized_img = resize(img, (128, 64))
        fd, hog_image = hog(resized_img, orientations=self.orientations, pixels_per_cell=self.pixelsPerCell,
                	cells_per_block=self.cellsPerBlock, visualize=True)
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
        return hog_image_rescaled
