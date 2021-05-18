import tkinter as tk
from tkinter import ttk
import re
import numpy as np

from ... import assets, defaults
from .. import formSite, imageLabel
from . import annealing

class Settings(formSite.FormSite):

    def generateContent(self):
        self.initForm(self.content)

    def generateForm(self):
        self.values = {}
        if self.app.settings is not None:
            self.values = self.app.settings

        self.title("Settings")
        self.input("showBundles", "Show bundles", self.app.showBundles, type=int)
        self.input("threadPoolSize", "Threads", 8, type=int)
        self.input("threadLength", "Thread length", 100, type=int)

        self.title("Image")
        self.imageLoader("imagePath", "Path", "original.png")
        self.input("imageSize", "Size", self.app.imageSize, type=int)
        self.select("grayScaleType", "Gray scale", ["List", "Equal"], subSettings=True)
        self.grayScaleTypeSettings = [
        self.input("grayScale", "Scale values e.g. 0 0.3 1", self.arrayString(self.app.grayScale), type=self.floatArrayType),
            self.input("grayScaleLength", "Scale length", self.app.grayScaleLength, type=int),
        ]

        self.line()

        self.title("Radon")
        self.input("theta", "Theta", self.app.theta, type=int)
        self.input("radonAngleBoundsMin", "Angle start", self.app.radonAngleBounds[0])
        self.input("radonAngleBoundsMax", "Angle end", self.app.radonAngleBounds[1])
        self.line()

        self.title("Temperature")
        self.input("temperatureStart", "Start", 0.145)
        self.input("temperatureAlpha", "Alpha (step)", 0.000002)
        self.line()

        self.title("Start")
        self.select("start", "Method", ["Color", "Image", "Random"], subSettings=True)
        self.startSettings = [
            [ self.input("colorStartColor", "Color [0, 1]", 0) ],
            [ self.imageLoader("imageStartImagePath", "Image") ],
            [ ],
        ]
        self.line()


        self.newColumn()

        self.title("Stop criteria")
        self.select("iterator", "Method", ["Constant", "Temperature", "Step", "Cost"], subSettings=True)

        self.iteratorSettings = [
            [
                self.input("constantIteratorDiff", "Cost difference is less than", 0.001),
                self.input("constantIteratorOverSteps", "Over x steps", 4000, type=int)
            ],
            [ self.input("temperatureIteratorTEnd", "Temperature is less than", 0.0002) ],
            [ self.input("stepIteratorMaxSteps", "Max", 200000, type=int) ],
            [ self.input("costIteratorValue", "Cost is less than", 0.8) ],
        ]
        self.line()


        self.title("Cost")
        self.input("costGoodValue", "Good value", self.goodValueString(), type=self.goodValueType),
        self.input("costLambda", "Lambda", self.arrayString([0, 10]), type=self.floatArrayType),
        self.input("costKappa", "Kappa", 1),


        self.title("Descriptor")
        self.select("descriptor", "Method", ["None", "Homogenity", "Lbp", "Coocc", "Gabor", "Hog"], subSettings=True)

        self.descriptorSettings = [
            [ ],
            [ ],
            [
                self.input("lbpDescriptorNumPoints", "Number of points", 4, type=int),
                self.input("lbpDescriptorRadius", "Radius", 1, type=int),
            ],
            [
                self.input("cooccDescriptorDistances", "Distances", self.arrayString([1, 2, 3, 4, 5]), type=self.floatArrayType),
                self.input("cooccDescriptorAngles", "Angles", self.arrayString([0, np.pi/4, np.pi/2, 3*np.pi/4]), type=self.floatArrayType),
            ],
            [
                self.input("gaborDescriptorThetas", "Theta", 2, type=int),
                self.input("gaborDescriptorSigmas", "Sigmas", self.arrayString([1, 2]), type=self.floatArrayType),
                self.input("gaborDescriptorFrequencies", "Frequencies", self.arrayString([0.05, 0.25]), type=self.floatArrayType),
            ],
            [
                self.input("hogDescriptorOrientations", "Orientations", 9, type=int),
                self.input("hogDescriptorPixelsPerCell", "Pixels per cell", self.arrayString([8, 8]), type=self.intArrayType),
                self.input("hogDescriptorCellsPerBlock", "Cells per block", self.arrayString([2, 2]), type=self.intArrayType),
            ],
        ]

        self.line()

        self.title("Neighbour")
        self.input("neighbourChangesBoundsMin", "Minimum change", 1, type=int)
        self.input("neighbourChangesBoundsMax", "Maximum change", 1, type=int)

        self.title("Position")
        self.select("position", "Method", ["Random", "Grid", "Snake"], subSettings=True)
        self.positionSettings = [
            [ ],
            [
                self.input("gridPositionSize", "Grid size", 20, type=int),
                self.input("gridPositionMaxSameCount", "Steps to switch", 100, type=int),
                self.input("gridPositionWalkChance", "Random pixels between steps", 5, type=int)
            ],
            [ self.input("snakePositionWalkChance", "Random pixels between steps", 5, type=int) ],
        ]
        self.line()


        self.newColumn()

        self.title("Color")
        self.select("color", "Method", ["Random", "Copy", "Norm Copy"], subSettings=True)
        self.colorSettings = [
            [ ],
            [
                self.input("copyColorCopyChance", "Chance of copy", 0.5),
                self.input("copyColorMaxDiff", "Color neighbour difference", 0.1)
            ],
            [
                self.input("normCopyColorCopyChance", "Chance of copy", 0.5),
                self.input("normCopyColorMaxDiff", "Color neighbour difference", 0.03)
            ],
        ]
        self.line()


        self.title("Filler")
        self.select("filler", "Method", ["Quick", "Shape"], subSettings=True, command=self.onFillerChange)

        quickFillerSettings = [
            self.input("quickFillerBoundsMin", "Rectangle min size", 1, type=int),
            self.input("quickFillerBoundsMax", "Rectangle max size", 16, type=int),
        ]

        shapeFillerRectangle = self.select("shapeFillerRectangle", "Rectangle", ["No", "Yes"], subSettings=True)
        self.shapeFillerRectangleSettings = [
            [ ],
            [
                self.input("shapeFillerRectangleMin", "Min size", 1, type=int),
                self.input("shapeFillerRectangleMax", "Max size", 15, type=int),
            ],
        ]

        shapeFillerCircle = self.select("shapeFillerCircle", "Circle", ["No", "Yes"], subSettings=True)
        self.shapeFillerCircleSettings = [
            [ ],
            [
                self.input("shapeFillerCircleMin", "Min size", 2, type=int),
                self.input("shapeFillerCircleMax", "Max size", 7, type=int),
            ],
        ]

        shapeFillerRoundedRectangle = self.select("shapeFillerRoundedRectangle", "Rounded rectangle", ["No", "Yes"], subSettings=True)
        self.shapeFillerRoundedRectangleSettings = [
            [ ],
            [
                self.input("shapeFillerRoundedRectangleMin", "Min size", 2, type=int),
                self.input("shapeFillerRoundedRectangleMax", "Max size", 7, type=int),
            ],
        ]

        shapeFillerTriangle = self.select("shapeFillerTriangle", "Triangle", ["No", "Yes"], subSettings=True)
        self.shapeFillerTriangleSettings = [
            [ ],
            [
                self.input("shapeFillerTriangleMin", "Min size", 3, type=int),
                self.input("shapeFillerTriangleMax", "Max size", 15, type=int),
            ],
        ]

        self.fillerSettings = [
            quickFillerSettings,
            [
                shapeFillerRectangle,
                shapeFillerCircle,
                shapeFillerRoundedRectangle,
                shapeFillerTriangle,
            ]
        ]

        self.line()
        self.submitButton()

    def goodValueType(self, value):
        t = self.descriptor.get()
        # print(t)
        return self.floatArrayType(value)
        # if t == "Lbp" or t == "Coocc" or t == "Gabor":
        # return float(value)

    def goodValueString(self):
        re = 0
        if self.settings is not None and 'descriptor' in self.settings:
            re = self.goodCostValue.get()
            t = self.descriptor.get()
            if t == "Lbp" or t == "Coocc" or t == "Gabor":
                return re.join(map(str, self.app.grayScale))
            else:
                return re
        return re

    def onFillerChange(self, val):
        self.hide(self.fillerSettings)
        if val == 'Shape':
            self.show(self.fillerSettings[1])
            self.initSubSettings(startswith="shapeFiller")
        else:
            self.show(self.fillerSettings[0])
            self.hide(self.shapeFillerRectangleSettings)
            self.hide(self.shapeFillerCircleSettings)
            self.hide(self.shapeFillerRoundedRectangleSettings)
            self.hide(self.shapeFillerTriangleSettings)

    def getValues(self):
        imageSize = int(self.imageSize.get())
        values = {
            'colorStartShape': (imageSize, imageSize),
            'randomStartShape': (imageSize, imageSize),
            'imageStartShape': (imageSize, imageSize),
        }
        return super().getValues(values)

    def onSubmit(self):
        values = self.getValues()

        if self.window.app.applySettings(values):
            self.window.app.settingsStatus = "Set"
            self.window.updateImageStatus()
            self.window.updateSettingsStatus()

            self.window.app.startAnnealing()
            self.window.setActiveSite(annealing.Annealing)
