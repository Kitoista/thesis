from skimage.transform import rescale, resize
from PIL import Image, ImageFile
import numpy as np

def normalize(image):
    image = np.asarray(image)
    # if isinstance(image, ImageFile):
    # #     image =
    # print(image.shape[0], image.shape[1])
    # scale = min(160/image.shape[0], 160/image.shape[1])
    # print(scale)
    image = rescale(image, scale=1, mode='reflect', multichannel=False)
    image = resize(image, (160, 160, 1))
    image = np.squeeze(image)
    return image

def convertArrayToImage(array, min=0, max=1):
    new_arr = ((array - array.min()) * (1/(array.max() - array.min()) * 255)).astype('uint8')
    data = np.zeros((new_arr.shape[0], new_arr.shape[1], 3), dtype=np.uint8)
    data[0:data.shape[0], 0:data.shape[1], 0] = new_arr
    data[0:data.shape[0], 0:data.shape[1], 1] = new_arr
    data[0:data.shape[0], 0:data.shape[1], 2] = new_arr
    image = Image.fromarray(data, 'RGB')
    return image
