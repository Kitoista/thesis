import numpy as np
from skimage.transform import iradon

class IRadon:

    def __init__(self, sinogram, theta):
        self.sinogram = sinogram
        self.theta = np.linspace(0., 180., theta, endpoint=False)

    def transform(self):
        recon = iradon(self.sinogram, theta=self.theta, circle=True)
        return recon
        # error = reconstruction_fbp - .image
        # print(f"FBP rms reconstruction error: {np.sqrt(np.mean(error**2)):.3g}")

        # return np.sqrt(np.mean(error**2))
        # imkwargs = dict(vmin=-0.2, vmax=0.2)
        # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5),
        #                                sharex=True, sharey=True)
        # ax1.set_title("Reconstruction\nFiltered back projection")
        # ax1.imshow(reconstruction_fbp, cmap=plt.cm.Greys_r)
        # ax2.set_title("Reconstruction error\nFiltered back projection")
        # ax2.imshow(reconstruction_fbp - radonTrans.image, cmap=plt.cm.Greys_r, **imkwargs)
        # plt.show()
