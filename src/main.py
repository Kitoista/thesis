from gui.window import Window
from app.application import app

from skimage.data import shepp_logan_phantom
from PIL import Image

# method = 'iradons'
method = 'annealing'
# method = 'nothing'

if method == 'annealing':
    window = Window()
    window.init(app)
    window.start()

import skimage
import numpy as np
import matplotlib.pyplot as plt

import random
import math

from app import radon, annealing
from app.reconstructors import iradon
from app.reconstructors import iradonSart
from app.error import rms


from gui import event
from app import imageLib


# print('a')
# print(shepp_logan_phantom())
image = imageLib.normalize(shepp_logan_phantom())
# print(image.shape)
# print(image)
# exit()
# print('b')
# image = imageLib.normalize(Image.open('pattern.jpg'))

theta = 32
radonTrans = radon.Radon(image, theta)
sinogram = radonTrans.transform()

def random_start():
    # return np.random.rand(image.shape[0], image.shape[1])
    return np.full(image.shape, 0, dtype=float)

def cost_function(state):
    stateRadonTrans = radon.Radon(state, theta)
    stateSinogram = stateRadonTrans.transform()

    sin_error = rms.error(sinogram, stateSinogram)

    count = 10
    ok = 0
    # not_ok = 50
    # for x in range(count):
    #     i = int(random.uniform(1, state.shape[0] - 1))
    #     j = int(random.uniform(1, state.shape[1] - 1))
    #     color = state[i][j]
    #     gotya = 0
    #     for di in range(3):
    #         if gotya == 1:
    #             break
    #         for dj in range(3):
    #             if di == 1 and dj == 1:
    #                 continue
    #             other_color = state[i - 1 + di][j - 1 + dj]
    #             if other_color > color * 0.9 and other_color < color * 1:
    #                 ok += 1
    #                 gotya = 1
    #                 break
    #
    not_ok = count - ok

    return sin_error + 0.01*(not_ok / count)

def temperature(step, maxsteps, probability_start, probability_end):
    temperature_start = -1.0/math.log(probability_start)
    temperature_end = -1.0/math.log(probability_end)

    exponent = (temperature_end / temperature_start)**(step/(maxsteps-1.0))

    return temperature_start*exponent


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def contains(self, pos):
        return np.linalg.norm((self.center[0] - pos[0], self.center[1] - pos[1])) <= self.radius

class Rectangle:
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def contains(self, pos):
        return self.position[0] <= pos[0] and (self.position[0] + self.size[0] >= pos[0]) and \
               self.position[1] <= pos[1] and (self.position[1] + self.size[1] >= pos[1])

class Shape:
    def __init__(self, corner):
        self.elements = []
        corner = float(corner) / 2
        self.elements.append(Rectangle((0, corner), (1, 1-2*corner)))
        self.elements.append(Rectangle((corner, 0), (1-2*corner, 1)))
        self.elements.append(Circle((corner, corner), corner))
        self.elements.append(Circle((corner, 1 - corner), corner))
        self.elements.append(Circle((1 - corner, corner), corner))
        self.elements.append(Circle((1 - corner, 1 - corner), corner))

    def contains(self, pos):
        for element in self.elements:
            if element.contains(pos):
                return True
        return False

    def toMask(self, size):
        mask = np.full((size, size), 0, dtype=float)
        for i in range(size):
            for j in range(size):
                if self.contains((i / float(size), j / float(size))):
                    mask[i][j] = 1
        return mask

class Triangle:
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



# triangle = Triangle(
#     (0, 0),
#     (0, 1),
#     (1, 0))
#
# print(triangle)
# print('-------------------')
# pos = (0, 0.9)
# print(triangle.underLine(triangle.A, triangle.B, pos))
# print(triangle.underLine(triangle.B, triangle.C, pos))
#
# for i in np.arange(0, 1, 0.1):
#     for j in np.arange(0, 1, 0.1):
#         print(f"({i:.1g}, {j:.1g}) {triangle.contains((i, j))}")

max_same_count = 62
same_count = 62
pos = 0

grid_size = 20

original_grid = []
for x in np.ndindex((grid_size, grid_size)):
    original_grid.append(( x[0]/grid_size, x[1]/grid_size ))

grid = np.copy(original_grid)

def random_neighbour(state, step, maxsteps):
    # Tx = temperature(step, maxsteps, 0.1, 0.02)
    # Ty = temperature(step, maxsteps, 0.1, 0.02)

    global max_same_count
    global same_count
    global pos
    global original_grid
    global grid

    # window_x_size = int(math.exp(-1/Tx) * state.shape[0] / 2)
    # window_y_size = int(math.exp(-1/Ty) * state.shape[1] / 2)

    # window_x_size = int(random.uniform(4, 12))
    # window_y_size = window_x_size
    window_x_size = int(random.uniform(0, 8))
    window_y_size = int(random.uniform(0, 8))

    # window_x_size = 1
    # window_y_size = 1

    # shape = Shape(random.uniform(0, 1))

    changes = int(random.uniform(1, 1))

    for db in range(changes):
        if same_count >= max_same_count:
            if len(grid) == 0:
                grid = np.copy(original_grid)

            grid_index = random.randrange(len(grid))
            pos = grid[grid_index]
            grid = np.delete(grid, grid_index, 0)


            pos = (int(pos[0] * state.shape[0]), int(pos[1] * state.shape[1]))
            same_count = 0
        else:
            pos = (max(0, min(state.shape[0] - 1, int(pos[0] + random.uniform(-4, 5)))), max(0, min(state.shape[1] - 1, int(pos[1] + random.uniform(-4, 5)))))
            same_count += 1

        window_x = (max(0, pos[0] - window_x_size), min(state.shape[0] - 1, pos[0] + window_x_size))
        window_y = (max(0, pos[1] - window_y_size), min(state.shape[1] - 1, pos[1] + window_y_size))

        new_color = random.uniform(0, 1)
        if random.uniform(0, 1) < 0.5:
            diff = random.uniform(1, 1)
            # diff = 1
            neighbour_random = random.uniform(0, 0)

            old_color = 0
            if neighbour_random < 0.25:
                old_color = state[pos[0]][max(0, pos[1] - 1)]
            elif neighbour_random < 0.5:
                old_color = state[pos[0]][min(state.shape[1] - 1, pos[1] + 1)]
            elif neighbour_random < 0.75:
                old_color = state[max(0, pos[0] - 1)][pos[1]]
            else:
                old_color = state[min(state.shape[0] - 1, pos[0] - 1)][pos[1]]

            new_color = max(0, min(1, old_color * diff))

        new_state = np.copy(state)

        # print(window_x)
        # print(window_y)

        if random.uniform(0, 1) < 1:
            new_state[window_x[0]:window_x[1], window_y[0]:window_y[1]] = new_color

        # for i in window_x_range:
        #     for j in window_y_range:
        #         if shape.contains(((i+window_x_size/2-pos[0]) / float(window_x_size), (j+window_y_size/2-pos[1]) / float(window_y_size))):

        # new_color = 1

        # print(triangle)

        # print(pos)
        # print(window_x_size)
        # print(window_x)
        # print('-------------------')
        # for i in np.arange(0, 1, 0.1):
        #     for j in np.arange(0, 1, 0.1):
        #         triangle.contains((i, j))

        else:
            sides = np.array([
                (0, random.uniform(0.3, 0.7)),
                (1, random.uniform(0.3, 0.7)),
                (random.uniform(0.3, 0.7), 0),
                (random.uniform(0.3, 0.7), 1)
            ])
            sides = np.delete(sides, random.randrange(4), 0)
            triangle = Triangle(sides[0], sides[1], sides[2])

            for i in range(int(window_x[0]), int(window_x[1])):
                for j in range(int(window_y[0]), int(window_y[1])):
                    relPos = ((i+window_x_size-pos[0]) / float(window_x_size*2), (j+window_y_size-pos[1]) / float(window_y_size*2))
                    if triangle.contains(relPos):
                        new_state[i][j] = new_color


    debug_message = f"window_size = {window_x_size}"

    return new_state, debug_message


def acceptance_probability(cost, new_cost, T):
    if cost > new_cost:
        return 1
    return math.exp(-1/T)


def show(state, cost, step, maxsteps):
    # imkwargs = dict(vmin=-0.2, vmax=0.2)
    # fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(12, 4.5),
    #                                sharex=True, sharey=True)

    stateRadonTrans = radon.Radon(state, theta)
    stateSinogram = stateRadonTrans.transform()
    error = rms.error(image, state)

    window.triggerEvent(event.ShowEvent(
        recon=state,
        reconRadon=stateSinogram,
        step=step,
        maxsteps=maxsteps,
        error=error,
        cost=cost,
    ))

    # ax1.set_title("Original")
    # ax1.imshow(image, cmap=plt.cm.Greys_r)
    # ax2.set_title("Original sinogram")
    # ax2.imshow(sinogram, cmap=plt.cm.Greys_r)
    # ax3.set_title(f"Reconstrunction\n #{(step + 1):>4g}/{maxsteps:>4g}")
    # ax3.imshow(state, cmap=plt.cm.Greys_r)
    # ax4.set_title("Reconstruction sinogram")
    # ax4.imshow(stateSinogram, cmap=plt.cm.Greys_r)
    # ax5.set_title(f"Cost: {cost:.3g} error: {error:.3g}")
    # ax5.imshow(state - image, cmap=plt.cm.Greys_r, **imkwargs)
    # plt.show()

# for step in range(3):
#     new_state = random_neighbour(random_start(), step, 100)
    # print(new_state)
    # show(new_state, 0, step, 3)


if method == 'annealing':
    window.triggerEvent(event.OriginalUpdateEvent(image, sinogram))

    recon, cost = annealing.annealing(random_start=random_start,
              cost_function=cost_function,
              random_neighbour=random_neighbour,
              acceptance_probability=acceptance_probability,
              temperature=temperature,
              probability_start=0.001,
              probability_end=0.00001,
              maxsteps=50000,
              debug_bundles=1000,
              show=show,
              show_budles=10,
              debug=True)



# using iradon and iradon sart
def iradons():
    # skimage.io.imsave(f"original.png", np.around(image*255).astype(np.uint8))
    theta = 32
    radonTrans = radon.Radon(image, theta)
    sinogram = radonTrans.transform()
    mode = None
    iterations = 2
    def logger(recon, i):
        # skimage.io.imsave(f"mode{mode}_iteration{i}.png", np.around((recon-image)*255).astype(np.uint8))
        error = rms.error(image, recon)
        print(f"Error ({i} iterations): {error:.3g}")

        # if i == iterations - 1:
        imkwargs = dict(vmin=-0.2, vmax=0.2)
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4.5),
        sharex=True, sharey=True)
        ax1.set_title("Original")
        ax1.imshow(image, cmap=plt.cm.Greys_r)
        ax2.set_title(f"Reconstrunction\n ({mode} iteration{i})")
        ax2.imshow(recon, cmap=plt.cm.Greys_r)
        ax3.set_title(f"Error: {error:.3g}")
        ax3.imshow(recon - image, cmap=plt.cm.Greys_r, **imkwargs)
        plt.show(block=False)



    def oneOf0():
        recon = None
        reconstructor0 = iradon.IRadon(sinogram, theta)
        recon = reconstructor0.transform()
        logger(recon, 0)

    def oneOf1():
        recon = None
        reconstructor1 = iradonSart.IRadonSart(sinogram, theta, 1, recon=recon)
        recon = reconstructor1.transform()
        logger(recon, 0)

    def twoOf1():
        recon = None
        reconstructor1 = iradonSart.IRadonSart(sinogram, theta, iterations, recon=recon)
        recon = reconstructor1.transform()
        logger(recon, iterations)

    def base0into1():
        recon = None
        reconstructor0 = iradon.IRadon(sinogram, theta)
        recon = reconstructor0.transform()

        reconstructor1 = iradonSart.IRadonSart(sinogram, theta, iterations, recon=recon)
        recon = reconstructor1.transform()
        logger(recon, iterations)

    print()
    mode = "IRadon"
    oneOf0()
    print()
    mode = "SART"
    oneOf1()
    print()
    mode = "SARTs"
    twoOf1()
    print()
    mode = "IRadon into SARTs"
    base0into1()
    print()

    input("Press enter to exit ;)")


if method == 'iradons':
    iradons()
