from .error import rms
from . import radon
from gui import event

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

        self.image = None

        self.debug = True
        self.debugBundles = 1000

        self.window = None
        self.showBundles = 10


    def getInstance():
        if Application.__instance is None:
            Application.__instance = Application()

        return Application.__instance

    def onAnnealingStep(self, state, step, cost, temperature, debugMessage, isLast):
        if self.debug and (step % self.debugBundles == 0 or isLast):
            print(f"Step #{(step + 1):>4g} : cost = {cost:>4.3g}, T = {temperature:>4.3g} ...  {debugMessage}")

        if self.window and step != 0 and (step % self.showBundles == 0 or isLast):
            stateRadonTrans = radon.Radon(state, self.theta)
            stateSinogram = stateRadonTrans.transform()
            error = rms.error(self.image, state)

            self.window.triggerEvent(event.ShowEvent(
                recon=state,
                reconRadon=stateSinogram,
                step=step,
                error=error,
                cost=cost,
            ))
        pass

app = Application.getInstance()
