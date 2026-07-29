# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

import numpy as np                      # untuk manipulasi array
import gc                               # untuk membantu pembersihan RAM
import tensorflow as tf
from model import build_model           # untuk membuat model lokal
from dataset import load_client_data    # untuk load data sesuai client_id
from config import BATCH_SIZE


# ==============================
# FUNGSI: TRAINING CLIENT
# ==============================
# ==============================
# MODEL PERMANEN UNTUK SETIAP CLIENT
# ==============================

from config import NUM_CLIENTS

CLIENT_MODELS = {
    client_id: build_model()
    for client_id in range(NUM_CLIENTS)
}
def client_update_fn(client_id: int, global_weights):
    """
    Fungsi yang dipanggil server untuk melakukan training di client tertentu.

    Parameters:
    - client_id      : int → ID client (0–3)
    - global_weights : bobot global dari server

    Return:
    - updated_weights : bobot hasil training client
    - data_size       : jumlah data yang digunakan client
    """

    print(f"\n[CLIENT {client_id}] Memulai training...")

    # ==============================
    # LOAD DATA SESUAI CLIENT ID
    # ==============================

    # Load data train sesuai client_id (tidak load semua client sekaligus)
    x_train, y_train = load_client_data(client_id=client_id)

    # Ambil jumlah data untuk keperluan FedAvg (weighted aggregation)
    data_size = len(x_train)

    print(f"[CLIENT {client_id}] Data loaded: {data_size} samples")

    # ==============================
    # TAMPILKAN DISTRIBUSI LABEL
    # ==============================

    unique, counts = np.unique(y_train, return_counts=True)

    print(f"[CLIENT {client_id}] Label distribution:")

    for u, c in zip(unique, counts):
        print(f"  Class {u}: {c}")

    # ==============================
    # INISIASI MODEL LOKAL
    # ==============================

    # Membuat model baru (arsitektur sama dengan global)
    # model = build_model()

    # Set bobot model lokal dengan bobot global dari server
    client_model = CLIENT_MODELS[client_id]

    client_model.set_weights(global_weights)

    # ==============================
    # TRAINING (1 EPOCH)
    # ==============================

    # Training model menggunakan data lokal client
    # model.fit(
    #     x_train,
    #     y_train,
    #     epochs=1,        # hanya 1 epoch sesuai instruksi
    #     batch_size=16,   # bisa kamu ubah jika perlu
    #     verbose=1        # tampilkan progress training
    # )
    train_ds = tf.data.Dataset.from_tensor_slices(
        (x_train, y_train)
    ).batch(BATCH_SIZE)

    client_model.fit(
        train_ds,
        epochs=1,
        verbose=1
    )
    # ==============================
    # SIMPAN HASIL TRAINING (WEIGHTS)
    # ==============================

    # Ambil bobot hasil training untuk dikirim ke server
    updated_weights = client_model.get_weights()

    # ==============================
    # BERSIHKAN MEMORI (RAM)
    # ==============================

# Bersihkan data training saja
    del x_train
    del y_train
    del train_ds

    gc.collect()

    print(f"[CLIENT {client_id}] Training selesai & memori dibersihkan")

    # ==============================
    # RETURN KE SERVER
    # ==============================

    return updated_weights, data_size