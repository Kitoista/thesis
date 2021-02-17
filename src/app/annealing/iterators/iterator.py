class Iterator:
    def __init__(self, maxsteps):
        self.maxsteps = maxsteps

    def __call__(self, step, cost, T):
        return step < self.maxsteps
