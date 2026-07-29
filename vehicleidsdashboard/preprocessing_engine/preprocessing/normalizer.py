import numpy as np


class Normalizer:
    """
    Normalisasi Min-Max
    Sama seperti notebook preprocessing.
    """

    def normalize(self, window):

        return window.astype(np.float32) / 255.0