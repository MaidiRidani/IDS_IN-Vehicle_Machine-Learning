# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

from sklearn.metrics import confusion_matrix
import gc
import pandas as pd

import torch
import numpy as np

from common import (
    calculate_final_metrics,
    calculate_best_metrics,
    get_model_size,
    init_experiment_note,
    save_test_results_to_csv,
    calculate_f1,
    save_final_model,
    save_best_model,
    init_training_history_file,
    append_training_history,
    write_experiment_config,
    write_final_results,
    write_model_info,
)

np.random.seed(42)
torch.manual_seed(42)

from server import (
    run_one_round,
    global_model,
    clear_validation_data
)

from client import client_update_fn
from dataset import VAL_PATH, load_test_data


# ==============================
# KONFIGURASI
# ==============================

NUM_ROUNDS = 25


# ==============================
# STORAGE
# ==============================
best_weights = None
best_accuracy = 0.0


# ==============================
# PRINT MODEL INFO (PYTORCH)
# ==============================
print(global_model)

total_params = sum(p.numel() for p in global_model.parameters())
trainable_params = sum(p.numel() for p in global_model.parameters() if p.requires_grad)
non_trainable_params = total_params - trainable_params

print("\n===== MODEL INFO =====")
print(f"Total Parameters     : {total_params:,}")
print(f"Trainable Parameters : {trainable_params:,}")
print(f"Non-trainable Params : {non_trainable_params:,}")
print("======================\n")


# ==============================
# INIT LOG
# ==============================
history_file = init_training_history_file()
note_path = init_experiment_note()

write_experiment_config(note_path, NUM_ROUNDS)
write_model_info(note_path, global_model)

print("===== START FEDERATED LEARNING =====")


# ==============================
# TRAINING LOOP
# ==============================
for rnd in range(NUM_ROUNDS):

    print(f"\n========== ROUND {rnd+1} ==========")

    loss, acc, prec, rec = run_one_round(client_update_fn)
    f1 = calculate_f1(prec, rec)

    append_training_history(
        history_file,
        rnd + 1,
        loss,
        acc,
        prec,
        rec,
        f1
    )

    # ==============================
    # SAVE BEST MODEL
    # ==============================
    if acc > best_accuracy:
        best_accuracy = acc

        # 🔁 ganti get_weights()
        best_weights = [
            v.detach().cpu().numpy()
            for v in global_model.state_dict().values()
        ]

        print(f"[INFO] Model terbaik diperbarui (Accuracy: {acc:.4f})")


# ==============================
# SELESAI TRAINING
# ==============================
print("\n===== TRAINING SELESAI =====")

gc.collect()
clear_validation_data()


# ==============================
# SAVE MODEL
# ==============================
print("\n[INFO] Menyimpan GLOBAL MODEL TERAKHIR...")
save_final_model(global_model)

print("\n[INFO] Menyimpan GLOBAL MODEL TERBAIK...")
save_best_model(global_model, best_weights)

print("\n===== TRAINING DONE (NO TEST) =====")