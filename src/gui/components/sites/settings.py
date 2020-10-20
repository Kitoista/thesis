import tkinter as tk
from ... import assets, defaults
from .. import site, imageLabel

class Settings(site.Site):

    def generateContent(self):
        self.row = 0

        self.settings = []

        self.select("textureMethod", "Textura descriptor", ["one", "two", "three"])
        self.input("lambdaValue", "Textura descriptor lambda", 12)

        self.input("lambdaValue", "Projection's count", 8)

        self.select("saStoppingCriteria", "Stopping criteria", ["Diff is less than", "Temperature is less than", "Max iteration count"],
            self.saStoppingCriteriaChange)
        self.input("saStoppingCriteriaParam", "Stopping criteria param", 0.0001)
        self.input("saTemperature", "Temperature", 30)
        self.select("startPictureMode", "Start", ["Random", "Continuous reconstructed"])

        self.submit = self.submitButton()

    def saStoppingCriteriaChange(self, val):
        if val == "Max iteration count":
            self.changeInputValue("saStoppingCriteriaParam", 1000)
        elif val == "Diff is less than":
            self.changeInputValue("saStoppingCriteriaParam", 0.0001)
        else:
            self.changeInputValue("saStoppingCriteriaParam", 0.1)

    def select(self, attr, name, options, command = None):
        self.labelFor(name)

        var = tk.StringVar(self.content)
        var.set(options[0])

        select = tk.OptionMenu(self.content, var, *options, command = command)
        select.config(width = 20)
        select.grid(row = self.row, column = 1)

        self.row = self.row + 1
        setattr(self, attr, var)
        self.settings.append(attr)

    def input(self, attr, name, value):
        self.labelFor(name)

        input = tk.Entry(self.content)
        input.config(width = 24)
        if value is not None:
            input.insert(0, value)
        input.grid(row = self.row, column = 1)

        self.row = self.row + 1
        setattr(self, attr, input)
        self.settings.append(attr)

    def changeInputValue(self, attr, value):
        getattr(self, attr).delete(0, tk.END)
        getattr(self, attr).insert(0, value)

    def labelFor(self, name):
        label = tk.Label(self.content, text = name + ": ")
        label.grid(row = self.row, column = 0)


    def submitButton(self):
        btn = tk.Button(self.content, text = 'Submit', command = self.setValues)
        btn.grid(row = self.row, column = 1)
        return btn

    def setValues(self):
        for attr in self.settings:
            setattr(self.window.app, attr, getattr(self, attr).get())

        self.window.app.settingsStatus = "Set"
        self.window.updateSettingsStatus()
