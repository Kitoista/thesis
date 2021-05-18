import random

from .shape import Shape
from .rectangle import Rectangle
from .circle import Circle

class RoundedRectangle(Shape):
    def random():
        return RoundedRectangle(random.uniform(0, 1))

    def __init__(self, corner):
        self.elements = []
        corner = float(corner) / 2
        self.elements.append(Rectangle((0.5, 0.5), (1, 1-2*corner)))
        self.elements.append(Rectangle((0.5, 0.5), (1-2*corner, 1)))
        self.elements.append(Circle((corner, corner), corner))
        self.elements.append(Circle((corner, 1 - corner), corner))
        self.elements.append(Circle((1 - corner, corner), corner))
        self.elements.append(Circle((1 - corner, 1 - corner), corner))

    def contains(self, pos):
        for element in self.elements:
            if element.contains(pos):
                return True
        return False
