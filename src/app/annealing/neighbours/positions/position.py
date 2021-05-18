import random

class Position:
    def __init__(self):
        pass

    def __call__(self, shape):
        return ( int(random.uniform(0, shape[0])), int(random.uniform(0, shape[1])) )
