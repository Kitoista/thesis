import random

from .color import Color

class CopyColor(Color):
    def __init__(self, copyChance = 0.5, maxDiff = 0.1):
        self.copyChance = copyChance
        self.maxDiff = 0.1

    def __call__(self, state, pos):
        if random.uniform(0, 1) > self.copyChance:
            return super().__call__(state, pos)

        diff = random.uniform(1 - self.maxDiff, 1 + self.maxDiff)

        direction = random.uniform(0, 0)

        oldColor = 0
        if direction < 0.25:
            # south
            oldColor = state[pos[0]][max(0, pos[1] - 1)]
        elif direction < 0.5:
            # north
            oldColor = state[pos[0]][min(state.shape[1] - 1, pos[1] + 1)]
        elif direction < 0.75:
            # west
            oldColor = state[max(0, pos[0] - 1)][pos[1]]
        else:
            # east
            oldColor = state[min(state.shape[0] - 1, pos[0] - 1)][pos[1]]

        newColor = max(0, min(1, oldColor * diff))

        return newColor
