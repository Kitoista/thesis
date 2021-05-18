import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import skimage
from skimage.data import shepp_logan_phantom
import warnings

from app import radon
from app.application import app
from app.error import error
from app.imageLib import imageLib
from app.reconstructors import iradon
from app.reconstructors import iradonSart
from app.annealing.costs.descriptors.lbpDescriptor import LbpDescriptor

from gui import event, assets
from gui.window import Window

# warnings.filterwarnings("")

app.window = Window()
app.window.init(app)
app.window.start()

# time.sleep(1)

# lbp = LbpDescriptor(4, 1)
# img = assets.loadImage(assets.getImage())
# app.window.show(img)
# app.window.show(lbp.show(img))
# print(lbp.show(img))
# print(lbp(img))

# app.grayScale = [0, 1]
# app.image = imageLib.normalize(shepp_logan_phantom())
# image = imageLib.normalize(Image.open('brick.jpg'))
#
# method = "iradons"
#
#
# # using iradon and iradon sart
#
# def iradons():
#     # skimage.io.imsave(f"original.png", np.around(image*255).astype(np.uint8))
#     theta = 180
#     radonTrans = radon.Radon(image, theta, (0., 180.))
#     sinogram = radonTrans.transform()
#     mode = None
#     iterations = 2
#     def logger(recon, i):
#         # skimage.io.imsave(f"mode{mode}_iteration{i}.png", np.around((recon-image)*255).astype(np.uint8))
#         error = error.rms(image, recon)
#         print(f"Error ({i} iterations): {error:.3g}")
#
#         # if i == iterations - 1:
#         imkwargs = dict(vmin=-0.2, vmax=0.2)
#         fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4.5),
#         sharex=True, sharey=True)
#         ax1.set_title("Original")
#         ax1.imshow(image, cmap=plt.cm.Greys_r)
#         ax2.set_title(f"Reconstrunction\n ({mode} iteration{i})")
#         ax2.imshow(recon, cmap=plt.cm.Greys_r)
#         ax3.set_title(f"Error: {error:.3g}")
#         ax3.imshow(recon - image, cmap=plt.cm.Greys_r, **imkwargs)
#         plt.show(block=False)
#
#
#
#     def oneOf0():
#         recon = None
#         reconstructor0 = iradon.IRadon(sinogram, theta)
#         recon = reconstructor0.transform()
#         logger(recon, 0)
#
#     def oneOf1():
#         recon = None
#         reconstructor1 = iradonSart.IRadonSart(sinogram, theta, 1, recon=recon)
#         recon = reconstructor1.transform()
#         logger(recon, 0)
#
#     def twoOf1():
#         recon = None
#         reconstructor1 = iradonSart.IRadonSart(sinogram, theta, iterations, recon=recon)
#         recon = reconstructor1.transform()
#         logger(recon, iterations)
#
#     def base0into1():
#         recon = None
#         reconstructor0 = iradon.IRadon(sinogram, theta)
#         recon = reconstructor0.transform()
#
#         reconstructor1 = iradonSart.IRadonSart(sinogram, theta, iterations, recon=recon)
#         recon = reconstructor1.transform()
#         logger(recon, iterations)
#
#     print()
#     mode = "IRadon"
#     oneOf0()
#     print()
#     mode = "SART"
#     oneOf1()
#     print()
#     mode = "SARTs"
#     twoOf1()
#     print()
#     mode = "IRadon into SARTs"
#     base0into1()
#     print()
#
#     input("Press enter to exit ;)")
#
#
# if method == 'iradons':
#     iradons()
