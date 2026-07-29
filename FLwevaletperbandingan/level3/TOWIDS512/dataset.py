# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

import os                      # untuk manipulasi path file
import numpy as np            # untuk load file .npz
from typing import Tuple      # untuk type hint return

# ==============================
# PATH DATASET (SESUAI YANG KAMU BERIKAN)
# ==============================

# Path utama dataset hasil preprocessing
BASE_PATH = "/home/dani/Documents/tugas akhir/TugasAkhir/codeTugasAkhirku2026/tow_ids/Preprocessing/Preprocessingbaru/imgsize512lv3/norm/dwt/"

# Path untuk data test global (dipakai server)
TEST_PATH = os.path.join(BASE_PATH, "tow_ids_test_dwt.npz")

# Path untuk data validation global (dipakai server)
VAL_PATH = os.path.join(BASE_PATH, "tow_ids_eval_dwt.npz")

# Path partition IID (mode 1)
IID_PATH = os.path.join(BASE_PATH, "forFL/partition_iid")

# Path partition Non-IID (mode 2)
NONIID_PATH = os.path.join(BASE_PATH, "forFL/partition_noniid_label_skew")


# ==============================
# FUNGSI LOAD DATA CLIENT
# ==============================

def load_client_data(client_id: int, mode: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load data untuk client tertentu berdasarkan client_id dan mode distribusi.

    Parameters:
    - client_id : int → id client (0–3)
    - mode      : int → 1 = IID, 2 = Non-IID

    Return:
    - x_train, y_train
    """

    # ==============================
    # VALIDASI INPUT
    # ==============================
    if client_id not in [0, 1, 2, 3]:
        raise ValueError("client_id harus antara 0–3")

    if mode not in [1, 2]:
        raise ValueError("mode harus 1 (IID) atau 2 (Non-IID)")

    # ==============================
    # PILIH PATH BERDASARKAN MODE
    # ==============================
    if mode == 1:
        # Mode IID
        partition_path = IID_PATH
    else:
        # Mode Non-IID
        partition_path = NONIID_PATH

    # ==============================
    # SUSUN NAMA FILE BERDASARKAN CLIENT ID
    # ==============================
    file_name = f"client_{client_id}.npz"
    file_path = os.path.join(partition_path, file_name)

    # ==============================
    # LOAD DATA NPZ
    # ==============================
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

    data = np.load(file_path, mmap_mode="r")

    # ==============================
    # AMBIL DATA (ASUMSI KEY: x dan y)
    # ==============================
    x_train = data["X"]   # fitur (image)
    y_train = data["y"]   # label

    return x_train, y_train


# ==============================
# FUNGSI LOAD VALIDATION (SERVER)
# ==============================

def load_validation_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load data validation global untuk evaluasi selama training FL.

    Return:
    - x_val, y_val
    """

    if not os.path.exists(VAL_PATH):
        raise FileNotFoundError(f"File validation tidak ditemukan: {VAL_PATH}")

    data = np.load(VAL_PATH, mmap_mode="r")

    x_val = data["X"]
    y_val = data["y"]

    return x_val, y_val


# ==============================
# FUNGSI LOAD TEST (SERVER - FINAL EVALUATION)
# ==============================

def load_test_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Load data test global untuk evaluasi akhir model setelah training FL selesai.

    Return:
    - x_test, y_test
    """

    if not os.path.exists(TEST_PATH):
        raise FileNotFoundError(f"File test tidak ditemukan: {TEST_PATH}")

    data = np.load(TEST_PATH)

    x_test = data["X"]
    y_test = data["y"]

    return x_test, y_test