# ==============================
# IMPORT
# ==============================
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
import os
import torch
import tempfile


# ==============================
# FPR / FNR
# ==============================
def calculate_fpr_fnr(y_true, y_pred):

    y_true = y_true.flatten()
    y_pred = y_pred.flatten()

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    fpr = fp / (fp + tn) if (fp + tn) != 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) != 0 else 0.0

    return fpr, fnr


def calculate_final_metrics(y_true, y_pred):
    return calculate_fpr_fnr(y_true, y_pred)


def calculate_best_metrics(y_true, y_pred):
    return calculate_fpr_fnr(y_true, y_pred)


# ==============================
# MODE
# ==============================
def get_mode_from_client():
    from client import mode
    return mode


# ==============================
# SAVE CSV
# ==============================
def save_test_results_to_csv(final_metrics, best_metrics, filename=None):

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
        filename = f"test_results_{mode_name}.csv"

    full_path = os.path.join(folder, filename)

    required_keys = ["loss", "accuracy", "precision", "recall", "f1", "fpr", "fnr"]

    for key in required_keys:
        if key not in final_metrics:
            raise ValueError(f"final_metrics missing key: {key}")
        if key not in best_metrics:
            raise ValueError(f"best_metrics missing key: {key}")

    data = [
        {"type": "final_model", **final_metrics},
        {"type": "best_model", **best_metrics}
    ]

    df = pd.DataFrame(data)
    df = df[["type", "loss", "accuracy", "precision", "recall", "f1", "fpr", "fnr"]]

    df.to_csv(full_path, index=False)

    print(f"[INFO] Hasil test disimpan ke {full_path}")

    return df


# ==============================
# F1
# ==============================
def calculate_f1(precision, recall):

    if (precision + recall) == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)


# ==============================
# SAVE MODEL (PYTORCH)
# ==============================
def save_model(model, path: str):

    folder = os.path.dirname(path)
    if folder != "":
        os.makedirs(folder, exist_ok=True)

    # 🔁 ubah ke .pt
    path = path.replace(".h5", ".pt")

    torch.save(model.state_dict(), path)

    print(f"[INFO] Model disimpan di: {path}")


def save_final_model(model):

    mode = get_mode_from_client()
    mode_name = "iid" if mode == 1 else "noniid"

    save_model(model, f"saved_models/model_final_{mode_name}.pt")


def save_best_model(model, best_weights):

    if best_weights is None:
        print("[WARNING] Tidak ada best_weights")
        return

    mode = get_mode_from_client()
    mode_name = "iid" if mode == 1 else "noniid"

    # 🔁 set weights versi pytorch
    state_dict = model.state_dict()
    new_state_dict = {}

    for (k, _), w in zip(state_dict.items(), best_weights):
        new_state_dict[k] = torch.tensor(w)

    model.load_state_dict(new_state_dict)

    save_model(model, f"saved_models/model_best_{mode_name}.pt")


# ==============================
# HISTORY
# ==============================
def init_training_history_file(filename=None):

    mode = get_mode_from_client()
    mode_name = "iid" if mode == 1 else "noniid"

    folder = "trainingsave"
    os.makedirs(folder, exist_ok=True)

    if filename is None:
        filename = f"training_history_{mode_name}.csv"

    full_path = os.path.join(folder, filename)

    with open(full_path, "w") as f:
        f.write("round,loss,accuracy,precision,recall,f1\n")

    return full_path


def append_training_history(file_path, round_num, loss, acc, prec, rec, f1):

    with open(file_path, "a") as f:
        f.write(f"{round_num},{loss},{acc},{prec},{rec},{f1}\n")


# ==============================
# NOTE
# ==============================
def init_experiment_note():

    mode = get_mode_from_client()
    mode_name = "iid" if mode == 1 else "noniid"

    folder = "trainingsave"
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, f"note_{mode_name}.txt")

    with open(path, "w") as f:
        f.write("===== EXPERIMENT NOTE =====\n")

    return path


def write_experiment_config(note_path, num_rounds):

    mode = get_mode_from_client()
    mode_name = "IID" if mode == 1 else "NON-IID"

    with open(note_path, "a") as f:
        f.write(f"\nMode: {mode_name}\nRounds: {num_rounds}\n")


# ==============================
# MODEL INFO (PYTORCH)
# ==============================
def write_model_info(note_path, model):

    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    non_trainable_params = total_params - trainable_params

    size_bytes, size_kb, size_mb = get_model_size(model)

    with open(note_path, "a") as f:
        f.write("\n--- MODEL INFO ---\n")
        f.write(f"Total Params: {total_params}\n")
        f.write(f"Trainable: {trainable_params}\n")
        f.write(f"Non-trainable: {non_trainable_params}\n")
        f.write(f"Model Size (MB): {size_mb:.2f}\n")


def write_final_results(note_path, final_metrics, best_metrics):

    with open(note_path, "a") as f:
        f.write("\n--- FINAL RESULTS ---\n")

        f.write("\n[FINAL]\n")
        for k, v in final_metrics.items():
            f.write(f"{k}: {v}\n")

        f.write("\n[BEST]\n")
        for k, v in best_metrics.items():
            f.write(f"{k}: {v}\n")


# ==============================
# MODEL SIZE (PYTORCH)
# ==============================
def get_model_size(model):

    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as tmp:
        torch.save(model.state_dict(), tmp.name)
        size_bytes = os.path.getsize(tmp.name)

    os.remove(tmp.name)

    size_kb = size_bytes / 1024
    size_mb = size_bytes / (1024 * 1024)

    return size_bytes, size_kb, size_mb