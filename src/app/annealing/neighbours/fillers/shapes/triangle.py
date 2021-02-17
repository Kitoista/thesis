import numpy as np
import random

from .shape import Shape

class Triangle(Shape):
    def random():
        sides = np.array([
            (0, random.uniform(0.3, 0.7)),
            (1, random.uniform(0.3, 0.7)),
            (random.uniform(0.3, 0.7), 0),
            (random.uniform(0.3, 0.7), 1)
        ])
        sides = np.delete(sides, random.randrange(4), 0)
        triangle = Triangle(sides[0], sides[1], sides[2])
        return triangle

    def __init__(self, A, B, C):
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)

        min = A
        max = A
        med = A
        for point in [B, C]:
            if min[0] > point[0]:
                min = point
            if max[0] < point[0]:
                max = point

        for point in [A, B, C]:
            if point is not min and point is not max:
                med = point
                break

        if min is max:
            self.A = A
            self.B = B
            self.C = C
        else:
            self.A = min
            self.B = med
            self.C = max

        self.oneDown = self.A[1] > self.B[1]

    def overLine(self, A, B, pos):
        if pos[0] < A[0] or pos[0] > B[0]:
            return False

        if A[1] + (B[1] - A[1]) / (B[0] - A[0]) * (pos[0] - A[0]) < pos[1]:
            return True
        return False

    def underLine(self, A, B, pos):
        if pos[0] < A[0] or pos[0] > B[0]:
            return False

        if A[1] + (B[1] - A[1]) / (B[0] - A[0]) * (pos[0] - A[0]) > pos[1]:
            return True
        return False

    def contains(self, pos):
        if self.oneDown:
            return self.underLine(self.A, self.C, pos) and (self.overLine(self.A, self.B, pos) or self.overLine(self.B, self.C, pos))
        else:
            return self.overLine(self.A, self.C, pos) and (self.underLine(self.A, self.B, pos) or self.underLine(self.B, self.C, pos))

    def __str__(self):
        return f"Triangle[ A: ({self.A[0]:.3g}, {self.A[1]:.3g}), B: ({self.B[0]:.3g}, {self.B[1]:.3g}), C: ({self.C[0]:.3g}, {self.C[1]:.3g}) ]"
