from skimage.transform import rescale, resize
from PIL import Image, ImageFile
import numpy as np

class ImageLib:
    @property
    def grayScale(self):
        return self._grayScale
    @grayScale.setter
    def grayScale(self, value):
        self._grayScale = value

    @property
    def grayScaleLength(self):
        return len(self._grayScale)
    @grayScaleLength.setter
    def grayScaleLength(self, value):
        self._grayScale = np.linspace(0, 1, value)

    def __init__(self, grayScale = None, grayScaleLength = None):
        self.imageSize = 160
        self._grayScale = None

        if grayScale is not None:
            self.grayScale = grayScale
        elif grayScaleLength is not None:
            self.grayScaleLength = grayScaleLength
        else:
            self.grayScaleLength = 256

    def closestColor(self, color):
        best = 3
        for g in self.grayScale:
            if abs(color - best) > abs(color - g):
                best = g
        return best

    def normalize(self, image):
        image = np.asarray(image)
        image = rescale(image, scale=1, mode='reflect', multichannel=False)
        image = resize(image, (self.imageSize, self.imageSize, 1))
        image = np.squeeze(image)
        for i in range(len(image)):
            for j in range(len(image[i])):
                image[i][j] = self.closestColor(image[i][j])
        return image

    def convertArrayToImage(self, array, min=0, max=1):
        new_arr = ((array - array.min()) * (1/(array.max() - array.min()) * 255)).astype('uint8')
        data = np.zeros((new_arr.shape[0], new_arr.shape[1], 3), dtype=np.uint8)
        data[0:data.shape[0], 0:data.shape[1], 0] = new_arr
        data[0:data.shape[0], 0:data.shape[1], 1] = new_arr
        data[0:data.shape[0], 0:data.shape[1], 2] = new_arr
        image = Image.fromarray(data, 'RGB')
        return image

imageLib = ImageLib()
