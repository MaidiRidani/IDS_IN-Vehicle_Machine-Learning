# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================
import time
import gc                                   # untuk membersihkan RAM
import pandas as pd  
import numpy as np                       # untuk simpan hasil ke CSV
import matplotlib.pyplot as plt
import tensorflow as tf
from common import (
    calculate_metrics,
    init_experiment_note,
    save_test_results_to_csv,
    save_final_model,
    save_best_model,
    init_training_history_file,
    append_training_history,
    write_experiment_config,
    write_final_results,
    write_model_info,
    write_training_time
)
from dataset import CLIENT_DATA
from common import write_client_partition
from config import NUM_CLIENTS, MODE
from dataset import initialize_partitions
import os
import matplotlib.pyplot as plt
from config import MODE
np.random.seed(42)
tf.random.set_seed(42)

from server import (
    run_one_round,                          # menjalankan 1 round FL
    global_model,                           # model global (akan terus update)
    clear_validation_data                    # fungsi untuk membersihkan data validation dari RAM
)

from client import client_update_fn         # fungsi training client
from dataset import load_test_data          # load dataset test
from config import NUM_ROUNDS
import numpy as np
from dataset import BASE_PATH, load_validation_data, load_test_data
# ==============================
# KONFIGURASI
# ==============================


# ==============================
# STORAGE UNTUK LOGGING
# ==============================

initialize_partitions(
    num_clients=NUM_CLIENTS,
    mode=MODE
)
# Menyimpan model terbaik (berdasarkan accuracy validation)
best_weights = None
best_accuracy = 0.0
best_round = -1
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
write_experiment_config(note_path)
write_model_info(note_path, global_model)
write_client_partition(
    note_path,
    CLIENT_DATA
)

# ==============================
# DEBUG DISTRIBUSI DATASET
# ==============================

train_data = np.load(
    os.path.join(BASE_PATH, "tow_ids_train_dwt.npz")
)

y_train = train_data["y"]

_, y_val = load_validation_data()
_, y_test = load_test_data()

for name, labels in [
    ("Train", y_train),
    ("Validation", y_val),
    ("Test", y_test),
]:
    print(f"\n===== {name} =====")

    unique, counts = np.unique(labels, return_counts=True)

    for u, c in zip(unique, counts):
        print(f"Class {u}: {c}")
start_time = time.time()
print("===== START FEDERATED LEARNING =====")

for rnd in range(NUM_ROUNDS):

    print(f"\n========== ROUND {rnd+1} ==========")

    # ==============================
    # JALANKAN 1 ROUND FL
    # ==============================

    loss, acc = run_one_round(client_update_fn)

    append_training_history(
        history_file,
        rnd + 1,
        loss,
        acc
    )

    # ==============================
    # SIMPAN MODEL TERBAIK
    # ==============================

    if acc > best_accuracy:
        best_accuracy = acc
        best_round = rnd + 1
        best_weights = [
            w.copy()
            for w in global_model.get_weights()
        ]

        print(
            f"[INFO] Best model updated "
            f"(Round {best_round}, Acc={best_accuracy:.4f})"
        )


# ==============================
# SETELAH SEMUA ROUND SELESAI
# ==============================
print("\n===== TRAINING SELESAI =====")
print("===== BEST VALIDATION MODEL =====")
print(f"Best Round              : {best_round}")
print(f"Validation Accuracy     : {best_accuracy:.4f}")
print("=================================")
print("\n===== TRAINING SELESAI =====")
end_time = time.time()
training_seconds = end_time - start_time
write_training_time(
    note_path,
    training_seconds
)

# ==============================
# BERSIHKAN DATA VALIDATION (RAM)
# ==============================

# (data validation ada di server, tapi kita bantu GC)
gc.collect()
clear_validation_data()


# ==============================
# LOAD DATA TEST
# ==============================

print("\n[TEST] Memuat data test...")

x_test, y_test = load_test_data()

print(f"[TEST] Jumlah data test: {len(x_test)}")


# ==============================
# TEST DENGAN MODEL TERAKHIR
# ==============================

print("\n[TEST] Evaluasi dengan GLOBAL MODEL TERAKHIR")

final_loss, final_acc = global_model.evaluate(
    x_test,
    y_test,
    verbose=1
)

# 2. Prediksi probabilitas
y_pred_prob = global_model.predict(x_test)
y_pred = np.argmax(y_pred_prob, axis=1)

# 4. Hitung FPR & FNR
final_metrics = calculate_metrics(
    y_test,
    y_pred
)

final_metrics["loss"] = final_loss

print(
    f"[FINAL MODEL]\n"
    f"Loss                : {final_loss:.4f}\n"
    f"Accuracy            : {final_metrics['accuracy']:.4f}\n"
    f"Precision Macro     : {final_metrics['precision_macro']:.4f}\n"
    f"Recall Macro        : {final_metrics['recall_macro']:.4f}\n"
    f"F1 Macro            : {final_metrics['f1_macro']:.4f}\n"
    f"Precision Weighted  : {final_metrics['precision_weighted']:.4f}\n"
    f"Recall Weighted     : {final_metrics['recall_weighted']:.4f}\n"
    f"F1 Weighted         : {final_metrics['f1_weighted']:.4f}"
)
print("\n===== FINAL CONFUSION MATRIX =====")
print(final_metrics["confusion_matrix"])

# ==============================
# SIMPAN MODEL TERAKHIR
# ==============================

print("\n[INFO] Menyimpan GLOBAL MODEL TERAKHIR...")
save_final_model(global_model)


# ==============================
# TEST DENGAN MODEL TERBAIK
# ==============================

print("\n[TEST] Evaluasi dengan GLOBAL MODEL TERBAIK")
if best_weights is None:
    raise RuntimeError("Best weights belum pernah diperbarui.")
# Set bobot terbaik ke model global sementara
print(
    "\nWeight difference:",
    np.sum(
        np.abs(
            global_model.get_weights()[0] -
            best_weights[0]
        )
    )
)
global_model.set_weights(best_weights)

best_loss, best_acc= global_model.evaluate(x_test, y_test, verbose=1)

# 2. Prediksi probabilitas
y_pred_prob = global_model.predict(x_test)
y_pred = np.argmax(y_pred_prob, axis=1)

# ==============================
# ROC + PR + DISTRIBUTION ANALYSIS
# AUTO DETECT IID / NON-IID
# ==============================


# ==============================
# AUTO DETECT MODE DARI client.py
# ==============================

if MODE == 1:
    FL_MODE = "iid"

elif MODE == 2:
    FL_MODE = "non_iid"

else:
    FL_MODE = "unknown"

print(f"\n[INFO] FL Mode Detected: {FL_MODE}")


# 3. Konversi ke label
best_metrics = calculate_metrics(
    y_test,
    y_pred
)
print("\n===== BEST CONFUSION MATRIX =====")
print(best_metrics["confusion_matrix"])

print(
    f"[BEST MODEL]\n"
    f"Loss                : {best_loss:.4f}\n"
    f"Accuracy            : {best_metrics['accuracy']:.4f}\n"
    f"Precision Macro     : {best_metrics['precision_macro']:.4f}\n"
    f"Recall Macro        : {best_metrics['recall_macro']:.4f}\n"
    f"F1 Macro            : {best_metrics['f1_macro']:.4f}\n"
    f"Precision Weighted  : {best_metrics['precision_weighted']:.4f}\n"
    f"Recall Weighted     : {best_metrics['recall_weighted']:.4f}\n"
    f"F1 Weighted         : {best_metrics['f1_weighted']:.4f}"
)
# ==============================
# SIMPAN MODEL TERBAIK
# ==============================

print("\n[INFO] Menyimpan GLOBAL MODEL TERBAIK...")
save_best_model(global_model, best_weights)

del x_test, y_test
gc.collect()


# ==============================
# SIMPAN HASIL KE CSV
# ==============================

print("\n[INFO] Menyimpan hasil ke CSV...")


# Simpan hasil test
final_metrics["loss"] = final_loss


best_metrics["loss"] = best_loss


write_final_results(note_path, final_metrics, best_metrics)
# ==============================
# OUTPUT AKHIR
# ==============================
df_result = save_test_results_to_csv(
    final_metrics,
    best_metrics
)
print("\n===== HASIL AKHIR =====")
print(df_result)

print("\n===== SELESAI =====")