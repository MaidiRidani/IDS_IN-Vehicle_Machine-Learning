import numpy as np
import pywt
import os
import cv2


class DWTProcessor:
    """
    Three Overlapped Wavelet Transform
    """

    def transform(
        self,
        window,
        level,
        index=None
    ):

        coif = window.copy()
        db3 = window.copy()
        rbio = window.copy()

        for _ in range(level):

            coif, _ = pywt.dwt2(coif, "coif1")
            db3, _ = pywt.dwt2(db3, "db3")
            rbio, _ = pywt.dwt2(rbio, "rbio1.3")

        target_size = window.shape[0] // (2 ** level)

        coif = coif[:target_size, :target_size]
        db3 = db3[:target_size, :target_size]
        rbio = rbio[:target_size, :target_size]

        # ==========================
        # DEBUG IMAGE
        # ==========================

        suffix = "" if index is None else f"_{index:03d}"

        self._save_image(coif, f"coif{suffix}.png")
        self._save_image(db3, f"db3{suffix}.png")
        self._save_image(rbio, f"rbio{suffix}.png")

        rgb = np.stack(
            [coif, db3, rbio],
            axis=-1
        )

        self._save_image(rgb, f"rgb{suffix}.png")

        return rgb

    def _save_image(
        self,
        image,
        filename
    ):

        os.makedirs("debug_dwt", exist_ok=True)

        img = image.copy()

        # Normalisasi agar bisa dilihat
        img = cv2.normalize(
            img,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        img = img.astype(np.uint8)

        cv2.imwrite(
            os.path.join("debug_dwt", filename),
            img
        )


    def save_rgb_image(
        self,
        image,
        index
    ):

        os.makedirs(
            "cache/images",
            exist_ok=True
        )

        img = image.copy()

        img = cv2.normalize(

            img,

            None,

            0,

            255,

            cv2.NORM_MINMAX

        )

        img = img.astype(np.uint8)

        cv2.imwrite(

            f"cache/images/image_{index}.png",

            img

        )