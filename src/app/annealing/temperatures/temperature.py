import math

class Temperature:
    def __init__(self, start, alpha):
        self.start = start
        self.alpha = alpha
        pass

    def __call__(self, step):
        T = self.start - (self.alpha * step)
        if T <= 0:
            return self.alpha / 2
        return T

    def probability(self, T):
        return math.exp(-1/T)
