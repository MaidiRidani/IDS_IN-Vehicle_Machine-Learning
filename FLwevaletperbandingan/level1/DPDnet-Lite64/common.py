# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

import tensorflow as tf
import numpy as np                                  # operasi numerik
import pandas as pd                                 # simpan ke CSV
from sklearn.metrics import confusion_matrix         # hitung TN, FP, FN, TP
import os


# ==============================
# FUNGSI: HITUNG FPR DAN FNR
# ==============================

def calculate_fpr_fnr(y_true, y_pred):
    """
    Menghitung False Positive Rate (FPR) dan False Negative Rate (FNR)

    Parameters:
    - y_true : label asli
    - y_pred : hasil prediksi (binary 0/1)

    Return:
    - fpr, fnr
    """

    # Pastikan bentuk data 1D
    y_true = y_true.flatten()
    y_pred = y_pred.flatten()

    # Ambil confusion matrix: [[TN, FP], [FN, TP]]
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    # Hitung FPR (False Positive Rate)
    fpr = fp / (fp + tn) if (fp + tn) != 0 else 0.0

    # Hitung FNR (False Negative Rate)
    fnr = fn / (fn + tp) if (fn + tp) != 0 else 0.0

    return fpr, fnr


# ==============================
# FUNGSI: FINAL MODEL (WRAPPER)
# ==============================

def calculate_final_metrics(y_true, y_pred):
    """
    Wrapper untuk final model (secara logika sama, hanya untuk konsistensi naming)

    Return:
    - fpr, fnr
    """

    return calculate_fpr_fnr(y_true, y_pred)


# ==============================
# FUNGSI: BEST MODEL (WRAPPER)
# ==============================

def calculate_best_metrics(y_true, y_pred):
    """
    Wrapper untuk best model (identik dengan final, hanya beda konteks)

    Return:
    - fpr, fnr
    """

    return calculate_fpr_fnr(y_true, y_pred)

# fungsi helper untuk ambil mode dari client.py (untuk keperluan penamaan file hasil test)
def get_mode_from_client():
    """
    Mengambil MODE dari client.py (lazy import untuk hindari circular import)
    """
    from client import mode
    return mode

# ==============================
# FUNGSI: SIMPAN HASIL TEST KE CSV
# ==============================

def save_test_results_to_csv(
    final_metrics: dict,
    best_metrics: dict,
    fnr_metrics: dict,
    filename: str = None
):
    """
    Menyimpan hasil test ke folder 'trainingsave' dengan nama file otomatis berdasarkan MODE
    """

    # ==============================
    # AMBIL MODE DARI CLIENT
    # ==============================
    mode = get_mode_from_client()

    if mode == 1:
        mode_name = "iid"
    elif mode == 2:
        mode_name = "noniid"
    else:
        mode_name = f"mode{mode}"

    # ==============================
    # FOLDER OUTPUT
    # ==============================
    folder = "trainingsave"
    os.makedirs(folder, exist_ok=True)  # buat folder jika belum ada

    # ==============================
    # AUTO NAMA FILE
    # ==============================
    if filename is None:
        filename = f"test_results_{mode_name}.csv"

    # Gabungkan dengan folder
    full_path = os.path.join(folder, filename)

    # ==============================
    # VALIDASI KEY
    # ==============================
    required_keys = ["loss", "accuracy", "precision", "recall", "f1", "fpr", "fnr"]

    for key in required_keys:
        if key not in final_metrics:
            raise ValueError(f"final_metrics missing key: {key}")
        if key not in best_metrics:
            raise ValueError(f"best_metrics missing key: {key}")

    # ==============================
    # DATAFRAME
    # ==============================
    data = [
        {"type": "final_model", **final_metrics},
        {"type": "best_f1_model", **best_metrics},
        {"type": "best_fnr_model", **fnr_metrics}
    ]

    df = pd.DataFrame(data)

    df = df[["type", "loss", "accuracy", "precision", "recall", "f1", "fpr", "fnr"]]

    # ==============================
    # SIMPAN
    # ==============================
    df.to_csv(full_path, index=False)

    print(f"[INFO] Hasil test disimpan ke {full_path}")

    return df


# ==============================
# FUNGSI: HITUNG F1-SCORE
# ==============================

def calculate_f1(precision, recall):
    """
    Menghitung F1-score dari precision dan recall
    """

    if (precision + recall) == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)

# ==============================
# IMPORT TAMBAHAN
# ==============================




# ==============================
# FUNGSI: SIMPAN MODEL
# ==============================

def save_model(model, path: str):
    """
    Menyimpan model ke path tertentu

    Parameters:
    - model : model keras (tf.keras.Model)
    - path  : lokasi file (contoh: saved_models/model_final.h5)
    """

    # Ambil folder dari path
    folder = os.path.dirname(path)

    # Jika folder belum ada → buat
    if folder != "":
        os.makedirs(folder, exist_ok=True)

    # Simpan model
    model.save(path)

    print(f"[INFO] Model disimpan di: {path}")


# ==============================
# FUNGSI: SIMPAN MODEL FINAL
# ==============================

def save_final_model(model):
    """
    Simpan model terakhir (final model) dengan nama sesuai MODE
    """

    mode = get_mode_from_client()
    mode_name = "iid" if mode == 1 else "noniid"

    path = f"saved_models/model_final_{mode_name}.h5"

    save_model(model, path)


# ==============================
# FUNGSI: SIMPAN MODEL TERBAIK
# ==============================

def save_best_model(model, best_weights):
    """
    Simpan model terbaik berdasarkan weights terbaik (overwrite, dengan nama sesuai MODE)
    """

    if best_weights is None:
        print("[WARNING] Tidak ada best_weights, model terbaik tidak disimpan")
        return

    # Ambil MODE dari client (lazy import biar aman)
    mode = get_mode_from_client()
    mode_name = "iid" if mode == 1 else "noniid"

    # Set weight terbaik ke model (sesuai keinginan kamu)
    model.set_weights(best_weights)

    # Simpan model (overwrite, tapi beda nama per mode)
    save_model(model, f"saved_models/model_best_{mode_name}.h5")


def save_best_fnr_model(model, best_weights_fnr):
    """
    Simpan model terbaik berdasarkan recall tertinggi / FNR terendah
    """

    if best_weights_fnr is None:
        print("[WARNING] Tidak ada best_weights_fnr")
        return

    mode = get_mode_from_client()
    mode_name = "iid" if mode == 1 else "noniid"

    model.set_weights(best_weights_fnr)

    save_model(
        model,
        f"saved_models/model_best_fnr_{mode_name}.h5"
    )



def init_training_history_file(filename: str = None):
    """
    Membuat file CSV kosong dengan header (sekali di awal training)
    """

    mode = get_mode_from_client()

    if mode == 1:
        mode_name = "iid"
    elif mode == 2:
        mode_name = "noniid"
    else:
        mode_name = f"mode{mode}"

    folder = "trainingsave"
    os.makedirs(folder, exist_ok=True)

    if filename is None:
        filename = f"training_history_{mode_name}.csv"

    full_path = os.path.join(folder, filename)

    # ==============================
    # BUAT FILE + HEADER
    # ==============================
    with open(full_path, "w") as f:
        f.write("round,loss,accuracy,precision,recall,f1\n")

    print(f"[INFO] File history dibuat: {full_path}")

    return full_path

def append_training_history(file_path, round_num, loss, acc, prec, rec, f1):

    """
    Menambahkan 1 baris hasil training ke CSV
    """

    with open(file_path, "a") as f:
        f.write(f"{round_num},{loss},{acc},{prec},{rec},{f1}\n")







def init_experiment_note():
    """
    Membuat file note.txt berdasarkan mode
    """
    mode = get_mode_from_client()

    if mode == 1:
        mode_name = "iid"
    elif mode == 2:
        mode_name = "noniid"
    else:
        mode_name = f"mode{mode}"

    folder = "trainingsave"
    os.makedirs(folder, exist_ok=True)

    filename = f"note_{mode_name}.txt"
    full_path = os.path.join(folder, filename)

    with open(full_path, "w") as f:
        f.write("===== EXPERIMENT NOTE =====\n")

    print(f"[INFO] Note file dibuat: {full_path}")

    return full_path

def write_experiment_config(note_path, num_rounds):
    mode = get_mode_from_client()

    if mode == 1:
        mode_name = "IID"
    elif mode == 2:
        mode_name = "NON-IID"
    else:
        mode_name = f"MODE-{mode}"

    with open(note_path, "a") as f:
        f.write("\n--- CONFIG ---\n")
        f.write(f"Mode   : {mode_name}\n")
        f.write(f"Rounds : {num_rounds}\n")

def write_model_info(note_path, model):

    total_params = model.count_params()
    trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    non_trainable_params = sum([tf.keras.backend.count_params(w) for w in model.non_trainable_weights])

    size_bytes, size_kb, size_mb = get_model_size(model)

    with open(note_path, "a") as f:
        f.write("\n--- MODEL INFO ---\n")
        f.write(f"Total Params          : {total_params}\n")
        f.write(f"Trainable Params      : {trainable_params}\n")
        f.write(f"Non-trainable Params  : {non_trainable_params}\n")
        f.write(f"Model Size (bytes)    : {size_bytes}\n")
        f.write(f"Model Size (KB)       : {size_kb:.2f}\n")
        f.write(f"Model Size (MB)       : {size_mb:.2f}\n")

def write_final_results(
    note_path,
    final_metrics,
    best_metrics,
    fnr_metrics
):
    with open(note_path, "a") as f:
        f.write("\n--- FINAL RESULTS ---\n")

        f.write("\n[FINAL MODEL]\n")
        for k, v in final_metrics.items():
            f.write(f"{k}: {v}\n")

        f.write("\n[BEST MODEL]\n")
        for k, v in best_metrics.items():
            f.write(f"{k}: {v}\n")
        f.write("\n[BEST FNR MODEL]\n")
        for k, v in fnr_metrics.items():
            f.write(f"{k}: {v}\n")


import tempfile
import os
import tensorflow as tf

import tempfile
import os

def get_model_size(model):
    with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
        model.save(tmp.name)   # 🔥 TANPA save_format
        size_bytes = os.path.getsize(tmp.name)

    os.remove(tmp.name)

    size_kb = size_bytes / 1024
    size_mb = size_bytes / (1024 * 1024)

    return size_bytes, size_kb, size_mb