import numpy as np
import random

from .position import Position

class GridPosition(Position):
    def __init__(self, gridSize, maxSameCount, walkChance):
        self.maxSameCount = maxSameCount
        self.sameCount = maxSameCount
        self.walkChance = walkChance

        self.pos = None

        self.originalGrid = []
        for x in np.ndindex((gridSize, gridSize)):
            self.originalGrid.append(( x[0] / gridSize, x[1] / gridSize ))

        self.grid = np.copy(self.originalGrid)

    def __call__(self, shape):
        if self.sameCount >= self.maxSameCount:
            if len(self.grid) == 0:
                self.grid = np.copy(self.originalGrid)

            gridIndex = random.randrange(len(self.grid))
            self.pos = self.grid[gridIndex]
            self.grid = np.delete(self.grid, gridIndex, 0)

            self.pos = (int(self.pos[0] * shape[0]),
                        int(self.pos[1] * shape[1]))
            self.sameCount = 0
        else:
            self.pos = (max(0, min(shape[0] - 1, int(self.pos[0] + random.uniform(-self.walkChance + 1, self.walkChance)))),
                        max(0, min(shape[1] - 1, int(self.pos[1] + random.uniform(-self.walkChance + 1, self.walkChance)))))
            self.sameCount += 1

        return self.pos
