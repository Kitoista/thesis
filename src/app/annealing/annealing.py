import math
import random
from ..application import app

class Annealing:
    def __init__(self, start=None, iterator=None, cost=None, neighbour=None, accept=None, temperature=None):
        self.start = start
        self.iterator = iterator
        self.cost = cost
        self.neighbour = neighbour
        self.accept = accept
        self.temperature = temperature
        pass

    def __call__(self):
        state = self.start()
        cost = self.cost(state)

        step = 0
        T = self.temperature(step)

        accepts = 0

        while self.iterator(step, cost, T):
            T = self.temperature(step)
            newState, debugMessage = self.neighbour(state, step)
            newCost = self.cost(newState)

            if self.accept(cost, newCost, T):
                accepts += 1
                state = newState
                cost = newCost

            debugMessage = f"accepts = {accepts} {debugMessage}"
            app.onAnnealingStep(state, step, cost, T, debugMessage, False)

            step += 1

        app.onAnnealingStep(state, step, cost, T, debugMessage, True)

        return state
