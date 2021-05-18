import tkinter as tk
import numpy as np
import time

from app.annealing.costs.descriptors.lbpDescriptor import LbpDescriptor
from app.annealing.costs.descriptors.cooccDescriptor import CooccDescriptor
from app.annealing.costs.descriptors.gaborDescriptor import GaborDescriptor
from app.annealing.costs.descriptors.hogDescriptor import HogDescriptor
# from app.imageLib import imageLib
from ... import assets
from .. import formSite, imageLabel

class Descriptors(formSite.FormSite):

    def generateContent(self):
        self.initForm(self.content)
        self.generateImageFrame()

    def generateImageFrame(self):
        self.rightFrame = tk.Frame(self.content)
        self.rightFrame.pack(side = tk.RIGHT, anchor = tk.NW)

        self.imageFrame = tk.Frame(self.rightFrame)
        self.imageFrame.pack(side = tk.TOP, anchor = tk.NW)

        self.logFrame = tk.Frame(self.rightFrame)
        self.logFrame.pack(side = tk.BOTTOM, anchor = tk.NW)

        self.originalFrame = tk.Frame(self.imageFrame)
        self.originalFrame.grid(row = 0, column = 0)
        self.descFrame = tk.Frame(self.imageFrame)
        self.descFrame.grid(row = 0, column = 1)

        self.img_original = imageLabel.ImageLabel(self.originalFrame, icon = assets.placeholder)
        self.img_original.pack()
        self.img_desc = imageLabel.ImageLabel(self.descFrame, icon = assets.placeholder)
        self.img_desc.pack()

        self.log = tk.StringVar(self.logFrame)

        logInput = tk.Entry(self.logFrame, textvariable=self.log)
        logInput.config(width = 75)
        logInput.pack()

    def generateForm(self):
        self.line()
        self.title("Texture descriptor tester")
        self.line()

        self.title("Image")
        self.imageLoader("original", "Path", "original.png")
        self.select("grayScaleType", "Gray scale", ["List", "Equal"], subSettings=True)
        self.grayScaleTypeSettings = [
            self.input("grayScale", "Scale values e.g. 0 0.3 1", self.arrayString(self.app.grayScale), type=self.floatArrayType),
            self.input("grayScaleLength", "Scale length", self.app.grayScaleLength, type=int),
        ]
        self.line()

        self.title("Descriptor")
        self.select("descriptor", "Method", ["Coocc", "Lbp", "Gabor", "Hog"], subSettings=True)
        self.descriptorSettings = [
            [
                self.input("cooccDistances", "Distances", self.arrayString([1, 2, 3, 4, 5]), type=self.floatArrayType),
                self.input("cooccAngles", "Angles", self.arrayString([0, np.pi/4, np.pi/2, 3*np.pi/4]), type=self.floatArrayType),
            ],
            [
                self.input("lbpNumPoints", "Number of points", 4, type=int),
                self.input("lbpRadius", "Radius", 1, type=int),
            ],
            [
                self.input("gaborThetas", "Theta", 2, type=int),
                self.input("gaborSigmas", "Sigmas", self.arrayString([1, 2]), type=self.floatArrayType),
                self.input("gaborFrequencies", "Frequencies", self.arrayString([0.05, 0.25]), type=self.floatArrayType),
            ],
            [
                self.input("hogOrientations", "Orientations", 9, type=int),
                self.input("hogPixelsPerCell", "Pixels per cell", self.arrayString([8, 8]), type=self.intArrayType),
                self.input("hogCellsPerBlock", "Cells per block", self.arrayString([2, 2]), type=self.intArrayType),
            ],
        ]
        self.line()

        self.submitButton()
        self.verticalLine()

    def replaceImage(self, image, icon):
        if icon is not None:
            newImage = assets.toPhotoImage(icon)
            image.configure(image=newImage)
            image.image = newImage

    def onSubmit(self):
        values = self.getValues()

        if values['grayScaleType'] == "Equal":
            self.app.grayScaleLength = values['grayScaleLength']
        else:
            self.app.grayScale = values['grayScale']

        # print(self.app.grayScale)

        original = assets.loadImage(values['original'])

        self.replaceImage(self.img_original, original)

        params = []
        descriptor = None
        if values['descriptor'] == 'Lbp':
            descriptor = LbpDescriptor(values['lbpNumPoints'], values['lbpRadius'])
            params = [values['lbpNumPoints'], values['lbpRadius']]
        elif values['descriptor'] == 'Coocc':
            descriptor = CooccDescriptor(values['cooccDistances'], values['cooccAngles'], self.app.grayScale)
            params = [values['cooccDistances'], values['cooccAngles']]
        elif values['descriptor'] == 'Gabor':
            descriptor = GaborDescriptor(values['gaborThetas'], values['gaborSigmas'], values['gaborFrequencies'])
            params = [values['gaborThetas'], values['gaborSigmas'], values['gaborFrequencies']]
        elif values['descriptor'] == 'Hog':
            descriptor = HogDescriptor(values['hogOrientations'], values['hogPixelsPerCell'], values['hogCellsPerBlock'])
            params = [values['hogOrientations'], values['hogPixelsPerCell'], values['hogCellsPerBlock']]

        self.replaceImage(self.img_desc, descriptor.show(original))

        timeA = time.time()
        desc = descriptor(original)
        timeB = time.time()
        desc_str = str(desc)
        if type(desc) is np.ndarray:
            desc_str = " ".join(map(lambda x: f"{x:.5g}", desc.flatten()))

        print(f"{values['descriptor']}:\t {(timeB - timeA):.3g} ms\t{params}" )

        self.log.set(desc_str)
