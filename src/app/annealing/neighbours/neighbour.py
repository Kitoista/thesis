import numpy as np
import random
from app.imageLib import imageLib

class Neighbour:

    def __init__(self, changesBounds):
        self.changesBounds = changesBounds
        self.position = None
        self.color = None
        self.filler = None

    def __call__(self, state, step, T):
        changes = int(random.uniform(self.changesBounds[0], self.changesBounds[1]))

        newState = np.copy(state)

        debugMessage = ""

        for i in range(changes):
            pos = self.position(newState.shape)

            newColor = imageLib.closestColor(self.color(state, pos))

            newState, currentDebugMessage = self.filler(newState, pos, newColor, T)

            if i != 0:
                currentDebugMessage = f" {currentDebugMessage}"

            debugMessage = f"{debugMessage}{currentDebugMessage}"

        return newState, f"[{debugMessage}]"
