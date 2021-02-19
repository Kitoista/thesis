from ... import radon
from ...error import rms

class Cost:
    def __init__(self):
        self.sinogram = None
        self.theta = None
        self.angleBounds = (0., 180.)

    def __call__(self, state):
        stateRadonTrans = radon.Radon(state, self.theta, self.angleBounds)
        stateSinogram = stateRadonTrans.transform()

        sin_error = rms.error(self.sinogram, stateSinogram)

        return sin_error
