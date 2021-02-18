import math
import random

class Annealing:
    def __init__(self, app, start=None, iterator=None, cost=None, neighbour=None, accept=None, temperature=None):
        self.app = app
        self.start = start
        self.iterator = iterator
        self.cost = cost
        self.neighbour = neighbour
        self.accept = accept
        self.temperature = temperature

        self.running = False
        pass

    def __call__(self):
        self.running = True
        state = self.start()
        cost = self.cost(state)

        step = 0
        T = self.temperature(step)

        accepts = 0

        while self.iterator(step, cost, T) and self.running:
            T = self.temperature(step)
            newState, debugMessage = self.neighbour(state, step)
            newCost = self.cost(newState)

            if self.accept(cost, newCost, T):
                accepts += 1
                state = newState
                cost = newCost

            debugMessage = f"accepts = {accepts} {debugMessage}"
            self.app.onAnnealingStep(state, step, cost, T, debugMessage, False)

            step += 1

        self.app.onAnnealingStep(state, step, cost, T, debugMessage, True)
        self.app.killAnnealing()

        return state
