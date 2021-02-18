from ... import radon
from ...error import rms

class Cost:
    def __init__(self):
        self.sinogram = None
        self.theta = None

    def __call__(self, state):
        stateRadonTrans = radon.Radon(state, self.theta)
        stateSinogram = stateRadonTrans.transform()

        sin_error = rms.error(self.sinogram, stateSinogram)

        return sin_error
