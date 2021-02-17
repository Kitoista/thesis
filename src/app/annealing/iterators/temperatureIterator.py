from .iterator import Iterator

class TemperatureIterator(Iterator):
    def __init__(self, tEnd):
        self.tEnd = tEnd

    def __call__(self, step, cost, T):
        return T > self.tEnd
