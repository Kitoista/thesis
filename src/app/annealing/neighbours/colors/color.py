import random

class Color:
    def __init__(self):
        pass

    def __call__(self, state, pos):
        return random.uniform(0, 1)
