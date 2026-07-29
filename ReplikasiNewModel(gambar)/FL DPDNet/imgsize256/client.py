# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

import numpy as np                      # untuk manipulasi array
import gc                               # untuk membantu pembersihan RAM
import tensorflow as tf
from model import build_model           # untuk membuat model lokal
from dataset import load_client_data    # untuk load data sesuai client_id


mode = 2  # 1 = IID, 2 = non-IID

# ==============================
# FUNGSI: TRAINING CLIENT
# ==============================

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
    x_train, y_train = load_client_data(client_id=client_id, mode=mode)

    # Ambil jumlah data untuk keperluan FedAvg (weighted aggregation)
    data_size = len(x_train)

    print(f"[CLIENT {client_id}] Data loaded: {data_size} samples")

    # ==============================
    # INISIASI MODEL LOKAL
    # ==============================

    # Membuat model baru (arsitektur sama dengan global)
    model = build_model()

    # Set bobot model lokal dengan bobot global dari server
    model.set_weights(global_weights)

    # ==============================
    # TRAINING (1 EPOCH)
    # ==============================

    # Training model menggunakan data lokal client
    model.fit(
        x_train,
        y_train,
        epochs=3,        # hanya 1 epoch sesuai instruksi
        batch_size=16,   # bisa kamu ubah jika perlu
        verbose=1        # tampilkan progress training
    )

    # ==============================
    # SIMPAN HASIL TRAINING (WEIGHTS)
    # ==============================

    # Ambil bobot hasil training untuk dikirim ke server
    updated_weights = model.get_weights()

    # ==============================
    # BERSIHKAN MEMORI (RAM)
    # ==============================

    # Hapus data train dari memori
    del x_train
    del y_train

    # Hapus model lokal (tidak dipakai lagi setelah ambil weight)
    del model
    tf.keras.backend.clear_session()
    # Paksa garbage collector untuk membebaskan RAM
    gc.collect()

    print(f"[CLIENT {client_id}] Training selesai & memori dibersihkan")

    # ==============================
    # RETURN KE SERVER
    # ==============================

    return updated_weights, data_size