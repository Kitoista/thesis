from ... import radon

class Cost:
    def __init__(self, sinogram):
        self.sinogram = sinogram

    def cost(self, state):
        stateRadonTrans = radon.Radon(state, theta)
        stateSinogram = stateRadonTrans.transform()

        sin_error = rms.error(sinogram, stateSinogram)

        return sin_error
