import random

from .descriptor import Descriptor

class HomogenityDescriptor(Descriptor):
    def __init__(self):
        super().__init__()

    def __call__(self, state):
        ok = 0
        for x in range(self.count):
            i = int(random.uniform(1, state.shape[0] - 1))
            j = int(random.uniform(1, state.shape[1] - 1))
            color = state[i][j]
            gotya = 0
            for di in range(3):
                if gotya == 1:
                    break
                for dj in range(3):
                    if di == 1 and dj == 1:
                        continue
                    other_color = state[i - 1 + di][j - 1 + dj]
                    if other_color > color * 0.9 and other_color < color * 1:
                        ok += 1
                        gotya = 1
                        break

        return [self.count - ok]

    def compare(self, goodValue, desc):
        return abs(desc - goodValue)[0]
