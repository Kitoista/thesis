import tkinter as tk
from .. import assets, event, defaults
from . import imageLabel
from .sites import settings, annealing

class Status:
    def __init__(self, window):
        self.window = window

    def generate(self):
        self.container = tk.Frame(self.window.topFrame)

        self.column = 0

        self.imageStatusFrame = tk.Frame(self.container)
        self.formatStatus(self.imageStatusFrame)
        self.redrawImageStatus()
        self.imageStatusFrame.grid(row = 0, column = self.column)
        self.column = self.column + 1

        self.settingsStatusFrame = tk.Frame(self.container)
        self.formatStatus(self.settingsStatusFrame)
        self.redrawSettingsStatus()
        self.settingsStatusFrame.grid(row = 0, column = self.column)
        self.column = self.column + 1


        self.runningStatusFrame = tk.Frame(self.container)
        self.formatStatus(self.runningStatusFrame)
        self.redrawRunningStatus()
        self.runningStatusFrame.grid(row = 0, column = self.column)
        self.column = self.column + 1

        self.container.pack(side = tk.TOP)

    def onEvent(self, e):
        if isinstance(e, event.ImagesUpdateEvent):
            self.redrawImageStatus()
        elif isinstance(e, event.SettingsUpdatedEvent):
            self.redrawSettingsStatus()

    def formatStatus(self, frame):
        frame.config(highlightbackground = defaults.lightgray)
        frame.config(highlightthickness = 1)

    def redrawImageStatus(self):
        for child in self.imageStatusFrame.winfo_children():
            child.destroy()
        label = tk.Label(self.imageStatusFrame, text = "  " + str(len(self.window.app.images)) + " image(s) loaded  ")
        if len(self.window.app.images) > 0:
            label.config(bg = defaults.lightgreen)
        else:
            label.config(bg = defaults.red)
        label.bind('<Button-1>', self.window.openImages)
        label.pack()

    def redrawSettingsStatus(self):
        for child in self.settingsStatusFrame.winfo_children():
            child.destroy()

        settingsStatusText = "Unset"
        if self.window.app.settingsStatus:
            settingsStatusText = "Set"

        label = tk.Label(self.settingsStatusFrame, text = "  Settings status: " + settingsStatusText + "  ")
        if self.window.app.settingsStatus:
            label.config(bg = defaults.lightgreen)
        else:
            label.config(bg = defaults.red)

        label.bind('<Button-1>', lambda x: self.window.setActiveSite(settings.Settings))
        label.pack()

    def redrawRunningStatus(self):
        for child in self.runningStatusFrame.winfo_children():
            child.destroy()

        runningStatusText = "Not running"
        if self.window.app.runningStatus:
            runningStatusText = "Running"

        label = tk.Label(self.runningStatusFrame, text = "  " + runningStatusText + "  ")
        if self.window.app.runningStatus:
            label.config(bg = defaults.lightgreen)
        else:
            label.config(bg = defaults.red)

        label.bind('<Button-1>', lambda x: self.window.setActiveSite(annealing.Annealing))
        label.pack()
