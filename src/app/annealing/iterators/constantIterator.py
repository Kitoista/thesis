from .iterator import Iterator
import math

class ConstantIterator:
    def __init__(self, diff, overSteps):
        self.diff = diff
        self.overSteps = overSteps

        self.lastChangedStep = -1
        self.lastCost = math.inf

    def __call__(self, step, cost, T):
        if cost < self.lastCost - self.diff:
            self.lastCost = cost
            self.lastChangedStep = step
        if step - self.lastChangedStep >= self.overSteps:
            return False
        return True
