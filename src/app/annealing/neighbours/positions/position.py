import random

class Position:
    def __init__(self):
        pass

    def __call__(self, shape):
        return ( int(random.uniform(0, shape[0] - 1)), int(random.uniform(0, shape[1] - 1)) )
