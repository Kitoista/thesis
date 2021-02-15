
class Application:
    __instance = None

    def __init__(self):
        self.images = []
        self.settingsStatus = None
        self.runningStatus = None

        self.lambdaValue = None


        self.theta = 32
        self.minAngle = 0
        self.maxAngle = 180


    def getInstance():
        if Application.__instance is None:
            Application.__instance = Application()

        return Application.__instance

app = Application.getInstance()
