import random

from .shape import Shape

class Rectangle(Shape):
    def random():
        return Rectangle((0.5, 0.5), (random.uniform(0.2, 1.1), random.uniform(0.2, 1.1)))

    def __init__(self, position, size):
        self.position = position
        self.size = size

    def contains(self, pos):
        return (self.position[0] + self.size[0] / 2 >= pos[0] and self.position[0] - self.size[0] / 2 <= pos[0]) and \
               (self.position[1] + self.size[1] / 2 >= pos[1] and self.position[1] - self.size[1] / 2 <= pos[1])
