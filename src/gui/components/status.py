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

        self.loadFrame = tk.Frame(self.container)
        self.formatStatus(self.loadFrame)
        self.drawLoad()
        self.loadFrame.grid(row = 0, column = self.column)
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


        self.killFrame = tk.Frame(self.container)
        self.formatStatus(self.killFrame)
        self.drawKill()
        self.killFrame.grid(row = 0, column = self.column)
        self.column = self.column + 1


        self.saveStatusFrame = tk.Frame(self.container)
        self.formatStatus(self.saveStatusFrame)
        self.redrawSaveStatus()
        self.saveStatusFrame.grid(row = 0, column = self.column)
        self.column = self.column + 1


        self.testFrame = tk.Frame(self.container)
        self.formatStatus(self.testFrame)
        self.drawTest()
        self.testFrame.grid(row = 0, column = self.column)
        self.column = self.column + 1

        self.container.pack(side = tk.TOP)

    def onEvent(self, e):
        if isinstance(e, event.SettingsUpdatedEvent):
            self.redrawSettingsStatus()
        elif isinstance(e, event.RunningUpdatedEvent):
            self.redrawRunningStatus()
        elif isinstance(e, event.SaveUpdatedEvent):
            self.redrawSaveStatus()

    def formatStatus(self, frame):
        frame.config(highlightbackground = defaults.lightgray)
        frame.config(highlightthickness = 1)

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

    def drawKill(self):
        killText = "Kill"

        label = tk.Label(self.killFrame, text = "  " + killText + "  ")
        label.config(bg = defaults.lightblue)

        label.bind('<Button-1>', lambda x: self.window.app.killAnnealing())
        label.pack()

    def redrawSaveStatus(self):
        for child in self.saveStatusFrame.winfo_children():
            child.destroy()

        saveText = "Save"

        label = tk.Label(self.saveStatusFrame, text = "  " + saveText + "  ")
        if self.window.app.saveStatus:
            label.config(bg = defaults.lightgreen)
            label.bind('<Button-1>', lambda x: self.window.app.save())
        else:
            label.config(bg = defaults.red)

        label.pack()

    def drawLoad(self):
        loadText = "Load"

        label = tk.Label(self.loadFrame, text = "  " + loadText + "  ")
        label.config(bg = defaults.lightblue)

        label.bind('<Button-1>', lambda x: self.window.app.load())
        label.pack()

    def drawTest(self):
        testText = "Test"

        label = tk.Label(self.testFrame, text = "  " + testText + "  ")
        label.config(bg = defaults.lightblue)

        label.bind('<Button-1>', lambda x: self.window.app.test())
        label.pack()
