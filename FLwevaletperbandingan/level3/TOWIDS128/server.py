# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

import gc

import numpy as np                      # untuk operasi numerik (agregasi, dll)
from typing import List, Tuple          # untuk type hint agar kode lebih jelas

from model import build_model           # fungsi untuk membuat arsitektur model global
from dataset import load_validation_data  # fungsi untuk load data validation global
from strategy import fedavg_aggregate   # fungsi agregasi FedAvg (dipanggil dari strategy.py)


# ==============================
# INISIASI GLOBAL MODEL
# ==============================

# Membuat instance model global menggunakan arsitektur dari model.py
global_model = build_model()


# Mengambil bobot awal dari model global (list numpy array per layer)
global_weights = global_model.get_weights()


# ==============================
# LOAD DATA VALIDATION (SERVER)
# ==============================

# Memuat data validation global (dipakai untuk evaluasi setiap round)
x_val, y_val = load_validation_data()


# ==============================
# DEFINISI CLIENT (ID 0–3)
# ==============================

# Mendefinisikan 4 client dengan ID tetap (0 sampai 3)
# ID ini akan dipakai oleh client untuk load data masing-masing
CLIENT_IDS = [0, 1, 2, 3]


# ==============================
# FUNGSI: MEMBERIKAN GLOBAL MODEL (ON-DEMAND)
# ==============================

def get_global_weights(client_id: int) -> List[np.ndarray]:
    """
    Mengembalikan bobot global hanya ketika client dengan ID tertentu meminta.
    Tidak ada broadcast ke semua client.

    Parameters:
    - client_id : int → ID client yang meminta bobot

    Return:
    - global_weights : list numpy array (bobot tiap layer)
    """

    # Validasi bahwa client_id termasuk dalam daftar client yang aktif
    if client_id not in CLIENT_IDS:
        raise ValueError(f"Client ID {client_id} tidak valid")

    # Mengembalikan bobot global saat diminta oleh client tersebut
    return global_weights


# ==============================
# FUNGSI: MENERIMA UPDATE DARI CLIENT + AGREGASI (VIA strategy.py)
# ==============================

def aggregate_from_clients(
    client_weights: List[List[np.ndarray]],
    client_sizes: List[int]
) -> List[np.ndarray]:
    """
    Menerima bobot dari beberapa client dan melakukan agregasi FedAvg
    dengan memanggil fungsi dari strategy.py.

    Parameters:
    - client_weights : list berisi bobot dari setiap client
    - client_sizes   : list jumlah data tiap client (untuk weighted average)

    Return:
    - aggregated_weights : bobot hasil agregasi
    """

    # Memanggil fungsi FedAvg dari strategy.py
    aggregated_weights = fedavg_aggregate(client_weights, client_sizes)

    return aggregated_weights


# ==============================
# FUNGSI: UPDATE GLOBAL MODEL
# ==============================

def update_global_model(aggregated_weights: List[np.ndarray]):
    """
    Mengupdate bobot model global dengan hasil agregasi.

    Parameters:
    - aggregated_weights : bobot hasil FedAvg
    """

    global global_weights  # agar variabel global bisa diubah di dalam fungsi

    # Update variabel bobot global
    global_weights = aggregated_weights

    # Set bobot tersebut ke model global
    global_model.set_weights(global_weights)


# ==============================
# FUNGSI: EVALUASI MODEL GLOBAL
# ==============================

def evaluate_global_model() -> Tuple[float, float, float, float]:
    """
    Mengevaluasi performa model global menggunakan data validation.

    Return:
    - loss     : nilai loss pada validation
    - accuracy : nilai akurasi pada validation
    - precision : nilai precision pada validation
    - recall : nilai recall pada validation
    """
    print("\n[SERVER] Evaluasi Global Model (Validation)...")
    # Melakukan evaluasi tanpa output verbose (0 = silent)
    loss, acc, prec, rec = global_model.evaluate(x_val, y_val, verbose=1)

    return loss, acc, prec, rec


# ==============================
# FUNGSI: SATU ROUND FL (TANPA LOOP)
# ==============================

def run_one_round(client_update_fn):

    # ==============================
    # INISIALISASI STREAMING AGGREGATION
    # ==============================
    aggregated_weights = None
    total_data = 0

    # 🔴 SNAPSHOT GLOBAL (PENTING!)
    base_weights = global_model.get_weights()

    # ==============================
    # PROSES TIAP CLIENT
    # ==============================
    for client_id in CLIENT_IDS:

        # Semua client pakai weight yang sama
        updated_weights, data_size = client_update_fn(client_id, base_weights)

        # ==============================
        # STREAMING AGGREGATION
        # ==============================
        if aggregated_weights is None:
            aggregated_weights = [
                w * data_size for w in updated_weights
            ]
        else:
            for i in range(len(aggregated_weights)):
                aggregated_weights[i] += updated_weights[i] * data_size

        total_data += data_size

        # 🔴 HAPUS SEGERA (INI KRITIS)
        del updated_weights
        gc.collect()

    # ==============================
    # NORMALISASI (FEDAVG)
    # ==============================
    for i in range(len(aggregated_weights)):
        aggregated_weights[i] /= total_data

    # ==============================
    # UPDATE GLOBAL MODEL
    # ==============================
    update_global_model(aggregated_weights)

    # ==============================
    # EVALUASI
    # ==============================
    loss, acc, prec, rec = evaluate_global_model()

    print(f"[SERVER] Validation Loss: {loss:.4f} | Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f}")

    return loss, acc, prec, rec

def clear_validation_data():
    global x_val, y_val

    del x_val
    del y_val

    import gc
    gc.collect()

    print("[SERVER] Validation data dibersihkan dari RAM")