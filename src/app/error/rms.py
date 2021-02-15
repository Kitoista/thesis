import numpy as np

def error(image, recon):
    error = recon - image
    return np.sqrt(np.mean(error**2))
