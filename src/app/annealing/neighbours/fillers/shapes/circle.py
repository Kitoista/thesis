import numpy as np

from .shape import Shape

class Circle(Shape):
    def random():
        return Circle((0.5, 0.5), 0.5)

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def contains(self, pos):
        return np.linalg.norm((self.center[0] - pos[0], self.center[1] - pos[1])) <= self.radius
