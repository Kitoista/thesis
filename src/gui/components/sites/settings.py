import tkinter as tk
from tkinter import ttk
import re

from ... import assets, defaults
from .. import site, imageLabel
from . import annealing

class Settings(site.Site):

    def generateContent(self):
        self.workFrame = tk.Frame(self.content)
        self.workFrame.pack(side = tk.TOP, anchor = tk.NW)

        self.containers = []
        self.container = None
        self.row = 0

        self.settings = []
        self.subSettings = {}


        self.newColumn()

        self.title("Image")
        self.imageLoader("imagePath", "Path")
        self.input("imageSize", "Size", self.app.imageSize, type=int)

        self.line()

        self.title("Radon")
        self.input("theta", "Theta", self.app.theta, type=int)
        self.input("radonAngleBoundsMin", "Angle start", self.app.radonAngleBounds[0], type=int)
        self.input("radonAngleBoundsMax", "Angle end", self.app.radonAngleBounds[1], type=int)
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


        self.newColumn()


        self.title("Cost")
        self.select("cost", "Method", ["Sinogram RMS", "Homogenity"], subSettings=True)
        self.costSettings = [
            [ ],
            [
                self.input("homogenityCostCount", "Same count", 100, type=int),
                self.input("homogenityCostLambda", "Lambda", 0.01)
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


        self.newColumn()


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
                self.input("shapeFillerRectangleMax", "Max size", 16, type=int),
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
                self.input("shapeFillerTriangleMin", "Min size", 5, type=int),
                self.input("shapeFillerTriangleMax", "Max size", 12, type=int),
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


        self.initSubSettings()
        self.submit = self.submitButton()

    def newColumn(self):
        if len(self.containers) > 0:
            self.verticalLine()
        self.container = tk.Frame(self.workFrame)
        self.container.grid(row = 0, column = len(self.containers), sticky="nsew")
        self.container.grid_columnconfigure(0, minsize=220)
        self.containers.append(self.container)

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

    def addSubSettings(self, attr, options, command=None):
        def func(val):
            settings = getattr(self, attr + "Settings")
            index = options.index(val)
            self.hide(settings)
            self.show(settings[index])
            if command is not None:
                command(val)
        self.subSettings[attr] = {
            'options': options,
            'command': func
        }
        return func

    def initSubSettings(self, startswith=""):
        for attr in self.subSettings:
            if attr.startswith(startswith):
                self.subSettings[attr]['command'](getattr(self, attr).get())

    def hide(self, attr):
        if isinstance(attr, list):
            for x in attr:
                self.hide(x)
        else:
            getattr(self, '_' + attr).grid_remove()
            getattr(self, '_l_' + attr).grid_remove()

    def show(self, attr):
        if isinstance(attr, list):
            for x in attr:
                self.show(x)
        else:
            getattr(self, '_' + attr).grid()
            getattr(self, '_l_' + attr).grid()

    def title(self, name):
        self.labelFor(name, ending="", columnspan=2, pady=(5, 10))
        self.row += 1

    def line(self, pady=10):
        separator = ttk.Separator(self.container, orient='horizontal')
        separator.grid(row = self.row, column = 0, columnspan = 2, pady=(pady, pady), sticky="ew")
        self.row += 1

    def verticalLine(self, padx=10):
        separator = ttk.Separator(self.container, orient='vertical')
        separator.grid(row = 0, rowspan = self.row + 1, column = 2, padx=(padx, padx), sticky="ns")
        self.row = 0

    def select(self, attr, name, options, command = None, subSettings = False, type=str):
        label = self.labelFor(name)

        value = options[0]
        if self.app.settings is not None:
            value = self.app.settings[attr]

        var = tk.StringVar(self.container)
        var.set(value)

        if subSettings:
            command = self.addSubSettings(attr, options, command=command)
        select = tk.OptionMenu(self.container, var, *options, command = command)
        select.config(width = 20)
        select.grid(row = self.row, column = 1)

        self.row += 1
        setattr(self, attr, var)
        setattr(self, '_' + attr, select)
        setattr(self, '_l_' + attr, label)
        setattr(self, '_t_' + attr, type)
        self.settings.append(attr)
        return attr

    def input(self, attr, name, value, type=float):
        label = self.labelFor(name)

        if self.app.settings is not None:
            value = self.app.settings[attr]

        input = tk.Entry(self.container)
        input.config(width = 24)
        if value is not None:
            input.insert(0, value)
        input.grid(row = self.row, column = 1)

        self.row += 1
        setattr(self, attr, input)
        setattr(self, '_' + attr, input)
        setattr(self, '_l_' + attr, label)
        setattr(self, '_t_' + attr, type)
        self.settings.append(attr)
        return attr

    def imageLoader(self, attr, name, value='', type=str):
        label = self.labelFor(name)

        if self.app.settings is not None:
            value = self.app.settings[attr]

        var = tk.StringVar(self.container)
        var.set(value)

        visible = tk.StringVar(self.container)
        visibleValue = ''
        if value == '':
            visibleValue = '-- click here to load image --'
        else:
            parts = value.split(self.window.app.separator)
            visibleValue = parts[len(parts) - 1]

        visible.set(visibleValue)

        imageLoader = tk.Label(self.container, textvariable = visible)
        imageLoader.bind("<Button-1>", lambda e: self.imageLoaderCommand(var, visible))
        imageLoader.grid(row = self.row, column = 1)

        self.row += 1
        setattr(self, attr, var)
        setattr(self, '_' + attr, imageLoader)
        setattr(self, '_l_' + attr, label)
        setattr(self, '_t_' + attr, type)
        self.settings.append(attr)
        return attr

    def imageLoaderCommand(self, target, visible):
        path = assets.getImage()
        if len(path) == 0:
            return
        target.set(path)
        parts = re.split('/', path)
        visible.set(parts[len(parts) - 1])
        return path

    def changeInputValue(self, attr, value):
        getattr(self, attr).delete(0, tk.END)
        getattr(self, attr).insert(0, value)

    def labelFor(self, name, ending = ": ", columnspan = None, pady = (0, 0)):
        label = tk.Label(self.container, text = name + ending)
        label.grid(row = self.row, column = 0, columnspan = columnspan, pady = pady)
        return label

    def submitButton(self):
        btn = tk.Button(self.container, text = 'Submit', command = self.setValues)
        btn.grid(row = self.row, column = 1)
        return btn

    def setValues(self):
        imageSize = int(self.imageSize.get())
        values = {
            'colorStartShape': (imageSize, imageSize),
            'randomStartShape': (imageSize, imageSize),
            'imageStartShape': (imageSize, imageSize),
        }
        for attr in self.settings:
            container = getattr(self, attr)
            convertTo = getattr(self, '_t_' + attr)
            value = container.get()
            values[attr] = convertTo(value)

        if self.window.app.applySettings(values):
            self.window.app.settingsStatus = "Set"
            self.window.updateImageStatus()
            self.window.updateSettingsStatus()

            self.window.app.startAnnealing()
            self.window.setActiveSite(annealing.Annealing)
