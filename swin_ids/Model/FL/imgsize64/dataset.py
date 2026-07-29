# ==============================
# IMPORT
# ==============================
import os
import numpy as np
from typing import Tuple


# ==============================
# PATH (SUDAH DIPERBAIKI)
# ==============================

BASE_PATH = "/home/dani/Documents/tugas akhir/TugasAkhirku2026/swin_ids/Preprocessing/hasil_preprocessing/prep64/forFL"

TEST_PATH = os.path.join(BASE_PATH, "test.npz")
VAL_PATH = os.path.join(BASE_PATH, "val.npz")

IID_PATH = os.path.join(BASE_PATH, "partition_iid")
NONIID_PATH = os.path.join(BASE_PATH, "partition_noniid_label_skew")


# ==============================
# LOAD CLIENT
# ==============================
def load_client_data(client_id: int, mode: int) -> Tuple[np.ndarray, np.ndarray]:

    if client_id not in [0, 1, 2, 3]:
        raise ValueError("client_id harus antara 0–3")

    if mode not in [1, 2]:
        raise ValueError("mode harus 1 atau 2")

    partition_path = IID_PATH if mode == 1 else NONIID_PATH

    file_path = os.path.join(partition_path, f"client_{client_id}.npz")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

    data = np.load(file_path, mmap_mode="r")

    # 🔥 konsisten pakai X, y
    x_train = data["X"]
    y_train = data["y"]

    # ==============================
    # VALIDASI MINIMAL (WAJIB)
    # ==============================
    if x_train.ndim != 4:
        raise ValueError(f"x_train harus 4D, dapat {x_train.shape}")

    if y_train.ndim != 1:
        raise ValueError(f"y_train harus 1D, dapat {y_train.shape}")

    return x_train, y_train


# ==============================
# LOAD VALIDATION
# ==============================
def load_validation_data() -> Tuple[np.ndarray, np.ndarray]:

    if not os.path.exists(VAL_PATH):
        raise FileNotFoundError(f"File validation tidak ditemukan: {VAL_PATH}")

    data = np.load(VAL_PATH, mmap_mode="r")

    # 🔥 konsisten
    x_val = data["X"]
    y_val = data["y"]

    return x_val, y_val


# ==============================
# LOAD TEST
# ==============================
def load_test_data() -> Tuple[np.ndarray, np.ndarray]:

    if not os.path.exists(TEST_PATH):
        raise FileNotFoundError(f"File test tidak ditemukan: {TEST_PATH}")

    data = np.load(TEST_PATH, mmap_mode="r")

    # 🔥 konsisten
    x_test = data["X"]
    y_test = data["y"]

    return x_test, y_test