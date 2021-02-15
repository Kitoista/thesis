import numpy as np

from skimage.transform import iradon_sart

class IRadonSart:

    def __init__(self, sinogram, theta, iterations, recon=None, logger=None):
        self.sinogram = sinogram
        self.theta = np.linspace(0., 180., theta, endpoint=False)
        self.iterations = iterations
        if logger is None:
            def logger(recon, i):
                pass
        self.logger = logger
        self.recon = recon

    def transform(self):
        for i in range(self.iterations):
            self.recon = iradon_sart(self.sinogram, theta=self.theta, image=self.recon)
            self.logger(self.recon, i)

        return self.recon
    #
    # error = reconstruction_sart - image
    # print("SART (1 iteration) rms reconstruction error: "
    #       f"{np.sqrt(np.mean(error**2)):.3g}")
    #
    # fig, axes = plt.subplots(2, 2, figsize=(8, 8.5), sharex=True, sharey=True)
    # ax = axes.ravel()
    #
    # ax[0].set_title("Reconstruction\nSART")
    # ax[0].imshow(reconstruction_sart, cmap=plt.cm.Greys_r)
    #
    # ax[1].set_title("Reconstruction error\nSART")
    # ax[1].imshow(reconstruction_sart - image, cmap=plt.cm.Greys_r, **imkwargs)
    #
    # # Run a second iteration of SART by supplying the reconstruction
    # # from the first iteration as an initial estimate
    # reconstruction_sart2 = iradon_sart(sinogram, theta=theta,
    #                                    image=reconstruction_sart)
    # error = reconstruction_sart2 - image
    # print("SART (2 iterations) rms reconstruction error: "
    #       f"{np.sqrt(np.mean(error**2)):.3g}")
    #
    # ax[2].set_title("Reconstruction\nSART, 2 iterations")
    # ax[2].imshow(reconstruction_sart2, cmap=plt.cm.Greys_r)
    #
    # ax[3].set_title("Reconstruction error\nSART, 2 iterations")
    # ax[3].imshow(reconstruction_sart2 - image, cmap=plt.cm.Greys_r, **imkwargs)
    # plt.show()
