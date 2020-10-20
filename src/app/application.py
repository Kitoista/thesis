
class Application:
    _images = []
    @property
    def images(self):
        return self._images
    @images.setter
    def images(self, value):
        self._images = value

    _settingsStatus = None
    @property
    def settingsStatus(self):
        return self._settingsStatus
    @settingsStatus.setter
    def settingsStatus(self, value):
        self._settingsStatus = value

    _runningStatus = None
    @property
    def runningStatus(self):
        return self._runningStatus
    @runningStatus.setter
    def runningStatus(self, value):
        self._runningStatus = value


    _lambdaValue = None
    @property
    def lambdaValue(self):
        return self._lambdaValue
    @lambdaValue.setter
    def lambdaValue(self, value):
        self._lambdaValue = value



    # def __init__(self):
