from .iterator import Iterator
import math

class CostIterator:
    def __init__(self, value):
        self.value = value

    def __call__(self, step, cost, T):
        return cost > self.value
