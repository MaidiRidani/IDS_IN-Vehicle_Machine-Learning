# ==========================================================
# IMPORT
# ==========================================================

import os
import numpy as np

from typing import Tuple

from config import (
    NUM_CLIENTS,
    MODE,
    RANDOM_SEED,
    DIRICHLET_ALPHA,
)

# ==========================================================
# GLOBAL CONFIG
# ==========================================================

NUM_CLASSES = 8

CLASS_NAMES = [
    "Normal23",
    "C_D",
    "P_I",
    "F_I23",
    "M_F",
    "C_R",
    "Normal21",
    "F_I21",
]

TARGET_CLIENT = 3

CLIENT_DATA = {}

_initialized = False

# ==========================================================
# DATASET23
# ==========================================================

BASE_PATH23 = (
    "/home/dani/Documents/tugas akhir/TugasAkhir/"
    "codeTugasAkhirku2026/tow_ids/"
    "Preprocessing/Preprocessingbaru/"
    "imgsize256lv2multiclass/norm/dwt/"
)

TRAIN_PATH23 = os.path.join(
    BASE_PATH23,
    "tow_ids_train_dwt.npz"
)

VAL_PATH23 = os.path.join(
    BASE_PATH23,
    "tow_ids_eval_dwt.npz"
)

TEST_PATH23 = os.path.join(
    BASE_PATH23,
    "tow_ids_test_dwt.npz"
)

# ==========================================================
# DATASET21
# ==========================================================

BASE_PATH21 = (
    "/home/dani/Documents/tugas akhir/TugasAkhir/"
    "codeTugasAkhirku2026/tow_ids/"
    "Preprocessing/Preprocessingdata21/"
    "imgsize256lv2data21/norm/dwt/"
)

TRAIN_PATH21 = os.path.join(
    BASE_PATH21,
    "tow_ids21_train_dwt.npz"
)

VAL_PATH21 = os.path.join(
    BASE_PATH21,
    "tow_ids21_eval_dwt.npz"
)

TEST_PATH21 = os.path.join(
    BASE_PATH21,
    "tow_ids21_test_dwt.npz"
)

# ==========================================================
# NPZ LOADER
# ==========================================================

def load_npz(path: str) -> Tuple[np.ndarray, np.ndarray]:

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    data = np.load(
        path,
        mmap_mode="r"
    )

    X = data["X"]
    y = data["y"]

    return X, y


# ==========================================================
# DATASET23
# ==========================================================

def load_dataset23_train():

    return load_npz(TRAIN_PATH23)


def load_dataset23_validation():

    return load_npz(VAL_PATH23)


def load_dataset23_test():

    return load_npz(TEST_PATH23)


# ==========================================================
# DATASET21
# ==========================================================

def load_dataset21_train():

    return load_npz(TRAIN_PATH21)


def load_dataset21_validation():

    return load_npz(VAL_PATH21)


def load_dataset21_test():

    return load_npz(TEST_PATH21)


# ==========================================================
# REMAP DATASET21
#
# Dataset21 asli
#
# 0 = Normal
# 1 = F_I
#
# Menjadi
#
# 6 = Normal21
# 7 = F_I21
# ==========================================================

def remap_dataset21_labels(
    y: np.ndarray
) -> np.ndarray:

    y = y.copy()

    y_new = np.full_like(
        y,
        fill_value=-1
    )

    y_new[y == 0] = 6
    y_new[y == 1] = 7

    if np.any(y_new == -1):

        unknown = np.unique(
            y[y_new == -1]
        )

        raise ValueError(
            f"Unknown Dataset21 labels: {unknown}"
        )

    return y_new.astype(np.int32)


# ==========================================================
# VALIDATION DATASET21
# (Server Evaluation)
# ==========================================================

def load_validation_data21():

    X, y = load_dataset21_validation()

    y = remap_dataset21_labels(y)

    return X, y


# ==========================================================
# TEST DATASET21
# ==========================================================

def load_test_data21():

    X, y = load_dataset21_test()

    y = remap_dataset21_labels(y)

    return X, y


# ==========================================================
# SANITY CHECK
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CHECK DATASET23")
    print("=" * 60)

    X23, y23 = load_dataset23_train()

    print(X23.shape)
    print(np.unique(y23, return_counts=True))

    print()

    print("=" * 60)
    print("CHECK DATASET21")
    print("=" * 60)

    X21, y21 = load_dataset21_train()

    y21 = remap_dataset21_labels(y21)

    print(X21.shape)
    print(np.unique(y21, return_counts=True))



    # ==========================================================
# INITIALIZE PARTITIONS
# ==========================================================

def initialize_partitions(
    num_clients=None,
    mode=None,
):

    global CLIENT_DATA
    global _initialized

    if _initialized:
        return

    if num_clients is None:
        num_clients = NUM_CLIENTS

    if mode is None:
        mode = MODE

    np.random.seed(RANDOM_SEED)

    CLIENT_DATA.clear()

    # ======================================================
    # LOAD DATASET23
    # ======================================================

    X, y = load_dataset23_train()

    print("\n")
    print("=" * 60)
    print("LOAD DATASET23")
    print("=" * 60)

    print("Shape :", X.shape)
    print("Label :", np.unique(y))

    # ======================================================
    # IID
    # ======================================================

    if mode == 1:

        print("\nMode : IID")

        indices = np.arange(len(y))

        np.random.shuffle(indices)

        split_indices = np.array_split(
            indices,
            num_clients
        )

        for cid, idx in enumerate(split_indices):

            CLIENT_DATA[cid] = {

                "x": X[idx].copy(),

                "y": y[idx].copy(),

                "manifest": None

            }

    # ======================================================
    # NON IID
    # ======================================================

    elif mode == 2:

        print("\nMode : NON IID")

        class_indices = {}

        for cls in range(6):

            idx = np.where(y == cls)[0]

            np.random.shuffle(idx)

            class_indices[cls] = idx

        client_indices = [

            [] for _ in range(num_clients)

        ]

        # --------------------------------------------------
        # NORMAL
        # --------------------------------------------------

        normal_split = np.array_split(

            class_indices[0],

            num_clients

        )

        for cid in range(num_clients):

            client_indices[cid].extend(

                normal_split[cid]

            )

        # --------------------------------------------------
        # ATTACK
        # --------------------------------------------------

        ATTACK_ALPHA = {

            1: 0.8,

            2: 0.5,

            3: 0.3,

            4: 0.6,

            5: 0.2,

        }

        MIN_SAMPLE = 10

        for cls in range(1, 6):

            idx = class_indices[cls]

            total = len(idx)

            if total >= MIN_SAMPLE * num_clients:

                counts = np.full(

                    num_clients,

                    MIN_SAMPLE,

                    dtype=int

                )

                remain = total - counts.sum()

            else:

                counts = np.zeros(

                    num_clients,

                    dtype=int

                )

                counts[:total] = 1

                remain = 0

            if remain > 0:

                alpha = ATTACK_ALPHA.get(

                    cls,

                    DIRICHLET_ALPHA

                )

                prop = np.random.dirichlet(

                    np.repeat(alpha, num_clients)

                )

                extra = np.floor(

                    prop * remain

                ).astype(int)

                diff = remain - extra.sum()

                if diff > 0:

                    order = np.argsort(-prop)

                    for i in range(diff):

                        extra[
                            order[i % num_clients]
                        ] += 1

                counts += extra

            assert counts.sum() == total

            start = 0

            for cid in range(num_clients):

                end = start + counts[cid]

                client_indices[cid].extend(

                    idx[start:end]

                )

                start = end

        # --------------------------------------------------
        # SIMPAN
        # --------------------------------------------------

        used = []

        for cid in range(num_clients):

            idx = np.array(

                client_indices[cid],

                dtype=np.int64

            )

            np.random.shuffle(idx)

            CLIENT_DATA[cid] = {

                "x": X[idx].copy(),

                "y": y[idx].copy(),

                "manifest": None

            }

            used.extend(idx.tolist())

        assert len(used) == len(set(used))

        assert len(used) == len(y)

    else:

        raise ValueError(

            "MODE harus 1 atau 2"

        )
        # ======================================================
    # Tambahkan Dataset21 ke Client 3
    # ======================================================

    inject_dataset21_to_client(
        client_id=TARGET_CLIENT
    )

    # ======================================================
    # Buat manifest masing-masing client
    # ======================================================

    build_client_manifest()

    _initialized = True

    print()

    print("=" * 60)
    print("PARTITION SELESAI")
    print("=" * 60)

    # ======================================================
    # RINGKASAN DATASET23
    # ======================================================

    print("\n")
    print("=" * 60)
    print("PARTITION DATASET23")
    print("=" * 60)

    for cid in range(num_clients):

        y_client = CLIENT_DATA[cid]["y"]

        unique, counts = np.unique(

            y_client,

            return_counts=True

        )

        print(f"\nClient {cid}")

        for c, n in zip(unique, counts):

            print(f"Class {c} : {n}")

    print()
# ==========================================================
# ADD DATASET21 TO TARGET CLIENT
# ==========================================================

def inject_dataset21_to_client(
    client_id=TARGET_CLIENT
):

    print("\n")
    print("=" * 60)
    print("ADD DATASET21")
    print("=" * 60)

    # ------------------------------------------------------
    # Load Dataset21
    # ------------------------------------------------------

    X21, y21 = load_dataset21_train()

    y21 = remap_dataset21_labels(y21)

    print("Dataset21")
    print("Shape :", X21.shape)

    unique, counts = np.unique(
        y21,
        return_counts=True
    )

    for cls, cnt in zip(unique, counts):

        print(
            f"Class {cls} : {cnt}"
        )

    # ------------------------------------------------------
    # Ambil client target
    # ------------------------------------------------------

    client = CLIENT_DATA[client_id]

    X_old = client["x"]
    y_old = client["y"]

    print("\nClient sebelum injection")

    unique, counts = np.unique(
        y_old,
        return_counts=True
    )

    for cls, cnt in zip(unique, counts):

        print(
            f"Class {cls} : {cnt}"
        )

    # ------------------------------------------------------
    # Merge
    # ------------------------------------------------------

    X_merge = np.concatenate(
        [
            X_old,
            X21
        ],
        axis=0
    )

    y_merge = np.concatenate(
        [
            y_old,
            y21
        ],
        axis=0
    )

    # ------------------------------------------------------
    # Shuffle
    # ------------------------------------------------------

    perm = np.random.permutation(
        len(y_merge)
    )

    X_merge = X_merge[perm]

    y_merge = y_merge[perm]

    CLIENT_DATA[client_id]["x"] = X_merge

    CLIENT_DATA[client_id]["y"] = y_merge

    print("\nClient sesudah injection")

    unique, counts = np.unique(
        y_merge,
        return_counts=True
    )

    for cls, cnt in zip(unique, counts):

        print(
            f"Class {cls} : {cnt}"
        )

    print()

    print(
        "Total sample :",
        len(y_merge)
    )
    assert np.all(np.isin(
    np.unique(y_merge),
    np.arange(NUM_CLASSES)
    ))


# ==========================================================
# BUILD MANIFEST
# ==========================================================

def build_client_manifest():

    print("\n")
    print("=" * 60)
    print("BUILD CLIENT MANIFEST")
    print("=" * 60)

    for cid in CLIENT_DATA:

        manifest = np.unique(

            CLIENT_DATA[cid]["y"]

        ).astype(np.int32)

        CLIENT_DATA[cid]["manifest"] = manifest

        print(

            f"Client {cid} -> {manifest}"

        )

# ======================================================
# LOAD DATA CLIENT
# ======================================================

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

    return (

        CLIENT_DATA[client_id]["x"],

        CLIENT_DATA[client_id]["y"]

    )

# ======================================================
# LOAD CLIENT MANIFEST
# ======================================================

def load_client_manifest(
    client_id: int
) -> np.ndarray:

    if client_id not in CLIENT_DATA:

        raise ValueError(
            f"Client {client_id} tidak ditemukan."
        )

    return CLIENT_DATA[client_id]["manifest"]


# ======================================================
# LOAD VALIDATION
# ======================================================

def load_validation_data():

    x23, y23 = load_dataset23_validation()

    x21, y21 = load_dataset21_validation()
    y21 = remap_dataset21_labels(y21)

    x = np.concatenate([

        x23,

        x21

    ])

    y = np.concatenate([

        y23,

        y21

    ])
    x = np.concatenate([x23, x21])
    y = np.concatenate([y23, y21])

    perm = np.random.permutation(len(y))

    x = x[perm]
    y = y[perm]
    print()

    print("=" * 60)
    print("VALIDATION SET")
    print("=" * 60)

    unique, counts = np.unique(
        y,
        return_counts=True
    )

    for cls, cnt in zip(unique, counts):

        print(
            f"Class {cls}: {cnt}"
        )

    return x, y

# ======================================================
# LOAD TEST
# ======================================================

def load_test_data():

    x23, y23 = load_dataset23_test()

    x21, y21 = load_dataset21_test()

    y21 = remap_dataset21_labels(y21)

    x = np.concatenate([

        x23,

        x21

    ])

    y = np.concatenate([

        y23,

        y21

    ])

    print()

    print("=" * 60)
    print("TEST SET")
    print("=" * 60)

    unique, counts = np.unique(
        y,
        return_counts=True
    )

    for cls, cnt in zip(unique, counts):

        print(
            f"Class {cls}: {cnt}"
        )

    return x, y

# ======================================================
# DEBUG DISTRIBUSI CLIENT
# ======================================================

def print_client_summary():

    print()

    print("=" * 70)
    print("CLIENT SUMMARY")
    print("=" * 70)

    for cid in sorted(CLIENT_DATA.keys()):

        y = CLIENT_DATA[cid]["y"]

        manifest = CLIENT_DATA[cid]["manifest"]

        print()

        print(f"Client {cid}")

        print("Manifest :", manifest)

        unique, counts = np.unique(
            y,
            return_counts=True
        )

        for cls, cnt in zip(unique, counts):

            print(
                f"Class {cls}: {cnt}"
            )


