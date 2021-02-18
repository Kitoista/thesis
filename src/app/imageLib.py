from skimage.transform import rescale, resize
from PIL import Image, ImageFile
import numpy as np

class ImageLib:
    def __init__(self):
        self.imageSize = 160

    def normalize(self, image):
        image = np.asarray(image)
        image = rescale(image, scale=1, mode='reflect', multichannel=False)
        image = resize(image, (self.imageSize, self.imageSize, 1))
        image = np.squeeze(image)
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
