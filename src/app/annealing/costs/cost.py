import numpy as np
import math
import time

from ... import radon
from ...error import error
from .descriptors.descriptor import Descriptor

class Cost:
    def __init__(self, goodValue, l, kappa):
        self.sinogram = None
        self.theta = None
        self.angleBounds = (0., 180.)
        self.descriptor = Descriptor()
        self.goodValue = goodValue
        self.l = l
        self.kappa = kappa
        self.maxT = None

    def __call__(self, state, T):
        if self.maxT is None:
            self.maxT = T

        timestamps = []
        timestamps.append(time.time())

        stateRadonTrans = radon.Radon(state, self.theta, self.angleBounds)
        timestamps.append(time.time())

        stateSinogram = stateRadonTrans.transform()
        timestamps.append(time.time())

        sin_error = error.rms(self.sinogram, stateSinogram)
        timestamps.append(time.time())

        desc = self.descriptor(state)
        timestamps.append(time.time())

        desc_error = self.descriptor.compare(self.goodValue, desc)
        timestamps.append(time.time())

        desc_str = desc
        if isinstance(desc, np.ndarray):
            desc_str = np.array_str(desc, precision = 3, suppress_small = True)

        l = self.l[0] + (self.l[1] - self.l[0]) * (self.maxT - T) / self.maxT

        sin_val = (100-l)*sin_error / 100
        desc_val = l*desc_error / 100 * self.kappa
        val = (sin_val + desc_val)
        timestamps.append(time.time())

        timediffs = []
        for i in range(len(timestamps)):
            if i == 0:
                continue
            timediffs.append("{:.4f}".format(timestamps[i] - timestamps[i-1]))

        return val, f"[l: {l:.3g}, ({(100-l):.3g}% {sin_error:.3g} + {l:.3g}% {desc_error:.3g} * {self.kappa} | {sin_val:.3g} + {desc_val:.3g} = {val:.3g}]"

# 0.017 0.01 0.002 0.003 0.027 0.044 0.013 0.008 0.006 0.85 0.021
# 0.02 0.01 0 0 0.03 0.04 0.01 0.01 0.01 0.85 0.02
# 0 0 0 0 0 0 0 0 0 1 0
