import tkinter as tk
from tkinter import ttk
import re

from .. import assets
from .site import Site

class FormSite(Site):

    def initForm(self, container, side = tk.LEFT):
        self.formFrame = tk.Frame(container)
        self.formFrame.pack(side = side, anchor = tk.NW)

        self.formColumns = []
        self.formColumn = None
        self.formRow = 0

        self.settings = []
        self.subSettings = {}
        self.values = {}

        self.newColumn()
        self.generateForm()
        self.initSubSettings()

    def generateForm(self):
        pass

    def newColumn(self):
        if len(self.formColumns) > 0:
            self.verticalLine()
        self.formColumn = tk.Frame(self.formFrame)
        self.formColumn.grid(row = 0, column = len(self.formColumns), sticky="nsew")
        self.formColumn.grid_columnconfigure(0, minsize=220)
        self.formColumns.append(self.formColumn)

    def addSubSettings(self, attr, options, command=None):
        def func(val):
            settings = getattr(self, attr + "Settings")
            if val != 'None':
                index = options.index(val)
            else:
                index = 0
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
        self.formRow += 1

    def line(self, pady=10):
        separator = ttk.Separator(self.formColumn, orient='horizontal')
        separator.grid(row = self.formRow, column = 0, columnspan = 2, pady=(pady, pady), sticky="ew")
        self.formRow += 1

    def verticalLine(self, padx=10):
        separator = ttk.Separator(self.formColumn, orient='vertical')
        separator.grid(row = 0, rowspan = self.formRow + 1, column = 2, padx=(padx, padx), sticky="ns")
        self.formRow = 0

    def select(self, attr, name, options, command = None, subSettings = False, type=str):
        label = self.labelFor(name)

        value = options[0]
        if self.values is not None and attr in self.values:
            value = self.values[attr]

        var = tk.StringVar(self.formColumn)
        var.set(value)

        if subSettings:
            command = self.addSubSettings(attr, options, command=command)
        select = tk.OptionMenu(self.formColumn, var, *options, command = command)
        select.config(width = 20)
        select.grid(row = self.formRow, column = 1)

        self.formRow += 1
        setattr(self, attr, var)
        setattr(self, '_' + attr, select)
        setattr(self, '_l_' + attr, label)
        setattr(self, '_t_' + attr, type)
        self.settings.append(attr)
        return attr

    def input(self, attr, name, value, type=float):
        label = self.labelFor(name)

        if self.values is not None and attr in self.values:
            value = self.values[attr]

        var = tk.StringVar(self.formColumn)

        input = tk.Entry(self.formColumn, textvariable=var)
        input.config(width = 24)
        if value is not None:
            var.set(value)
        input.grid(row = self.formRow, column = 1)

        # if attr == 'costGoodValue':
        #     print(value)

        self.formRow += 1
        setattr(self, attr, var)
        setattr(self, '_' + attr, input)
        setattr(self, '_l_' + attr, label)
        setattr(self, '_t_' + attr, type)
        self.settings.append(attr)
        return attr

    def imageLoader(self, attr, name, value='', type=str):
        label = self.labelFor(name)

        if self.values is not None and attr in self.values:
            value = self.values[attr]

        var = tk.StringVar(self.formColumn)
        var.set(value)

        visible = tk.StringVar(self.formColumn)
        visibleValue = ''
        if value == '':
            visibleValue = '-- click here to load image --'
        else:
            parts = value.split(self.window.app.separator)
            visibleValue = parts[len(parts) - 1]

        visible.set(visibleValue)

        imageLoader = tk.Label(self.formColumn, textvariable = visible)
        imageLoader.bind("<Button-1>", lambda e: self.imageLoaderCommand(var, visible))
        imageLoader.grid(row = self.formRow, column = 1)

        self.formRow += 1
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

    def labelFor(self, name, ending = ": ", columnspan = None, pady = (0, 0)):
        label = tk.Label(self.formColumn, text = name + ending)
        label.grid(row = self.formRow, column = 0, columnspan = columnspan, pady = pady)
        return label

    def submitButton(self):
        btn = tk.Button(self.formColumn, text = 'Submit', command = self.onSubmit)
        btn.grid(row = self.formRow, column = 1)
        return btn

    def arrayString(self, arr):
        return " ".join(map(str, arr))

    def arrayType(self, x, t):
        return [t(i) for i in x.strip('(').strip(')').replace(',', '').split(' ')]

    def floatArrayType(self, x):
        return self.arrayType(x, float)

    def intArrayType(self, x):
        return self.arrayType(x, int)

    def getValues(self, values = {}):
        for attr in self.settings:
            formColumn = getattr(self, attr)
            convertTo = getattr(self, '_t_' + attr)
            value = formColumn.get()
            values[attr] = convertTo(value)
        return values

    def refreshValues(self):
        self.formFrame.destroy()
        self.generateContent()
