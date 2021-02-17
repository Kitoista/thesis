from gui.window import Window
from app.application import app

from skimage.data import shepp_logan_phantom
from PIL import Image

# method = 'iradons'
method = 'annealing'
# method = 'nothing'

if method == 'annealing':
    window = Window()
    window.init(app)
    window.start()
    app.window = window

import skimage
import numpy as np
import matplotlib.pyplot as plt

import random
import math

from app import radon
from app.reconstructors import iradon
from app.reconstructors import iradonSart
from app.error import rms

from app.annealing.annealing import Annealing
from app.annealing.accepts.accept import Accept
from app.annealing.starts.colorStart import ColorStart
from app.annealing.costs.cost import Cost
from app.annealing.temperatures.temperature import Temperature
from app.annealing.neighbours.neighbour import Neighbour

from app.annealing.iterators.iterator import Iterator
from app.annealing.iterators.constantIterator import ConstantIterator
from app.annealing.iterators.costIterator import CostIterator
from app.annealing.iterators.temperatureIterator import TemperatureIterator

from app.annealing.neighbours.positions.position import Position
from app.annealing.neighbours.positions.gridPosition import GridPosition
from app.annealing.neighbours.positions.snakePosition import SnakePosition

from app.annealing.neighbours.fillers.filler import Filler
from app.annealing.neighbours.fillers.shapeFiller import ShapeFiller

from app.annealing.neighbours.fillers.shapes.roundedRectangle import RoundedRectangle
from app.annealing.neighbours.fillers.shapes.triangle import Triangle
from app.annealing.neighbours.fillers.shapes.rectangle import Rectangle

from app.annealing.neighbours.colors.color import Color
from app.annealing.neighbours.colors.copyColor import CopyColor
from app.annealing.neighbours.colors.normCopyColor import NormCopyColor

from gui import event
from app import imageLib


# print('a')
# print(shepp_logan_phantom())
app.image = imageLib.normalize(shepp_logan_phantom())
# print(image.shape)
# print(image)
# exit()
# print('b')
# image = imageLib.normalize(Image.open('pattern.jpg'))

radonTrans = radon.Radon(app.image, app.theta)
sinogram = radonTrans.transform()

if method == 'annealing':
    window.triggerEvent(event.OriginalUpdateEvent(app.image, sinogram))

    annealing = Annealing()
    annealing.accept = Accept()
    annealing.start = ColorStart(shape=app.image.shape, color=0)
    annealing.cost = Cost(sinogram=sinogram, theta = app.theta)
    annealing.temperature = Temperature(start=0.145, alpha=0.000002)
    annealing.neighbour = Neighbour(changesBounds=(1, 1))

    # annealing.iterator = Iterator(maxsteps=50000)
    # annealing.iterator = CostIterator(value=0.8)
    annealing.iterator = ConstantIterator(diff=0.001, overSteps=5000)

    # annealing.neighbour.position = GridPosition(gridSize=20, maxSameCount=100, walkChance=5)
    # annealing.neighbour.position = Position()
    annealing.neighbour.position = SnakePosition(walkChance=5)
    # annealing.neighbour.color = CopyColor(copyChance=0.5, maxDiff=0.1)
    annealing.neighbour.color = NormCopyColor(copyChance=0.5, maxDiff=0.03)

    shapeClassesWithBounds = [
        (Triangle, (5, 12)),
        (RoundedRectangle, (2, 7)),
        (Rectangle, (1, 16))
    ]

    annealing.neighbour.filler = ShapeFiller(shapeClassesWithBounds)

    state = annealing()

# using iradon and iradon sart
def iradons():
    # skimage.io.imsave(f"original.png", np.around(image*255).astype(np.uint8))
    theta = 32
    radonTrans = radon.Radon(image, theta)
    sinogram = radonTrans.transform()
    mode = None
    iterations = 2
    def logger(recon, i):
        # skimage.io.imsave(f"mode{mode}_iteration{i}.png", np.around((recon-image)*255).astype(np.uint8))
        error = rms.error(image, recon)
        print(f"Error ({i} iterations): {error:.3g}")

        # if i == iterations - 1:
        imkwargs = dict(vmin=-0.2, vmax=0.2)
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4.5),
        sharex=True, sharey=True)
        ax1.set_title("Original")
        ax1.imshow(image, cmap=plt.cm.Greys_r)
        ax2.set_title(f"Reconstrunction\n ({mode} iteration{i})")
        ax2.imshow(recon, cmap=plt.cm.Greys_r)
        ax3.set_title(f"Error: {error:.3g}")
        ax3.imshow(recon - image, cmap=plt.cm.Greys_r, **imkwargs)
        plt.show(block=False)



    def oneOf0():
        recon = None
        reconstructor0 = iradon.IRadon(sinogram, theta)
        recon = reconstructor0.transform()
        logger(recon, 0)

    def oneOf1():
        recon = None
        reconstructor1 = iradonSart.IRadonSart(sinogram, theta, 1, recon=recon)
        recon = reconstructor1.transform()
        logger(recon, 0)

    def twoOf1():
        recon = None
        reconstructor1 = iradonSart.IRadonSart(sinogram, theta, iterations, recon=recon)
        recon = reconstructor1.transform()
        logger(recon, iterations)

    def base0into1():
        recon = None
        reconstructor0 = iradon.IRadon(sinogram, theta)
        recon = reconstructor0.transform()

        reconstructor1 = iradonSart.IRadonSart(sinogram, theta, iterations, recon=recon)
        recon = reconstructor1.transform()
        logger(recon, iterations)

    print()
    mode = "IRadon"
    oneOf0()
    print()
    mode = "SART"
    oneOf1()
    print()
    mode = "SARTs"
    twoOf1()
    print()
    mode = "IRadon into SARTs"
    base0into1()
    print()

    input("Press enter to exit ;)")


if method == 'iradons':
    iradons()
