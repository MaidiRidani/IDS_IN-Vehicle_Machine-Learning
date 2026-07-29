# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

from sklearn.metrics import confusion_matrix
import gc                                   # untuk membersihkan RAM
import pandas as pd                         # untuk simpan hasil ke CSV

import tensorflow as tf
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
tf.random.set_seed(42)

from server import (
    run_one_round,                          # menjalankan 1 round FL
    global_model,                           # model global (akan terus update)
    clear_validation_data                    # fungsi untuk membersihkan data validation dari RAM
)

from client import client_update_fn         # fungsi training client
from dataset import VAL_PATH, load_test_data          # load dataset test


# ==============================
# KONFIGURASI
# ==============================

NUM_ROUNDS = 25   # jumlah round FL (bisa kamu ubah)

# ==============================
# STORAGE UNTUK LOGGING
# ==============================


# Menyimpan model terbaik (berdasarkan accuracy validation)
best_weights = None
best_accuracy = 0.0

# ==============================
# PRINT MODEL INFO
# ==============================
global_model.summary()

total_params = global_model.count_params()
trainable_params = sum([tf.keras.backend.count_params(w) for w in global_model.trainable_weights])
non_trainable_params = sum([tf.keras.backend.count_params(w) for w in global_model.non_trainable_weights])

print("\n===== MODEL INFO =====")
print(f"Total Parameters     : {total_params:,}")
print(f"Trainable Parameters : {trainable_params:,}")
print(f"Non-trainable Params : {non_trainable_params:,}")
print("======================\n")
# ==============================
# START FEDERATED LEARNING
# ==============================
# ==============================
# INIT LOG FILE
# ==============================
history_file = init_training_history_file()

note_path = init_experiment_note()

# ==============================
# WRITE META INFO (SEKALI SAJA)
# ==============================
write_experiment_config(note_path, NUM_ROUNDS)
write_model_info(note_path, global_model)

print("===== START FEDERATED LEARNING =====")

for rnd in range(NUM_ROUNDS):

    print(f"\n========== ROUND {rnd+1} ==========")

    # ==============================
    # JALANKAN 1 ROUND FL
    # ==============================

    loss, acc, prec, rec = run_one_round(client_update_fn)
    f1 = calculate_f1(prec, rec)

    # ==============================
    # SIMPAN HASIL ROUND
    # ==============================

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
    # SIMPAN MODEL TERBAIK
    # ==============================

    if acc > best_accuracy:
        best_accuracy = acc
        best_weights = global_model.get_weights()

        print(f"[INFO] Model terbaik diperbarui (Accuracy: {acc:.4f})")


# ==============================
# SETELAH SEMUA ROUND SELESAI
# ==============================

print("\n===== TRAINING SELESAI =====")

print("\n===== TRAINING SELESAI =====")

gc.collect()
clear_validation_data()

print("\n[INFO] Menyimpan GLOBAL MODEL TERAKHIR...")
save_final_model(global_model)

print("\n[INFO] Menyimpan GLOBAL MODEL TERBAIK...")
save_best_model(global_model, best_weights)

print("\n===== TRAINING DONE (NO TEST) =====")