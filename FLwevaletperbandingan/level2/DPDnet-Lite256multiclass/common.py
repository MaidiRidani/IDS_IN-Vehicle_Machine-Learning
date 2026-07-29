# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================
import tempfile
from config import (
    DIRICHLET_ALPHA,
    MODE,
    NUM_CLIENTS,
    NUM_ROUNDS,
    LOCAL_EPOCHS,
    BATCH_SIZE,
    RANDOM_SEED
)
import tensorflow as tf
import numpy as np                                  # operasi numerik
import pandas as pd                                 # simpan ke CSV
import os
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
) 
from dataset import NUM_CLASSES

def calculate_metrics(y_true, y_pred):
    """
    Menghitung metrik evaluasi multiclass.
    """

    y_true = np.asarray(y_true).flatten()
    y_pred = np.asarray(y_pred).flatten()

    metrics = {

        "accuracy": accuracy_score(
            y_true,
            y_pred
        ),

        "precision_macro": precision_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        ),

        "recall_macro": recall_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        ),

        "f1_macro": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        ),

        "precision_weighted": precision_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ),

        "recall_weighted": recall_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ),

        "f1_weighted": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ),

        "confusion_matrix": confusion_matrix(
            y_true,
            y_pred
        )

    }

    return metrics

# fungsi helper untuk mengambil mode eksperimen dari config.py
def get_mode():
    """
    Mengambil mode eksperimen dari config.py.
    """

    return MODE

# ==============================
# FUNGSI: SIMPAN HASIL TEST KE CSV
# ==============================
def get_mode_name():

    mode = get_mode()

    if mode == 1:
        return "iid"

    elif mode == 2:
        return "noniid"

    return f"mode{mode}"
def save_test_results_to_csv(
    final_metrics: dict,
    best_metrics: dict,
    filename: str = None
):
    """
    Menyimpan hasil test ke folder 'trainingsave' dengan nama file otomatis berdasarkan MODE
    """

    # ==============================
    # AMBIL MODE DARI CLIENT
    # ==============================
    mode_name = get_mode_name()
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
    required_keys = [

    "loss",
    "accuracy",

    "precision_macro",
    "recall_macro",
    "f1_macro",

    "precision_weighted",
    "recall_weighted",
    "f1_weighted"

    ]

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
        {"type": "best_model", **best_metrics}
    ]

    df = pd.DataFrame(data)

    df = df[
    [
    "type",

    "loss",
    "accuracy",

    "precision_macro",
    "recall_macro",
    "f1_macro",

    "precision_weighted",
    "recall_weighted",
    "f1_weighted"

    ]
    ]

    # ==============================
    # SIMPAN
    # ==============================
    df.to_csv(full_path, index=False)

    print(f"[INFO] Hasil test disimpan ke {full_path}")

    return df

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

    mode_name = get_mode_name()

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
    mode_name = get_mode_name()

    # Set weight terbaik ke model (sesuai keinginan kamu)
    model.set_weights(best_weights)

    # Simpan model (overwrite, tapi beda nama per mode)
    save_model(model, f"saved_models/model_best_{mode_name}.h5")




def init_training_history_file(filename: str = None):
    """
    Membuat file CSV kosong dengan header (sekali di awal training)
    """
    mode_name = get_mode_name()

    folder = "trainingsave"
    os.makedirs(folder, exist_ok=True)

    if filename is None:
        filename = f"training_history_{mode_name}.csv"

    full_path = os.path.join(folder, filename)

    # ==============================
    # BUAT FILE + HEADER
    # ==============================
    with open(full_path, "w") as f:
        f.write("round,loss,accuracy\n")

    print(f"[INFO] File history dibuat: {full_path}")

    return full_path

def append_training_history(
    file_path,
    round_num,
    loss,
    acc
):

    with open(file_path, "a") as f:
        f.write(
            f"{round_num},{loss},{acc}\n"
        )







def init_experiment_note():
    """
    Membuat file note.txt berdasarkan mode
    """
    mode_name = get_mode_name()

    folder = "trainingsave"
    os.makedirs(folder, exist_ok=True)

    filename = f"note_{mode_name}.txt"
    full_path = os.path.join(folder, filename)

    with open(full_path, "w") as f:
        f.write("===== EXPERIMENT NOTE =====\n")

    print(f"[INFO] Note file dibuat: {full_path}")

    return full_path

def write_experiment_config(note_path):

    mode_name = get_mode_name()

    with open(note_path, "a") as f:

        f.write("\n--- CONFIG ---\n")
        f.write(f"Mode             : {mode_name.upper()}\n")
        f.write(f"Clients          : {NUM_CLIENTS}\n")
        f.write(f"Rounds           : {NUM_ROUNDS}\n")
        f.write(f"Local Epochs     : {LOCAL_EPOCHS}\n")
        f.write(f"Batch Size       : {BATCH_SIZE}\n")
        f.write(f"Random Seed      : {RANDOM_SEED}\n")
        f.write(f"Classes          : {NUM_CLASSES}\n")

        if MODE == 2:
            f.write(f"Dirichlet Alpha  : {DIRICHLET_ALPHA}\n")

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

def write_final_results(note_path, final_metrics, best_metrics):
    with open(note_path, "a") as f:

        f.write("\n--- FINAL RESULTS ---\n")

        # ==============================
        # FINAL MODEL
        # ==============================
        f.write("\n[FINAL MODEL]\n")

        for key, value in final_metrics.items():

            if key == "confusion_matrix":
                continue

            f.write(f"{key:22}: {value}\n")

        f.write("\nConfusion Matrix\n")
        f.write(str(final_metrics["confusion_matrix"]))
        f.write("\n")

        # ==============================
        # BEST MODEL
        # ==============================
        f.write("\n[BEST MODEL]\n")

        for key, value in best_metrics.items():

            if key == "confusion_matrix":
                continue

            f.write(f"{key:22}: {value}\n")

        f.write("\nConfusion Matrix\n")
        f.write(str(best_metrics["confusion_matrix"]))
        f.write("\n")





def get_model_size(model):
    with tempfile.NamedTemporaryFile(
        suffix=".h5",
        delete=False
    ) as tmp:

        temp_path = tmp.name

    model.save(temp_path)

    size_bytes = os.path.getsize(temp_path)

    os.remove(temp_path)

    size_kb = size_bytes / 1024
    size_mb = size_bytes / (1024 * 1024)

    return size_bytes, size_kb, size_mb

def write_training_time(note_path, seconds):

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = seconds % 60

    with open(note_path, "a") as f:

        f.write("\n--- TRAINING TIME ---\n")
        f.write(f"Total Seconds : {seconds:.2f}\n")
        f.write(f"Duration      : {hours}h {minutes}m {sec:.2f}s\n")

import numpy as np

def write_client_partition(note_path, client_data):
    """
    Menulis informasi partition setiap client ke note.
    """

    with open(note_path, "a") as f:

        f.write("\n--- CLIENT PARTITION ---\n\n")

        total_samples = 0
        sample_counts = []

        for client_id in sorted(client_data.keys()):

            x, y = client_data[client_id]

            total = len(y)

            sample_counts.append(total)
            total_samples += total

            f.write(f"Client {client_id}\n")
            f.write(f"Samples : {total}\n")

            classes, counts = np.unique(
                y,
                return_counts=True
            )

            for c in range(NUM_CLASSES):

                if c in classes:
                    idx = np.where(classes == c)[0][0]
                    jumlah = counts[idx]
                else:
                    jumlah = 0

                persen = jumlah / total * 100

                f.write(
                    f"  Class {c} : {jumlah} ({persen:.2f}%)\n"
                )

        f.write("--- PARTITION SUMMARY ---\n")
        f.write(f"Total Samples : {total_samples}\n")
        f.write(f"Clients       : {len(client_data)}\n")
        f.write(f"Min Samples   : {np.min(sample_counts)}\n")
        f.write(f"Max Samples   : {np.max(sample_counts)}\n")
        f.write(f"Mean Samples  : {np.mean(sample_counts):.2f}\n")
        f.write(f"Std Samples   : {np.std(sample_counts):.2f}\n")