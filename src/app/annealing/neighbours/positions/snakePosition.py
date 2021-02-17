import numpy as np
import random

from .position import Position

class SnakePosition(Position):
    def __init__(self, walkChance):
        self.walkChance = walkChance

        self.pos = (80, 80)

    def __call__(self, shape):
        self.pos = (max(0, min(shape[0] - 1, int(self.pos[0] + random.uniform(-self.walkChance + 1, self.walkChance)))),
        max(0, min(shape[1] - 1, int(self.pos[1] + random.uniform(-self.walkChance + 1, self.walkChance)))))
        return self.pos
