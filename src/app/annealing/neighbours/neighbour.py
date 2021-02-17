import numpy as np
import random

class Neighbour:

    def __init__(self, changesBounds = (1, 1)):
        self.changesBounds = changesBounds
        self.position = None
        self.color = None
        self.filler = None

    def __call__(self, state, step):
        changes = int(random.uniform(self.changesBounds[0], self.changesBounds[1]))

        newState = np.copy(state)

        debugMessage = ""

        for i in range(changes):
            pos = self.position(newState.shape)

            newColor = self.color(state, pos)

            newState, currentDebugMessage = self.filler(newState, pos, newColor)

            if i != 0:
                currentDebugMessage = f" {currentDebugMessage}"

            debugMessage = f"{debugMessage}{currentDebugMessage}"

        return newState, f"[{debugMessage}]"
