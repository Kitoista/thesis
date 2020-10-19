import tkinter as tk
from . import defaults, assets
from .components import menu, site
from .components.sites import gallery

class Window:
    title = "Képrekonstrukció textúrainformációk figyelembe vételével"
    activeSite = None

    def __init__(self, app):
        self.app = app
        self.menu = menu.Menu(self)
        self.assets = assets.AssetLoader()

    def open(self):
        self.gui = tk.Tk()
        self.gui.title(self.title)
        self.gui.geometry("{}x{}".format(defaults.size["width"], defaults.size["height"]))

        self.menu.generate()
        self.generateSiteFrame()
        self.generateBottomFrame()

        self.gui.mainloop()

    def generateSiteFrame(self):
        self.siteFrame = tk.Frame(self.gui)
        self.siteFrame.pack(side = tk.TOP, anchor = tk.NW)
        self.activeSite = site.Site(self)
        self.activeSite.activate()

    def setActiveSite(self, siteClass):
        if not isinstance(self.activeSite, siteClass):
            self.activeSite = siteClass(self)
            self.activeSite.activate()

    def generateBottomFrame(self):
        self.bottomFrame = tk.Frame(self.gui)
        self.bottomFrame.pack(side = tk.BOTTOM, anchor = tk.SE)

        tk.Label(self.bottomFrame, text = "made by: Krisztián Tóth", fg = "#555555").pack()
