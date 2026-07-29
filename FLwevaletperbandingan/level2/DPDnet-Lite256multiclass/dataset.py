# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

import os
import numpy as np
from typing import Tuple

from config import (
    NUM_CLIENTS,
    MODE,
    RANDOM_SEED,
    DIRICHLET_ALPHA
)
# ==============================
# PATH DATASET
# ==============================

BASE_PATH = "/home/dani/Documents/tugas akhir/TugasAkhir/codeTugasAkhirku2026/tow_ids/Preprocessing/Preprocessingbaru/imgsize256lv3multiclass/norm/dwt/"

TRAIN_PATH = os.path.join(
    BASE_PATH,
    "tow_ids_train_dwt.npz"
)

VAL_PATH = os.path.join(
    BASE_PATH,
    "tow_ids_eval_dwt.npz"
)

TEST_PATH = os.path.join(
    BASE_PATH,
    "tow_ids_test_dwt.npz"
)

NUM_CLASSES = 6

# ==============================
# STORAGE PARTITION CLIENT
# ==============================

CLIENT_DATA = {}

_initialized = False

# ==============================
# MEMBUAT PARTITION CLIENT
# ==============================

def initialize_partitions(
    num_clients=None,
    mode=None
):
    """
    Membagi dataset train menjadi beberapa client.
    Saat ini hanya mendukung IID.
    """

    global CLIENT_DATA
    global _initialized

    if _initialized:
        return

    if num_clients is None:
        num_clients = NUM_CLIENTS

    if mode is None:
        mode = MODE

    # ==============================
    # LOAD TRAIN DATA
    # ==============================

    if not os.path.exists(TRAIN_PATH):
        raise FileNotFoundError(TRAIN_PATH)

    data = np.load(
        TRAIN_PATH,
        mmap_mode="r"
    )

    X = data["X"]
    y = data["y"]

    # ==============================
    # MODE IID
    # ==============================

    if mode == 1:

        np.random.seed(RANDOM_SEED)

        indices = np.arange(len(y))

        np.random.shuffle(indices)

        split_indices = np.array_split(
            indices,
            num_clients
        )

        CLIENT_DATA.clear()

        for client_id, idx in enumerate(split_indices):

            CLIENT_DATA[client_id] = (
                X[idx].copy(),
                y[idx].copy()
            )

    # ==============================
    # MODE NON-IID (Vehicle-like)
    # ==============================
    # ==============================
    # MODE NON-IID (Realistic IoV)
    # ==============================
    # ==============================
    # MODE NON-IID (Realistic IoV)
    # ==============================
    elif mode == 2:

        np.random.seed(RANDOM_SEED)

        CLIENT_DATA.clear()

        # ==========================================================
        # Kelompokkan index tiap kelas
        # ==========================================================

        class_indices = {
            c: np.where(y == c)[0]
            for c in range(NUM_CLASSES)
        }

        for c in class_indices:
            np.random.shuffle(class_indices[c])

        # ==========================================================
        # Storage
        # ==========================================================

        client_idx = [[] for _ in range(num_clients)]

        # ==========================================================
        # NORMAL
        # Dibagi hampir merata
        # ==========================================================

        normal_idx = class_indices[0]

        normal_split = np.array_split(
            normal_idx,
            num_clients
        )

        for cid in range(num_clients):
            client_idx[cid].extend(
                normal_split[cid]
            )

        # ==========================================================
        # ATTACK
        # ==========================================================

        alpha = DIRICHLET_ALPHA

        MIN_ATTACK = 10

        for cls in range(1, NUM_CLASSES):

            idx = class_indices[cls]

            np.random.shuffle(idx)

            total_cls = len(idx)

            # ------------------------------------------------------
            # Minimal data tiap client
            # ------------------------------------------------------

            if total_cls >= MIN_ATTACK * num_clients:

                counts = np.full(
                    num_clients,
                    MIN_ATTACK,
                    dtype=int
                )

                remaining = total_cls - counts.sum()

            else:

                counts = np.zeros(
                    num_clients,
                    dtype=int
                )

                counts[:total_cls] = 1

                remaining = 0

            # ------------------------------------------------------
            # Dirichlet
            # ------------------------------------------------------
            ATTACK_ALPHA = {
                    1: 0.8,  
                    2: 0.5,  
                    3: 0.3,
                    4: 0.6,  
                    5: 0.2   
                }
            if remaining > 0:

                proportions = np.random.dirichlet(
                    np.repeat(ATTACK_ALPHA.get(cls, DIRICHLET_ALPHA), num_clients)
                )

                extra = np.floor(
                    proportions * remaining
                ).astype(int)

                diff = remaining - extra.sum()

                if diff > 0:

                    order = np.argsort(-proportions)

                    for i in range(diff):
                        extra[
                            order[i % num_clients]
                        ] += 1

                counts += extra

            # ------------------------------------------------------
            # Safety
            # ------------------------------------------------------

            assert counts.sum() == total_cls

            # ------------------------------------------------------
            # Distribusi
            # ------------------------------------------------------

            start = 0

            for cid in range(num_clients):

                end = start + counts[cid]

                client_idx[cid].extend(
                    idx[start:end]
                )

                start = end

        # ==========================================================
        # VALIDASI
        # ==========================================================

        used = 0

        all_index = []

        for cid in range(num_clients):

            idx = np.array(
                client_idx[cid],
                dtype=np.int64
            )

            np.random.shuffle(idx)

            CLIENT_DATA[cid] = (
                X[idx],
                y[idx]
            )

            used += len(idx)

            all_index.extend(idx.tolist())

        # ==========================================================
        # PENGAMAN
        # ==========================================================

        assert used == len(y), (
            f"Sample hilang! {used}/{len(y)}"
        )

        assert len(all_index) == len(set(all_index)), (
            "Ada sample yang duplikat!"
        )

        print(
            f"[CHECK] Semua sample digunakan: {used}"
        )


    else:

        raise ValueError(
            "MODE harus 1 atau 2."
        )

    _initialized = True

    print(
        f"[DATASET] Partition berhasil dibuat "
        f"({num_clients} client)"
    )

# ==============================
# LOAD DATA CLIENT
# ==============================

def load_client_data(
    client_id: int
) -> Tuple[np.ndarray, np.ndarray]:

    if not _initialized:
        raise RuntimeError(
            "initialize_partitions() belum dipanggil."
        )

    if client_id not in CLIENT_DATA:
        raise ValueError(
            f"Client {client_id} tidak ditemukan."
        )

    x_train, y_train = CLIENT_DATA[client_id]

    labels = np.unique(y_train)

    if np.any(labels < 0) or np.any(labels >= NUM_CLASSES):
        raise ValueError(
            f"Label client tidak valid: {labels}"
        )

    return x_train, y_train

# ==============================
# LOAD VALIDATION
# ==============================

def load_validation_data() -> Tuple[np.ndarray, np.ndarray]:

    if not os.path.exists(VAL_PATH):
        raise FileNotFoundError(VAL_PATH)

    data = np.load(
        VAL_PATH,
        mmap_mode="r"
    )

    x_val = data["X"]
    y_val = data["y"]

    labels = np.unique(y_val)

    if np.any(labels < 0) or np.any(labels >= NUM_CLASSES):
        raise ValueError(
            f"Validation label tidak valid: {labels}"
        )

    return x_val, y_val

# ==============================
# LOAD TEST
# ==============================

def load_test_data() -> Tuple[np.ndarray, np.ndarray]:

    if not os.path.exists(TEST_PATH):
        raise FileNotFoundError(TEST_PATH)

    data = np.load(TEST_PATH)

    x_test = data["X"]
    y_test = data["y"]

    labels = np.unique(y_test)

    if np.any(labels < 0) or np.any(labels >= NUM_CLASSES):
        raise ValueError(
            f"Test label tidak valid: {labels}"
        )

    return x_test, y_test