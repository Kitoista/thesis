import numpy as np

class Shape:
    def random():
        return Shape()

    def __init__(self):
        pass

    def contains(self, pos):
        return True

    def toMask(self, size):
        mask = np.full((size, size), 0, dtype=float)
        for i in range(size):
            for j in range(size):
                if self.contains((i / float(size), j / float(size))):
                    mask[i][j] = 1
        return mask
