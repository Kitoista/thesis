import math
import random
import time
import datetime
# from threading import Thread, Semaphore
from app.threads.threadPool import ThreadPool
from app.threads.oldThreadPool import OldThreadPool
from app.threads.normalPool import NormalPool

from app.imageLib import imageLib

class Annealing:
    def __init__(self, app, start=None, iterator=None, cost=None, neighbour=None, accept=None, temperature=None):
        self.app = app
        self.start = start
        self.iterator = iterator
        self.cost = cost
        self.neighbour = neighbour
        self.accept = accept
        self.temperature = temperature

        self.normalizerInterval = 50000000
        self.normalizerHist = []

        self.threadLength = 100
        self.threadPoolSize = 8

        self.startedAt = None
        self.running = False
        pass

    def __call__(self):
        self.running = True
        self.startedAt = time.time();

        step = 0
        accepts = 0

        state = self.start()
        T = self.temperature(step)
        cost, costDebug = self.cost(state, T)

        tp = ThreadPool(threadPoolSize=self.threadPoolSize, threadJob=self.threadJob)
        tp.startThreads()

        while self.iterator(step, cost, T) and self.running:
            T = self.temperature(step)
            debugMessage = ""

            inputs = {}
            for i in range(self.threadPoolSize):
                inputs[i] = (state, cost, step, accepts, i)

            results = tp.nextResults(inputs)

            for i in range(self.threadPoolSize):
                newState, newCost, newStep, newAccepts, debugMessage = results[i]
                if self.accept(cost, newCost, T):
                    state = newState
                    cost = newCost
                    accepts = newAccepts
                    step = newStep

            self.app.onAnnealingStep(state, step, cost, T, debugMessage, False)


        self.app.onAnnealingStep(state, step, cost, T, debugMessage, True)
        self.app.killAnnealing()
        tp.killThreads()

        return state

    def threadJob(self, input):
        state = input[0]
        cost = input[1]
        step = input[2]
        accepts = input[3]
        index = input[4]

        for step in range(step, step + self.threadLength):
            if not self.running:
                break;
            T = self.temperature(step)

            newState, neighbourDebug = self.neighbour(state, step, T)
            newCost, costDebug = self.cost(newState, T)

            if self.accept(cost, newCost, T):
                accepts += 1
                cost = newCost
                state, changed = self.normalizer(newState, step)
                if changed:
                    cost, costDebug = self.cost(state, T)

            debugMessage = f"accepts = {accepts} {costDebug} {neighbourDebug} {str(datetime.timedelta(seconds=(math.floor(time.time() - self.startedAt))))}"
            if index == 0:
                self.app.onAnnealingStep(state, step, cost, T, debugMessage, False)

        return (state, cost, step, accepts, debugMessage)

    def normalizer(self, state, step):
        histEntry = math.floor(step / self.normalizerInterval)

        if histEntry in self.normalizerHist:
            return state, False

        self.normalizerHist.append(histEntry)

        for i in range(state.shape[0]):
            for j in range(state.shape[1]):
                state[i, j] = imageLib.closestColor(state[i, j])

        return state, True
