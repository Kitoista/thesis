import random

from .cost import Cost

class HomogenityCost(Cost):
    def __init__(self, count, l):
        super().__init__()
        self.count = count
        self.l = l

    def __call__(self, state):
        sin_error = super().cost(state)

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

        not_ok = self.count - ok

        return sin_error + self.l*(not_ok / self.count)
