import tkinter as tk
import threading
from . import defaults, assets, event
from .components import menu, site, status
from .components.sites import gallery, settings
from app import radon, imageLib

class Window(threading.Thread):
    title = "Képrekonstrukció textúrainformációk figyelembe vételével"
    activeSite = None

    def init(self, app):
        self.app = app
        # self.menu = menu.Menu(self)
        self.status = status.Status(self)

    def run(self):
        self.gui = tk.Tk()
        self.gui.title(self.title)
        self.gui.geometry("{}x{}".format(defaults.size["width"], defaults.size["height"]))

        # self.menu.generate()
        self.generateTopFrame()
        self.generateSiteFrame()
        self.generateBottomFrame()

        self.status.generate()

        self.gui.mainloop()

    def generateSiteFrame(self):
        self.siteFrame = tk.Frame(self.gui)
        self.siteFrame.pack(side = tk.TOP, anchor = tk.NW)
        self.activeSite = settings.Settings(self)
        self.activeSite.activate()

    def setActiveSite(self, siteClass):
        if not isinstance(self.activeSite, siteClass):
            self.activeSite = siteClass(self)
            self.activeSite.activate()

    def generateBottomFrame(self):
        self.bottomFrame = tk.Frame(self.gui)
        self.bottomFrame.pack(side = tk.BOTTOM, anchor = tk.SE)

        tk.Label(self.bottomFrame, text = "made by: Krisztián Tóth", fg = defaults.gray).pack()

    def generateTopFrame(self):
        self.topFrame = tk.Frame(self.gui, width = defaults.size["width"])
        self.topFrame.pack(side = tk.TOP, anchor = tk.NW)

    def openImage(self, *args):
        image = assets.getImage()
        if image:
            self.app.image = assets.loadImage(image)
            # print(self.app.image)
            self.triggerEvent(event.ImageUpdatedEvent())

    def updateImageStatus(self):
        self.triggerEvent(event.ImageUpdatedEvent())

    def updateSettingsStatus(self):
        self.triggerEvent(event.SettingsUpdatedEvent())

    def updateRunningStatus(self):
        self.triggerEvent(event.RunningUpdatedEvent())

    def updateSaveStatus(self):
        self.triggerEvent(event.SaveUpdatedEvent())

    def triggerEvent(self, e):
        self.status.onEvent(e)
        if self.activeSite is not None:
            self.activeSite.onEvent(e)
