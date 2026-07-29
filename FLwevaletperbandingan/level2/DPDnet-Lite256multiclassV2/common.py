# ==========================================================
# COMMON UTILITIES
# PART 1
#
# - Import
# - Mode Helper
# - Evaluation Metrics
# - Model Saving
# ==========================================================

import os
import shutil
import tempfile

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from config import (
    MODE,
    NUM_CLIENTS,
    NUM_ROUNDS,
    LOCAL_EPOCHS,
    BATCH_SIZE,
    RANDOM_SEED,
    DIRICHLET_ALPHA,
    INITIAL_GLOBAL_MODEL_PATH,
)

from dataset import NUM_CLASSES


# ==========================================================
# MODE HELPER
# ==========================================================

def get_mode_name() -> str:
    """
    Mengubah MODE menjadi nama eksperimen.
    """

    if MODE == 1:
        return "iid"

    if MODE == 2:
        return "noniid"

    return f"mode{MODE}"


# ==========================================================
# CALCULATE METRICS
# ==========================================================

def calculate_metrics(
    y_true,
    y_pred,
):
    """
    Menghitung metrik evaluasi multiclass.
    """

    y_true = np.asarray(y_true).flatten()
    y_pred = np.asarray(y_pred).flatten()

    return {

        "accuracy": accuracy_score(
            y_true,
            y_pred
        ),

        "precision_macro": precision_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),

        "recall_macro": recall_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),

        "f1_macro": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),

        "precision_weighted": precision_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0,
        ),

        "recall_weighted": recall_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0,
        ),

        "f1_weighted": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0,
        ),

        "confusion_matrix": confusion_matrix(
            y_true,
            y_pred,
            labels=np.arange(NUM_CLASSES),
        ),

    }


# ==========================================================
# SAVE MODEL
# ==========================================================

def save_model(
    model,
    path: str,
):
    """
    Menyimpan model ke lokasi tertentu.
    """

    folder = os.path.dirname(path)

    if folder != "":
        os.makedirs(
            folder,
            exist_ok=True
        )

    model.save(path)

    print(
        f"[INFO] Model saved -> {path}"
    )


# ==========================================================
# COPY INITIAL GLOBAL MODEL
# ==========================================================

def save_initial_global_model():

    """
    Menyalin Initial Global Model
    ke folder eksperimen.
    """

    folder = "saved_models"

    os.makedirs(
        folder,
        exist_ok=True
    )

    dst = os.path.join(
        folder,
        "initial_global_model.keras"
    )

    shutil.copy2(
        INITIAL_GLOBAL_MODEL_PATH,
        dst
    )

    print(
        "[INFO] Initial Global Model copied."
    )


# ==========================================================
# SAVE FINAL MODEL
# ==========================================================

def save_final_model(
    model,
):
    """
    Menyimpan model global terakhir.
    """

    mode = get_mode_name()

    path = os.path.join(

        "saved_models",

        f"global_model_final_{mode}.keras"

    )

    save_model(
        model,
        path
    )


# ==========================================================
# SAVE BEST MODEL
# ==========================================================

def save_best_model(
    model,
    best_weights,
):
    """
    Menyimpan Best Global Model.
    """

    if best_weights is None:

        print(
            "[WARNING] Best weights tidak tersedia."
        )

        return

    model.set_weights(
        best_weights
    )

    mode = get_mode_name()

    path = os.path.join(

        "saved_models",

        f"global_model_best_{mode}.keras"

    )

    save_model(
        model,
        path
    )

# ==========================================================
# TRAINING HISTORY
# ==========================================================

def init_training_history_file(
    filename: str = None,
):
    """
    Membuat file CSV untuk menyimpan history validation.
    """

    folder = "trainingsave"

    os.makedirs(
        folder,
        exist_ok=True
    )

    mode = get_mode_name()

    if filename is None:

        filename = (
            f"training_history_{mode}.csv"
        )

    path = os.path.join(
        folder,
        filename
    )

    with open(path, "w") as f:

        f.write(
            "round,loss,accuracy\n"
        )

    print(
        f"[INFO] History file : {path}"
    )

    return path


# ==========================================================
# APPEND TRAINING HISTORY
# ==========================================================

def append_training_history(
    file_path,
    round_num,
    loss,
    accuracy,
):
    """
    Menambahkan satu baris history training.
    """

    with open(file_path, "a") as f:

        f.write(
            f"{round_num},"
            f"{loss:.6f},"
            f"{accuracy:.6f}\n"
        )


# ==========================================================
# EXPERIMENT NOTE
# ==========================================================

def init_experiment_note():
    """
    Membuat note eksperimen.
    """

    folder = "trainingsave"

    os.makedirs(
        folder,
        exist_ok=True
    )

    filename = (
        f"note_{get_mode_name()}.txt"
    )

    path = os.path.join(
        folder,
        filename
    )

    with open(path, "w") as f:

        f.write(
            "========== FEDERATED CONTINUAL LEARNING ==========\n"
        )

    print(
        f"[INFO] Experiment note : {path}"
    )

    return path


# ==========================================================
# WRITE CONFIG
# ==========================================================

def write_experiment_config(
    note_path,
):
    """
    Menulis konfigurasi eksperimen.
    """

    with open(note_path, "a") as f:

        f.write("\n")

        f.write("=" * 60 + "\n")
        f.write("CONFIGURATION\n")
        f.write("=" * 60 + "\n")

        f.write(
            f"Mode              : "
            f"{get_mode_name().upper()}\n"
        )

        f.write(
            f"Clients           : "
            f"{NUM_CLIENTS}\n"
        )

        f.write(
            f"Communication     : "
            f"{NUM_ROUNDS}\n"
        )

        f.write(
            f"Local Epochs      : "
            f"{LOCAL_EPOCHS}\n"
        )

        f.write(
            f"Batch Size        : "
            f"{BATCH_SIZE}\n"
        )

        f.write(
            f"Random Seed       : "
            f"{RANDOM_SEED}\n"
        )

        f.write(
            f"Classes           : "
            f"{NUM_CLASSES}\n"
        )

        if MODE == 2:

            f.write(
                f"Dirichlet Alpha   : "
                f"{DIRICHLET_ALPHA}\n"
            )

        f.write(
            f"Initial Model     : "
            f"{INITIAL_GLOBAL_MODEL_PATH}\n"
        )

        f.write("\n")


# ==========================================================
# MODEL INFORMATION
# ==========================================================

def write_model_info(
    note_path,
    model,
):
    """
    Menulis informasi model.
    """

    total_params = model.count_params()

    trainable_params = sum(

        tf.keras.backend.count_params(w)

        for w in model.trainable_weights

    )

    non_trainable_params = sum(

        tf.keras.backend.count_params(w)

        for w in model.non_trainable_weights

    )

    size_bytes, size_kb, size_mb = get_model_size(
        model
    )

    with open(note_path, "a") as f:

        f.write("=" * 60 + "\n")
        f.write("MODEL INFORMATION\n")
        f.write("=" * 60 + "\n")

        f.write(
            f"Total Parameters      : "
            f"{total_params:,}\n"
        )

        f.write(
            f"Trainable Parameters  : "
            f"{trainable_params:,}\n"
        )

        f.write(
            f"Non-trainable Params  : "
            f"{non_trainable_params:,}\n"
        )

        f.write(
            f"Model Size (Bytes)    : "
            f"{size_bytes:,}\n"
        )

        f.write(
            f"Model Size (KB)       : "
            f"{size_kb:.2f}\n"
        )

        f.write(
            f"Model Size (MB)       : "
            f"{size_mb:.2f}\n"
        )

        f.write("\n")


# ==========================================================
# CLIENT PARTITION
# ==========================================================

def write_client_partition(
    note_path,
    client_data,
):
    """
    Menulis distribusi data seluruh client.
    """

    with open(note_path, "a") as f:

        f.write("=" * 60 + "\n")
        f.write("CLIENT PARTITION\n")
        f.write("=" * 60 + "\n\n")

        sample_counts = []

        total_samples = 0

        for client_id in sorted(client_data.keys()):

            client = client_data[client_id]

            y = client["y"]

            manifest = client["manifest"]

            total = len(y)

            sample_counts.append(total)

            total_samples += total

            f.write(
                f"Client {client_id}\n"
            )

            f.write(
                f"Samples  : {total}\n"
            )

            f.write(
                f"Manifest : {manifest.tolist()}\n"
            )

            classes, counts = np.unique(

                y,

                return_counts=True

            )

            for cls in range(NUM_CLASSES):

                if cls in classes:

                    idx = np.where(
                        classes == cls
                    )[0][0]

                    count = counts[idx]

                else:

                    count = 0

                percent = (
                    count / total * 100
                )

                f.write(

                    f"  Class {cls:<2} : "

                    f"{count:<6}"

                    f"({percent:6.2f}%)\n"

                )

            f.write("\n")

        f.write("=" * 60 + "\n")
        f.write("PARTITION SUMMARY\n")
        f.write("=" * 60 + "\n")

        f.write(
            f"Total Samples : "
            f"{total_samples}\n"
        )

        f.write(
            f"Clients       : "
            f"{len(client_data)}\n"
        )

        f.write(
            f"Min Samples   : "
            f"{np.min(sample_counts)}\n"
        )

        f.write(
            f"Max Samples   : "
            f"{np.max(sample_counts)}\n"
        )

        f.write(
            f"Mean Samples  : "
            f"{np.mean(sample_counts):.2f}\n"
        )

        f.write(
            f"Std Samples   : "
            f"{np.std(sample_counts):.2f}\n"
        )

        f.write("\n")


# ==========================================================
# TRAINING TIME
# ==========================================================

def write_training_time(
    note_path,
    seconds,
):
    """
    Menulis durasi training.
    """

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    sec = seconds % 60

    with open(note_path, "a") as f:

        f.write("=" * 60 + "\n")
        f.write("TRAINING TIME\n")
        f.write("=" * 60 + "\n")

        f.write(
            f"Total Seconds : "
            f"{seconds:.2f}\n"
        )

        f.write(

            f"Duration      : "

            f"{hours}h "

            f"{minutes}m "

            f"{sec:.2f}s\n\n"

        )


# ==========================================================
# MODEL SIZE
# ==========================================================

def get_model_size(
    model,
):
    """
    Menghitung ukuran model.
    """

    with tempfile.NamedTemporaryFile(

        suffix=".keras",

        delete=False

    ) as tmp:

        temp_path = tmp.name

    model.save(
        temp_path
    )

    size_bytes = os.path.getsize(
        temp_path
    )

    os.remove(
        temp_path
    )

    size_kb = size_bytes / 1024

    size_mb = size_kb / 1024

    return (

        size_bytes,

        size_kb,

        size_mb,

    )



# ==========================================================
# SAVE TEST RESULTS
# ==========================================================

def save_test_results_to_csv(
    final_metrics23,
    final_metrics21,
    best_metrics23,
    best_metrics21,
    filename=None,
):
    """
    Menyimpan hasil evaluasi test ke CSV.

    Model:
        - Final Global Model
        - Best Global Model

    Dataset:
        - Dataset23 Test
        - Dataset21 Test
    """

    folder = "trainingsave"

    os.makedirs(
        folder,
        exist_ok=True
    )

    if filename is None:

        filename = (
            f"test_results_"
            f"{get_mode_name()}.csv"
        )

    path = os.path.join(
        folder,
        filename
    )

    rows = [

        {
            "model": "Final Global Model",
            "dataset": "Dataset23",
            **final_metrics23,
        },

        {
            "model": "Final Global Model",
            "dataset": "Dataset21",
            **final_metrics21,
        },

        {
            "model": "Best Global Model",
            "dataset": "Dataset23",
            **best_metrics23,
        },

        {
            "model": "Best Global Model",
            "dataset": "Dataset21",
            **best_metrics21,
        },

    ]

    df = pd.DataFrame(rows)

    df = df[

        [

            "model",
            "dataset",

            "loss",
            "accuracy",

            "precision_macro",
            "recall_macro",
            "f1_macro",

            "precision_weighted",
            "recall_weighted",
            "f1_weighted",

        ]

    ]

    df.to_csv(

        path,

        index=False,

    )

    print(
        f"[INFO] Test results saved -> {path}"
    )

    return df


# ==========================================================
# WRITE FINAL RESULTS
# ==========================================================

def write_final_results(

    note_path,

    final_metrics23,
    final_metrics21,

    best_metrics23,
    best_metrics21,

    best_round,

):
    """
    Menulis seluruh hasil evaluasi akhir.
    """

    def write_block(
        file,
        title,
        metrics,
    ):

        file.write("\n")
        file.write(title)
        file.write("\n")

        for key, value in metrics.items():

            if key == "confusion_matrix":
                continue

            file.write(

                f"{key:<22}: "

                f"{value}\n"

            )

        file.write("\nConfusion Matrix\n")

        file.write(
            str(metrics["confusion_matrix"])
        )

        file.write("\n")

    with open(note_path, "a") as f:

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write("FINAL RESULTS\n")
        f.write("=" * 60 + "\n")

        # ==================================================
        # FINAL MODEL
        # ==================================================

        f.write("\nFINAL GLOBAL MODEL\n")

        write_block(

            f,

            "Dataset23 Test",

            final_metrics23,

        )

        write_block(

            f,

            "Dataset21 Test",

            final_metrics21,

        )

        # ==================================================
        # BEST MODEL
        # ==================================================

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write("BEST GLOBAL MODEL\n")
        f.write("=" * 60 + "\n")

        f.write(
            f"Best Round : {best_round}\n"
        )

        write_block(

            f,

            "Dataset23 Test",

            best_metrics23,

        )

        write_block(

            f,

            "Dataset21 Test",

            best_metrics21,

        )

    print(
        "[INFO] Final results written."
    )