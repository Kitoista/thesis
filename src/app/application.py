from datetime import datetime
import json
import platform
import numpy as np

from .error import error
from . import radon
from gui import event
from app import radon
import threading

from .imageLib import imageLib
from gui import assets

from gui.components.sites.settings import Settings as SettingsSite
from gui.components.sites.descriptors import Descriptors as DescriptorsSite

from app.annealing.annealing import Annealing
from app.annealing.accepts.accept import Accept

from app.annealing.temperatures.temperature import Temperature

from app.annealing.starts.colorStart import ColorStart
from app.annealing.starts.imageStart import ImageStart
from app.annealing.starts.randomStart import RandomStart

from app.annealing.iterators.constantIterator import ConstantIterator
from app.annealing.iterators.temperatureIterator import TemperatureIterator
from app.annealing.iterators.stepIterator import StepIterator
from app.annealing.iterators.costIterator import CostIterator

from app.annealing.costs.cost import Cost

from app.annealing.costs.descriptors.noneDescriptor import NoneDescriptor
from app.annealing.costs.descriptors.homogenityDescriptor import HomogenityDescriptor
from app.annealing.costs.descriptors.lbpDescriptor import LbpDescriptor
from app.annealing.costs.descriptors.cooccDescriptor import CooccDescriptor
from app.annealing.costs.descriptors.gaborDescriptor import GaborDescriptor
from app.annealing.costs.descriptors.hogDescriptor import HogDescriptor

from app.annealing.neighbours.neighbour import Neighbour

from app.annealing.neighbours.positions.randomPosition import RandomPosition
from app.annealing.neighbours.positions.gridPosition import GridPosition
from app.annealing.neighbours.positions.snakePosition import SnakePosition

from app.annealing.neighbours.colors.randomColor import RandomColor
from app.annealing.neighbours.colors.copyColor import CopyColor
from app.annealing.neighbours.colors.normCopyColor import NormCopyColor

from app.annealing.neighbours.fillers.filler import Filler
from app.annealing.neighbours.fillers.quickFiller import QuickFiller
from app.annealing.neighbours.fillers.shapeFiller import ShapeFiller

from app.annealing.neighbours.fillers.shapes.roundedRectangle import RoundedRectangle
from app.annealing.neighbours.fillers.shapes.circle import Circle
from app.annealing.neighbours.fillers.shapes.triangle import Triangle
from app.annealing.neighbours.fillers.shapes.rectangle import Rectangle


class Application:
    __instance = None

    classMap = {
        'temperature': Temperature,
        'colorStart': ColorStart,
        'imageStart': ImageStart,
        'randomStart': RandomStart,
        'constantIterator': ConstantIterator,
        'temperatureIterator': TemperatureIterator,
        'stepIterator': StepIterator,
        'costIterator': CostIterator,
        'cost': Cost,
        'homogenityDescriptor': HomogenityDescriptor,
        'noneDescriptor': NoneDescriptor,
        'lbpDescriptor': LbpDescriptor,
        'cooccDescriptor': CooccDescriptor,
        'gaborDescriptor': GaborDescriptor,
        'hogDescriptor': HogDescriptor,
        'neighbour': Neighbour,
        'randomPosition': RandomPosition,
        'gridPosition': GridPosition,
        'snakePosition': SnakePosition,
        'randomColor': RandomColor,
        'copyColor': CopyColor,
        'normCopyColor': NormCopyColor,
        'filler': Filler,
        'quickFiller': QuickFiller,
        'shapeFiller': ShapeFiller,
        'roundedRectangle': RoundedRectangle,
        'circle': Circle,
        'triangle': Triangle,
        'rectangle': Rectangle,
    }

    @property
    def theta(self):
        return self._theta
    @theta.setter
    def theta(self, value):
        self._theta = int(value)
        self.setSinogram()

    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, value):
        self._image = value
        self.setSinogram()

    @property
    def imageSize(self):
        return imageLib.imageSize
    @imageSize.setter
    def imageSize(self, value):
        if value != imageLib.imageSize:
            self.image = None
            self.lastShowEvent = None
            if self.window is not None:
                self.window.updateSaveStatus()
        imageLib.imageSize = value

    @property
    def grayScale(self):
        return imageLib.grayScale
    @grayScale.setter
    def grayScale(self, value):
        if not np.array_equal(value, imageLib.grayScale):
            self.image = None
            self.lastShowEvent = None
            if self.window is not None:
                self.window.updateSaveStatus()
        imageLib.grayScale = np.array(value)

    @property
    def grayScaleLength(self):
        return imageLib.grayScaleLength
    @grayScaleLength.setter
    def grayScaleLength(self, value):
        if value != imageLib.grayScaleLength:
            self.image = None
            self.lastShowEvent = None
            if self.window is not None:
                self.window.updateSaveStatus()
        imageLib.grayScaleLength = value

    @property
    def saveStatus(self):
        return self.lastShowEvent is not None

    def __init__(self):
        self.window = None
        self.images = []
        self.settingsStatus = None
        self.runningStatus = None
        self.annealingThread = None

        self.settings = None

        self._image = None
        self._theta = None

        self.imageSize = 160
        self.theta = 32
        self.radonAngleBounds = (0., 180.)

        self.annealing = None

        self.image = None
        self.sinogram = None

        self.debug = True
        self.debugBundles = 1000

        # self.grayScaleLenght = 256
        self.grayScale = np.array([0, 0.2, 0.3, 0.4, 1])
        self.showBundles = 10

        self.lastShowEvent = None
        self.debugHist = ''

        self.separator = '/'
        if platform.system() == 'Windows':
            self.separator = '\\'

    def setSinogram(self):
        if self.image is None or self.theta is None:
            self.sinogram = None
        else:
            radonTrans = radon.Radon(self.image, self.theta, self.radonAngleBounds)
            self.sinogram = radonTrans.transform()

    def getInstance():
        if Application.__instance is None:
            Application.__instance = Application()

        return Application.__instance

    def onAnnealingStep(self, state, step, cost, temperature, debugMessage, isLast):
        if self.debug and (step % self.debugBundles == 0 or isLast):
            entry = f"Step #{(step + 1):>4g} : cost = {cost:>4.3g}, T = {temperature:>4.3g} ...  {debugMessage}"
            print(entry)
            self.debugHist += entry + "\n"

        if self.window and step != 0 and (step % self.showBundles == 0 or isLast):
            err = error.rms(self.image, state)

            saveStatusUpade = self.saveStatus == False
            show = self.annealing.cost.descriptor.show(state)
            if show is None:
                stateRadonTrans = radon.Radon(state, self.theta, self.radonAngleBounds)
                show = stateRadonTrans.transform()

            self.lastShowEvent = event.ShowEvent(
                recon=state,
                reconRadon=show,
                step=step,
                error=err,
                cost=cost,
                startedAt=self.annealing.startedAt
            )
            self.window.triggerEvent(self.lastShowEvent)
            if saveStatusUpade:
                self.window.updateSaveStatus()
        pass

    def applySettings(self, settings):
        if self.annealing is not None and self.annealing.running:
            raise ValueError('Kill the previous run first!')

        def toClassKey(key):
            str = settings[key]
            first = str[:1].lower() + str[1:].replace(' ', '')
            second = key[:1].upper() + key[1:]
            return first + second

        self.settings = settings
        self.showBundles = settings['showBundles']
        self.theta = settings['theta']
        if settings['grayScaleType'] == 'List':
            self.grayScale = settings['grayScale']
        else:
            self.grayScaleLength = settings['grayScaleLength']
        self.radonAngleBounds = (settings['radonAngleBoundsMin'], settings['radonAngleBoundsMax'])
        self.imageSize = settings['imageSize']
        if settings['imagePath'] != '':
            self.image = assets.loadImage(settings['imagePath'])
        else:
            self.image = None

        self.debugHist = ''
        self.annealing = Annealing(self)
        self.annealing.threadPoolSize = settings['threadPoolSize']
        self.annealing.threadLength = settings['threadLength']
        self.annealing.accept = Accept()
        self.annealing.temperature = self.applyClass('temperature', settings)
        self.annealing.start = self.applyClass(toClassKey('start'), settings)
        self.annealing.iterator = self.applyClass(toClassKey('iterator'), settings)
        self.annealing.cost = self.applyClass('cost', settings)
        self.annealing.cost.descriptor = self.applyClass(toClassKey('descriptor'), settings)
        self.annealing.neighbour = self.applyClass('neighbour', settings)
        self.annealing.neighbour.position = self.applyClass(toClassKey('position'), settings)
        self.annealing.neighbour.color = self.applyClass(toClassKey('color'), settings)
        self.annealing.neighbour.filler = self.applyClass(toClassKey('filler'), settings)

        if self.sinogram is not None:
            return True
        return False

    def applyShapeFiller(self, c, settings):
        shapeClassesWithBounds = []

        shapes = ['Rectangle', 'Circle', 'RoundedRectangle', 'Triangle']

        for shape in shapes:
            if settings['shapeFiller' + shape] == 'Yes':
                shapeClass = Application.classMap[shape[:1].lower() + shape[1:]]
                shapeClassesWithBounds.append((shapeClass, (settings['shapeFiller' + shape + 'Min'], settings['shapeFiller' + shape + 'Max'])))

        if len(shapeClassesWithBounds) == 0:
            raise ValueError('Shape Filler has to have atleat one shape enabled!')

        filler = ShapeFiller(shapeClassesWithBounds)

        return filler

    def applyCooccDescriptor(self, c, settings):
        return CooccDescriptor(settings['cooccDescriptorDistances'], settings['cooccDescriptorAngles'], self.grayScale)

    def applyClass(self, c, settings):
        applyFunction = getattr(self, "apply" + c[:1].upper() + c[1:], None)
        if callable(applyFunction):
            return applyFunction(c, settings)

        args = []
        longers = []
        for c2 in Application.classMap:
            if c2.startswith(c) and c2 != c:
                longers.append(c2)
        for attr in settings:
            if attr.startswith(c):
                bad = False
                for c2 in longers:
                    if attr.startswith(c2):
                        bad = True
                if not bad:
                    if attr.endswith("Max"):
                        args[len(args) - 1] = (args[len(args) - 1], settings[attr])
                    else:
                        args.append(settings[attr])
        return Application.classMap[c](*args)

    def startAnnealing(self):
        if self.image is None:
            raise ValueError('Load an image first!')
        if self.annealing is None:
            raise ValueError('Submit the settings first!')

        self.runningStatus = True
        self.annealing.cost.sinogram = self.sinogram
        self.annealing.cost.theta = self.theta
        self.annealing.cost.angleBounds = self.radonAngleBounds

        self.annealingThread = threading.Thread(target=lambda x: self.annealing(), args=(1,))
        self.annealingThread.start()

        if self.window is not None:
            self.window.updateRunningStatus()
            self.window.updateSaveStatus()

    def killAnnealing(self):
        if self.annealing is None or not self.annealing.running:
            return
        self.annealing.running = False
        self.settingsStatus = False
        self.runningStatus = False

        if self.window is not None:
            self.window.updateSettingsStatus()
            self.window.updateRunningStatus()

    def save(self):
        if self.lastShowEvent is None:
            return

        img = imageLib.convertArrayToImage(self.lastShowEvent.recon)
        settings = json.dumps(self.settings)

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        img.save(filename + '.png')

        settingsFile = open(filename + '.json', 'w')
        settingsFile.write(settings)
        settingsFile.close()

        histFile = open(filename + '.hist', 'w')
        histFile.write(self.debugHist)
        histFile.close()


    def load(self, input=None):
        if input is None:
            input = assets.getJson()
        self.settings = json.loads(input)
        self.window.setActiveSite(SettingsSite)
        self.window.activeSite.refreshValues()

    def test(self):
        self.window.setActiveSite(DescriptorsSite)

app = Application.getInstance()
