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
# PATH DATASET23 tow ids
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
# CONTINUAL LEARNING CONFIG
# ==============================

TARGET_CLIENT = 3          # Vehicle yang mengalami domain shift

OLD_MEMORY_RATIO = 0.25    # Replay Dataset23

MIN_CLASS_SAMPLE = 10      # Minimal replay tiap kelas


# ==============================
# PATH DATASET21
# ==============================

BASE_PATH21 = (
    "/home/dani/Documents/tugas akhir/TugasAkhir/"
    "codeTugasAkhirku2026/tow_ids/Preprocessing/"
    "Preprocessingdata21/imgsize256lv2data21/norm/dwt/"
)

TRAIN_PATH21 = os.path.join(
    BASE_PATH21,
    "tow_ids21_train_dwt.npz"
)

EVAL_PATH21 = os.path.join(
    BASE_PATH21,
    "tow_ids21_eval_dwt.npz"
)

TEST_PATH21 = os.path.join(
    BASE_PATH21,
    "tow_ids21_test_dwt.npz"
)


# ==============================
# HELPER LOAD NPZ DATASET21
# ==============================

def _load_dataset21_npz(path: str, split_name: str):
    """
    Memuat satu split Dataset21.

    Label asli Dataset21:
    0 = Normal
    1 = F_I

Remapping ke label global Dataset23 tidak dilakukan
di loader mentah ini.

Remapping dilakukan oleh:
- simulate_vehicle_memory_shift() untuk training Client 3
- load_validation_data21() untuk evaluasi Dataset21
- load_test_data21() untuk test Dataset21
    """

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File Dataset21 {split_name} tidak ditemukan: {path}"
        )

    data = np.load(
        path,
        mmap_mode="r"
    )

    x_data = data["X"]
    y_data = data["y"]

    # Dataset21 asli wajib hanya memiliki label 0 dan 1.
    labels = np.unique(y_data)

    expected_labels = np.array([0, 1])

    if not np.array_equal(labels, expected_labels):
        raise ValueError(
            f"Label Dataset21 {split_name} tidak lengkap atau tidak valid: "
            f"{labels}. Dataset21 harus memiliki [0, 1]."
        )
    return x_data, y_data


# ==============================
# LOAD DATASET21 TRAIN
# Dipakai Vehicle 3 untuk training lokal
# ==============================

def load_dataset21():
    return _load_dataset21_npz(
        TRAIN_PATH21,
        "train"
    )


# ==============================
# LOAD DATASET21 EVALUATION
# Dipakai server untuk evaluasi per round
# ==============================

def load_dataset21_eval():
    return _load_dataset21_npz(
        EVAL_PATH21,
        "evaluation"
    )


# ==============================
# LOAD DATASET21 TEST
# Dipakai hanya pada evaluasi akhir
# ==============================

def load_dataset21_test():
    return _load_dataset21_npz(
        TEST_PATH21,
        "test"
    )

# ==============================
# REMAP LABEL DATASET21 KE MODEL GLOBAL
# ==============================

def remap_dataset21_labels(
    y: np.ndarray
) -> np.ndarray:
    """
    Mengubah label Dataset21 ke label global model V1.

    Dataset21:
    0 = Normal
    1 = F_I

    Model global:
    0 = Normal
    3 = F_I
    """

    y_remap = y.copy()

    y_remap[y_remap == 1] = 3

    labels = np.unique(y_remap)

    if not np.all(np.isin(labels, [0, 3])):
        raise ValueError(
            f"Label Dataset21 setelah remap tidak valid: {labels}"
        )

    return y_remap

# ==============================
# LOAD VALIDATION DATASET21
# ==============================

def load_validation_data21() -> Tuple[np.ndarray, np.ndarray]:
    """
    Memuat Dataset21 evaluation untuk server.

    File asli:
    0 = Normal
    1 = F_I

    Output ke server:
    0 = Normal
    3 = F_I
    """

    x_val21, y_val21 = load_dataset21_eval()

    y_val21 = remap_dataset21_labels(
        y_val21
    )

    print("\n[DATASET21] Validation loaded")

    unique, counts = np.unique(
        y_val21,
        return_counts=True
    )

    for cls, count in zip(unique, counts):
        print(f"Class {cls}: {count}")

    return x_val21, y_val21


# ==============================
# LOAD TEST DATASET21
# ==============================

def load_test_data21() -> Tuple[np.ndarray, np.ndarray]:
    """
    Memuat Dataset21 test untuk evaluasi akhir.

    File asli:
    0 = Normal
    1 = F_I

    Output ke model global:
    0 = Normal
    3 = F_I
    """

    x_test21, y_test21 = load_dataset21_test()

    y_test21 = remap_dataset21_labels(
        y_test21
    )

    print("\n[DATASET21] Test loaded")

    unique, counts = np.unique(
        y_test21,
        return_counts=True
    )

    for cls, count in zip(unique, counts):
        print(f"Class {cls}: {count}")

    return x_test21, y_test21

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

    simulate_vehicle_memory_shift()

    _initialized = True

    print(
        f"[DATASET] Partition berhasil dibuat "
        f"({num_clients} client)"
    )

# ==============================
# DATASET21 CONFIG
# ==============================

MIN_FI_RATIO = 0.30
MAX_FI_RATIO = 0.50
# ==============================
# SIMULATE VEHICLE MEMORY SHIFT
# ==============================

def simulate_vehicle_memory_shift(
    client_id=TARGET_CLIENT
):

    # ==============================
    # Ambil data client
    # ==============================

    x_old, y_old = CLIENT_DATA[client_id]

    print(
        f"Client {client_id}"
    )

    print(
        x_old.shape,
        y_old.shape
    )
    memory_size = len(y_old)


    old_memory = int(
        memory_size * OLD_MEMORY_RATIO
    )

    minimum_required_replay = NUM_CLASSES * MIN_CLASS_SAMPLE

    if old_memory < minimum_required_replay:
        raise ValueError(
            f"Replay memory terlalu kecil: {old_memory}. "
            f"Minimal diperlukan {minimum_required_replay} sample "
            f"untuk {NUM_CLASSES} kelas dengan "
            f"MIN_CLASS_SAMPLE={MIN_CLASS_SAMPLE}."
        )

    new_memory = memory_size - old_memory

    print("\n========== VEHICLE MEMORY ==========")
    print(f"Total Memory      : {memory_size}")
    print(f"Replay Dataset23  : {old_memory}")
    print(f"Dataset21         : {new_memory}")


    classes = np.unique(y_old)
    print(classes)


    # ==============================
    # Hitung target replay tiap kelas
    # ==============================

    target_per_class = {}

    for cls in range(NUM_CLASSES):

        total_cls = np.sum(y_old == cls)

        target = round(
            total_cls / memory_size * old_memory
        )

        target_per_class[cls] = target

    print("\nTarget replay awal")

    for cls in range(NUM_CLASSES):

        print(
            f"Class {cls}: {target_per_class[cls]}"
        )
    # ==============================
    # Terapkan minimal replay
    # ==============================

    for cls in target_per_class:

        if target_per_class[cls] < MIN_CLASS_SAMPLE:

            target_per_class[cls] = MIN_CLASS_SAMPLE

    print("\nSetelah minimum")

    for cls in range(NUM_CLASSES):

        print(
            f"Class {cls}: {target_per_class[cls]}"
        )

    current_total = sum(
        target_per_class.values()
    )

    print()

    print(
        "Replay sekarang:",
        current_total
    )

    print(
        "Replay target:",
        old_memory
    )


    print("\nOriginal Client Distribution")

    unique, counts = np.unique(
        y_old,
        return_counts=True
    )

    for cls, cnt in zip(unique, counts):
        print(f"Class {cls}: {cnt}")
    # ==============================
    # Sesuaikan agar total replay
    # tepat sama dengan kapasitas
    # ==============================

    while sum(target_per_class.values()) > old_memory:

        # Cari kelas dengan jumlah replay terbesar
        largest_class = max(
            target_per_class,
            key=target_per_class.get
        )

        # Jangan pernah mengurangi
        # jika sudah mencapai batas minimum
        if target_per_class[largest_class] > MIN_CLASS_SAMPLE:

            target_per_class[largest_class] -= 1

        else:

            # Cari kelas terbesar berikutnya
            sorted_classes = sorted(
                target_per_class,
                key=target_per_class.get,
                reverse=True
            )

            for cls in sorted_classes:

                if target_per_class[cls] > MIN_CLASS_SAMPLE:

                    target_per_class[cls] -= 1
                    break
    while sum(target_per_class.values()) < old_memory:

        largest = max(
            target_per_class,
            key=target_per_class.get
        )

        target_per_class[largest] += 1

    print("\nReplay akhir")

    for cls in range(NUM_CLASSES):

        print(
            f"Class {cls}: {target_per_class[cls]}"
        )

    print(
        "\nTotal Replay:",
        sum(target_per_class.values())
    )
    # ==============================
    # Ambil sample replay Dataset23
    # ==============================

    replay_indices = []

    for cls in range(NUM_CLASSES):

        # Semua index milik kelas tersebut
        cls_idx = np.where(y_old == cls)[0]

        # Acak agar random
        np.random.shuffle(cls_idx)

        # Ambil sesuai target replay
        selected = cls_idx[:target_per_class[cls]]
        assert len(selected) == target_per_class[cls], (
        f"Kelas {cls} hanya memiliki "
        f"{len(selected)} sample, "
        f"target {target_per_class[cls]}"
    )


        replay_indices.extend(selected)
    print("\nReplay sample :", len(replay_indices))
    # ==============================
    # Bentuk replay dataset
    # ==============================

    replay_indices = np.array(
        replay_indices,
        dtype=np.int64
    )

    x_replay = x_old[replay_indices]
    y_replay = y_old[replay_indices]

    print("\nReplay Dataset23")

    print(
        x_replay.shape,
        y_replay.shape
    )

    for cls in range(NUM_CLASSES):

        print(
            cls,
            np.sum(y_replay == cls)
        )

    assert len(replay_indices) == len(set(replay_indices)), \
    "Replay buffer mengandung index duplikat!"


    # ==============================
    # Load Dataset21
    # ==============================

    x21, y21 = load_dataset21()
    # ==============================
    # Hitung kapasitas Dataset21
    # ==============================

    new_memory = memory_size - len(y_replay)

    print(
        f"Dataset21 yang dibutuhkan : {new_memory}"
    )
    # ==============================
    # Ambil index Dataset21
    # ==============================

    normal21_idx = np.where(y21 == 0)[0]
    fi21_idx = np.where(y21 == 1)[0]
    np.random.shuffle(normal21_idx)
    np.random.shuffle(fi21_idx)

    # ==============================
    # Proporsi Dataset21
    # ==============================

    total21 = len(y21)

    normal_target = round(
        len(normal21_idx) / total21 * new_memory
    )

    fi_target = new_memory - normal_target

    # ------------------------------
    # Pastikan F_I berada pada
    # rentang 30% - 50%
    # ------------------------------

    min_fi = int(new_memory * MIN_FI_RATIO)
    max_fi = int(new_memory * MAX_FI_RATIO)

    if fi_target < min_fi:
        fi_target = min_fi

    elif fi_target > max_fi:
        fi_target = max_fi

    normal_target = new_memory - fi_target

    assert len(fi21_idx) >= fi_target, (
        f"Dataset21 hanya memiliki {len(fi21_idx)} sampel F_I, "
        f"minimal yang dibutuhkan adalah {min_fi}."
    )

    assert len(normal21_idx) >= normal_target, (
        f"Dataset21 hanya memiliki {len(normal21_idx)} sampel Normal, "
        f"minimal yang dibutuhkan adalah {normal_target}."
    )

    # ==============================
    # Ambil Dataset21
    # ==============================

    selected21 = np.concatenate([
        normal21_idx[:normal_target],
        fi21_idx[:fi_target]
    ])
    assert len(selected21) == new_memory, (
    "Dataset21 tidak cukup "
    "memenuhi kapasitas memory."
)
    
    print("\nDataset21 Allocation")

    print(f"Normal : {normal_target}")
    print(f"F_I    : {fi_target}")

    print(
        f"F_I Ratio : {fi_target/new_memory:.2%}"
    )

    np.random.shuffle(selected21)

    x_new = x21[selected21]

    y_new = remap_dataset21_labels(
        y21[selected21]
    )


    print("\nDataset21 setelah remap")

    unique, counts = np.unique(
        y_new,
        return_counts=True
    )

    for cls, cnt in zip(unique, counts):
        print(f"Class {cls}: {cnt}")
    
    # ==============================
    # Merge Replay + Dataset21
    # ==============================

    x_final = np.concatenate([
        x_replay,
        x_new
    ])

    y_final = np.concatenate([
        y_replay,
        y_new
    ])

    # ==============================
    # Shuffle memory vehicle
    # ==============================

    perm = np.random.permutation(
        len(y_final)
    )

    x_final = x_final[perm]
    y_final = y_final[perm]

    # ==============================
    # Update memory client
    # ==============================

    CLIENT_DATA[client_id] = (
        x_final,
        y_final
    )
    assert len(y_final) == memory_size


    print("\n====================================")
    print(f"Vehicle {client_id} Memory Updated")
    print("====================================")

    unique, counts = np.unique(
        y_final,
        return_counts=True
    )

    for cls, cnt in zip(unique, counts):
        print(f"Class {cls}: {cnt}")

    print(f"Total Sample : {len(y_final)}")
    print()

    print(
        f"Replay Dataset23 : {len(y_replay)}"
    )

    print(
        f"Dataset21        : {len(y_new)}"
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