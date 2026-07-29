# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

import numpy as np                    # untuk operasi numerik pada weight
from typing import List              # untuk type hint list


# ==============================
# FUNGSI: FEDAVG AGGREGATION
# ==============================

def fedavg_aggregate(
    client_weights: List[List[np.ndarray]],
    client_sizes: List[int]
) -> List[np.ndarray]:
    """
    Melakukan agregasi bobot model dari beberapa client menggunakan metode FedAvg.

    Parameters:
    - client_weights : List dari bobot tiap client
                       (setiap elemen adalah list weight per layer)
    - client_sizes   : List jumlah data tiap client (digunakan sebagai bobot rata-rata)

    Return:
    - aggregated_weights : List bobot hasil agregasi
    """

    # ==============================
    # VALIDASI INPUT
    # ==============================

    # Pastikan jumlah client_weights dan client_sizes sama
    if len(client_weights) != len(client_sizes):
        raise ValueError("Jumlah client_weights dan client_sizes harus sama")

    # Pastikan tidak kosong
    if len(client_weights) == 0:
        raise ValueError("client_weights tidak boleh kosong")

    # ==============================
    # HITUNG TOTAL DATA
    # ==============================

    # Total seluruh data dari semua client (untuk weighted average)
    total_data = sum(client_sizes)

    # ==============================
    # INISIALISASI HASIL AGREGASI
    # ==============================

    # List kosong untuk menyimpan hasil agregasi tiap layer
    aggregated_weights = []

    # ==============================
    # LOOP PER LAYER
    # ==============================

    # Jumlah layer diambil dari client pertama
    num_layers = len(client_weights[0])

    for layer_idx in range(num_layers):

        # Ambil shape layer untuk inisialisasi array nol
        layer_shape = client_weights[0][layer_idx].shape

        # Buat array nol dengan shape yang sama
        layer_sum = np.zeros(layer_shape)

        # ==============================
        # AKUMULASI WEIGHT DARI SEMUA CLIENT
        # ==============================

        for client_idx in range(len(client_weights)):

            # Ambil weight layer dari client ke-i
            weight = client_weights[client_idx][layer_idx]

            # Ambil jumlah data client ke-i
            size = client_sizes[client_idx]

            # Hitung kontribusi weight client (weighted average)
            layer_sum += (size / total_data) * weight

        # Simpan hasil agregasi layer ini
        aggregated_weights.append(layer_sum)

    # ==============================
    # RETURN HASIL AGREGASI
    # ==============================

    return aggregated_weights