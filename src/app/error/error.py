import numpy as np

def sumDiff(image, recon):
    error = recon - image
    return np.sum((error)**2)

def meanDiff(image, recon):
    error = recon - image
    return np.mean(error)

def maxDiff(image, recon):
    error = recon - image
    return np.max(error)

def rms(image, recon):
    error = recon - image
    return np.sqrt(np.mean(error**2))
