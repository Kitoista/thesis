import random

from .filler import Filler

class ShapeFiller(Filler):
    # shapeClassesWithBounds [ (ShapeClass, (min, max)) ]
    def __init__(self, shapeClassesWithBounds):
        self.shapeClassesWithBounds = shapeClassesWithBounds
        self.maxT = None

    def __call__(self, newState, pos, color, T):
        if self.maxT is None:
            self.maxT = T
        shapeClassWithBounds = self.shapeClassesWithBounds[random.randrange(len(self.shapeClassesWithBounds))]
        shapeClass = shapeClassWithBounds[0]
        shape = shapeClass.random()
        bounds = shapeClassWithBounds[1]
        # bounds = (bounds[0], bounds[0] + ((bounds[1]-bounds[0])*(T/self.maxT)))

        size = int(random.uniform(bounds[0], bounds[1]))
        window_x = (max(0, pos[0] - size), min(newState.shape[0], pos[0] + size))
        window_y = (max(0, pos[1] - size), min(newState.shape[0], pos[1] + size))

        for i in range(int(window_x[0]), int(window_x[1])):
            for j in range(int(window_y[0]), int(window_y[1])):
                relPos = ((i+size+0.5-pos[0]) / float(size*2), (j+size+0.5-pos[1]) / float(size*2))
                if shape.contains(relPos):
                    newState[i][j] = color


        # debugMessage = f"{shapeClass.__name__} bounds: ({bounds})"
        debugMessage = ""

        return newState, debugMessage
