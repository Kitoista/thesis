import random

class Filler:
    def __init__(self, bounds):
        self.bounds = bounds

    def __call__(self, newState, pos, color, T):
        window_x_size = int(random.uniform(self.bounds[0], self.bounds[1]))
        window_y_size = int(random.uniform(self.bounds[0], self.bounds[1]))

        window_x = (max(0, pos[0]), min(newState.shape[0], pos[0] + window_x_size))
        window_y = (max(0, pos[1]), min(newState.shape[1], pos[1] + window_y_size))

        newState[window_x[0]:window_x[1], window_y[0]:window_y[1]] = color
        # debugMessage = f"window size: ({window_x_size}, {window_y_size})"
        debugMessage = ""

        return newState, debugMessage
