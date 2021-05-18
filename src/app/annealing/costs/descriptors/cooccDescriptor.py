from skimage import feature
import numpy as np

from .descriptor import Descriptor
from ....error import error

class CooccDescriptor(Descriptor):
    def __init__(self, distances, angles, grayScale):
        self.distances = distances
        self.angles = angles
        self.grayScale = grayScale

        self.grayScaleDict = {}
        for i in range(len(self.grayScale)):
            self.grayScaleDict[self.grayScale[i]] = i

    def __call__(self, state):
        img = np.zeros(state.shape)

        for i in range(state.shape[0]):
            for j in range(state.shape[1]):
                img[i, j] = self.grayScaleDict[state[i, j]]

        img = img.astype('uint8')

        levels = self.grayScale.shape[0]

        coocc = feature.greycomatrix(img, self.distances, self.angles, levels=levels)
        feats = np.zeros((len(self.distances), len(self.angles), 4), dtype=np.float)
        vect = np.arange(levels)
        ones = np.ones(levels)
        rows = np.matmul(vect.reshape(levels, 1), ones.reshape(1, levels))
        columns = np.matmul(ones.reshape(levels, 1), vect.reshape(1, levels))

        eps = np.ones((levels, levels)) * 0.00000000000001

        for i in range(len(self.distances)):
            for j in range(len(self.angles)):
                Q = coocc[:, :, i, j]

                columnMeans = Q.mean(0)
                rowMeans = Q.mean(1)

                columnVars = Q.var(0)
                rowVars = Q.var(1)

                # contrast
                feats[i, j, 0] = np.sum((rows - columns)**2 * Q)
                if rowVars.min() == 0 or columnVars.min() == 0:
                    # correlation
                    feats[i, j, 1] = 0
                else:
                    # correlation
                    feats[i, j, 1] = np.sum((rows - rowMeans) * (columns - columnMeans) * Q / rowVars / columnVars)
                # energy
                feats[i, j, 2] = np.sum(Q**2)
                # homogenity
                feats[i, j, 3] = np.sum(Q / (1 + np.abs(rows - columns)))

        res = np.zeros((4, 2), dtype=np.float)
        for i in range(4):
            res[i, 0] = np.mean(feats[:, :, i])
            res[i, 1] = np.var(feats[:, :, i])


        # 15233 5.1459e+07 0.64905 0.079268 2.4014e+08 4.9993e+14 23352 8.9761e+05
        # goodValue = np.array([15233, 5.1459e+07, 1.3584e+11, 5.8197e+19, 2.4014e+08, 4.9993e+14, 23352, 8.9761e+05])
        # desc = np.array([14981, 8.6682e+07, 1.3486e+11, 1.0322e+20, 2.3783e+08, 8.9695e+14, 23284, 1.6061e+06])


        # print(feats)
        # desc = feats


        # print(np.array_str(desc, precision = 3, suppress_small = True))
        # print(res)
        return res.flatten()

    def compare(self, goodValue, desc):
        err = (goodValue - desc)
        return np.sum(np.abs(err) / goodValue)
        # return error.sumDiff(goodValue, desc)

    def show(self, img):
        return img

    # def toMatrix(self, vect):
    #     return vect.reshape((self.grayScale.shape[0], self.grayScale.shape[0], self.distances.shape[0], self.angles.shape[0]))
