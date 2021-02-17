import math
import random

class Accept:
    def __init__(self):
        pass

    def __call__(self, cost, newCost, T):
        diff = cost - newCost

        if diff > 0:
            return True

        return random.uniform(0, 1) < math.exp(diff / (T / 100))
