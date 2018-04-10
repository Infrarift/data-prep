import random

import numpy as np


class PoissonNoise:
    def __init__(self):
        pass

    def augment(self, image):
        # Add Poisson Noise
        noise = len(np.unique(image))
        noise = 2 ** np.ceil(np.log2(noise))
        noisy = np.random.poisson(image * noise) / float(noise)
        noisy = np.clip(noisy, 0, 255)
        return noisy

    def augment_gaussian(self, image):
        var = 50 + random.random() * 50
        sigma = var ** 0.5
        gauss = np.random.normal(0, sigma, image.shape)
        gauss = gauss.reshape(image.shape)
        noisy = image + gauss
        noisy = np.clip(noisy, 0, 255)
        return noisy.astype(np.uint8)

