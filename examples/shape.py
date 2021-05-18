import numpy as np
import random

class Shape:
    def random():
        return Shape()

    def __init__(self):
        pass

    def contains(self, pos):
        return True

    def toMask(self, size):
        mask = np.full((size, size), 0, dtype=float)
        for i in range(size):
            for j in range(size):
                if self.contains((i / float(size), j / float(size))):
                    mask[i][j] = 1
        return mask

class Rectangle(Shape):
    def random():
        return Rectangle((0.5, 0.5), (random.uniform(0.2, 1.1), random.uniform(0.2, 1.1)))

    def __init__(self, position, size):
        self.position = position
        self.size = size

    def contains(self, pos):
        return (self.position[0] + self.size[0] / 2 >= pos[0] and self.position[0] - self.size[0] / 2 <= pos[0]) and \
               (self.position[1] + self.size[1] / 2 >= pos[1] and self.position[1] - self.size[1] / 2 <= pos[1])

class Circle(Shape):
    def random():
        return Circle((0.5, 0.5), 0.5)

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def contains(self, pos):
        return np.linalg.norm((self.center[0] - pos[0], self.center[1] - pos[1])) < self.radius

class RoundedRectangle(Shape):
    def random():
        return RoundedRectangle(random.uniform(0, 1))

    def __init__(self, corner):
        self.elements = []
        corner = float(corner) / 2
        self.elements.append(Rectangle((0.5, 0.5), (1, 1-2*corner)))
        self.elements.append(Rectangle((0.5, 0.5), (1-2*corner, 1)))
        self.elements.append(Circle((corner, corner), corner))
        self.elements.append(Circle((corner, 1 - corner), corner))
        self.elements.append(Circle((1 - corner, corner), corner))
        self.elements.append(Circle((1 - corner, 1 - corner), corner))

    def contains(self, pos):
        for element in self.elements:
            if element.contains(pos):
                return True
        return False

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



size = 15

# shape = Rectangle.random()
# shape = Circle.random()
# shape = RoundedRectangle.random()
# shape = RoundedRectangle(0)
# shape = RoundedRectangle(1)
shape = Triangle.random()

# print("   ", end="")
# for i in range(size):
#     print(i, end=" ")
# print()

nyomi=1

for j in range(int(size*nyomi)):
    print(j, end="\t")
    for i in range(size):
        print('#' if shape.contains(((i+0.5)/(size), (j+0.5)/(size*nyomi))) else ' ', end=" ")
    print()
