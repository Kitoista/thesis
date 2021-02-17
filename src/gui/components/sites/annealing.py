import tkinter as tk
import numpy as np
from ... import assets, defaults
from .. import site, imageLabel
from app.error import rms
from ...event import ShowEvent, OriginalUpdateEvent

class Annealing(site.Site):
    def generateContent(self):
        self.original=None
        self.originalRadon=None

        self.workFrame = tk.Frame(self.content)
        self.workFrame.pack(side = tk.TOP, anchor = tk.NW)

        # containers
        self.logFrame = tk.Frame(self.workFrame)
        self.logFrame.grid(row = 0, column = 0)

        self.pictureFrame = tk.Frame(self.workFrame)
        self.pictureFrame.grid(row = 1, column = 0)

        # log
        self.logText = tk.StringVar()
        self.logText.set("-- log comes here --")
        self.logLabel = tk.Label(self.logFrame, textvariable = self.logText)
        self.logLabel.grid(row = 0, column = 0)

        # pictures
        self.originalFrame = tk.Frame(self.pictureFrame)
        self.originalFrame.grid(row = 0, column = 0)

        self.originalRadonFrame = tk.Frame(self.pictureFrame)
        self.originalRadonFrame.grid(row = 0, column = 1)

        self.reconFrame = tk.Frame(self.pictureFrame)
        self.reconFrame.grid(row = 0, column = 2)

        self.reconRadonFrame = tk.Frame(self.pictureFrame)
        self.reconRadonFrame.grid(row = 0, column = 3)


        self.diffFrame = tk.Frame(self.pictureFrame)
        self.diffFrame.grid(row = 0, column = 4)

        self.img_original = imageLabel.ImageLabel(self.originalFrame, icon = assets.placeholder)
        self.img_original.pack()
        self.img_originalRadon = imageLabel.ImageLabel(self.originalRadonFrame, icon = assets.placeholder)
        self.img_originalRadon.pack()
        self.img_recon = imageLabel.ImageLabel(self.reconFrame, icon = assets.placeholder)
        self.img_recon.pack()
        self.img_reconRadon = imageLabel.ImageLabel(self.reconRadonFrame, icon = assets.placeholder)
        self.img_reconRadon.pack()
        self.img_diff = imageLabel.ImageLabel(self.diffFrame, icon = assets.placeholder)
        self.img_diff.pack()

        self.setOriginal(self.original, self.originalRadon)

    def onEvent(self, e):
        if isinstance(e, ShowEvent):
            self.update(e.recon, e.reconRadon, e.step, e.cost)
        if isinstance(e, OriginalUpdateEvent):
            self.setOriginal(e.original, e.originalRadon)

    def setOriginal(self, original, originalRadon):
        self.original = original
        self.originalRadon = originalRadon
        self.replaceImage(self.img_original, self.originalFrame, original)
        self.replaceImage(self.img_originalRadon, self.originalRadonFrame, originalRadon)

    def update(self, recon, reconRadon, step, cost):
        self.replaceImage(self.img_recon, self.reconFrame, recon)
        self.replaceImage(self.img_reconRadon, self.reconRadonFrame, reconRadon)
        diff = self.original - recon
        self.replaceImage(self.img_diff, self.diffFrame, diff)

        error = rms.error(self.original, recon)

        self.logText.set(f"#{step+1} cost: {cost:.3g} error: {error:.3g}")

    def replaceImage(self, image, frame, icon):
        if icon is not None:
            newImage = assets.loadImage(icon)
            image.configure(image=newImage)
            image.image = newImage
