import time
import sys

from app.threads.threadPool import ThreadPool
from app.threads.oldThreadPool import OldThreadPool
from app.threads.normalPool import NormalPool

from gui import assets

from app.radon import Radon
from app.annealing.costs.cost import Cost
from app.annealing.costs.descriptors.lbpDescriptor import LbpDescriptor
# from app.annealing.costs.descriptors.cooccDescriptor import CooccDescriptor
from app.annealing.costs.descriptors.gaborDescriptor import GaborDescriptor

threadPoolMode = sys.argv[1]
threadPoolSize = int(sys.argv[2])
modes = {
    "tp": ThreadPool,
    "otp": OldThreadPool,
    "np": NormalPool
}
inputs = {}


image = assets.loadImage("original.png")
state = assets.loadImage("2021-03-25_17-51-26.png")

# descriptor = LbpDescriptor(4, 1)
# goodValue = [0, 3.9062e-05, 0.033125, 0.028906, 0.93746, 0.00046875]

# descriptor = CooccDescriptor(1, 1)
# goodValue = [0, 3.9062e-05, 0.033125, 0.028906, 0.93746, 0.00046875]

descriptor = GaborDescriptor(2, [1, 2], [0.05, 0.25])
goodValue = [0.11822, 0.02963, 0.03614, 0.0041105, 0.10196, 0.017051, 0.00087619, 0.00037481, 0.11822, 0.029539, 0.03614, 0.0035751, 0.10196, 0.016891, 0.00087619, 0.00015239]
l = 5

cost = Cost(goodValue, l)

cost.sinogram = Radon(image, 32, [0, 180]).transform()
cost.theta = 32
cost.angleBounds =  [0, 180]
cost.descriptor = descriptor

for a in range(1, 23):

    timeA = time.time()

    for i in range(threadPoolSize):
        inputs[i] = 0

    def mainJob(results):
        for i in range(threadPoolSize):
            inputs[i] = results[i]
        return inputs

    def threadJob(input):
        a = 0
        for i in range(100):
            a = cost(state, 0.1)[0]
        return input + a

    def mainLoopCondition(step):
        return step < 100

    timeA = time.time()
    tp = modes[threadPoolMode](mainJob=mainJob, threadJob=threadJob, threadPoolSize=threadPoolSize, mainLoopCondition=mainLoopCondition)
    tp.run(inputs)
    timeB = time.time()
    print(f"({threadPoolSize}, {(int)((timeB - timeA) * 1000)})")


#
# (1, 2706)
# (2, 2766)
# (3, 2920)
# (4, 3150)
# (5, 3288)
# (6, 3538)
# (7, 4610)
# (8, 4901)
# (9, 5257)
# (10, 5699)
# (11, 6290)
# (12, 7042)
# (13, 7922)
# (14, 8624)
# (15, 9299)
# (16, 9930)
# (17, 10559)
