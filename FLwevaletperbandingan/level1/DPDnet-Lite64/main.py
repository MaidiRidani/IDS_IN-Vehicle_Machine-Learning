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
    save_best_fnr_model,
    init_training_history_file,
    append_training_history,
    write_experiment_config,
    write_final_results,
    write_model_info,
)
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    roc_curve,
    auc,
    precision_recall_curve
)
from client import mode


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

NUM_ROUNDS = 20   # jumlah round FL (bisa kamu ubah)

# ==============================
# STORAGE UNTUK LOGGING
# ==============================


# ==============================
# BEST GENERAL MODEL (F1)
# ==============================
best_weights = None
best_f1_score = 0.0

# ==============================
# BEST SAFETY MODEL (LOWEST FNR)
# ==============================
best_weights_fnr = None
best_safety_score = 0.0


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
    safety_score = (
    0.8 * rec
    + 0.2 * prec
)

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
    # STRICT CONDITION
    # ==============================

    if (
        f1 > best_f1_score
        and prec > 0.8
        and acc > 0.8
    ):

        best_f1_score = f1
        best_weights = global_model.get_weights()

        print(
            f"[INFO] Best F1 Model Updated (STRICT) | "
            f"F1: {f1:.4f}"
        )

    # ==============================
    # RELAXED CONDITION
    # ==============================

    elif (
        f1 > best_f1_score
        and prec > 0.65
        and acc > 0.65
    ):

        best_f1_score = f1
        best_weights = global_model.get_weights()

        print(
            f"[INFO] Best F1 Model Updated (RELAXED) | "
            f"F1: {f1:.4f}"
        )

    # ==============================
    # BEST SAFETY MODEL
    # ==============================

    # STRICT CONDITION
    if (
        safety_score > best_safety_score
        and prec > 0.8
        and acc > 0.8
    ):

        best_safety_score = safety_score
        best_weights_fnr = global_model.get_weights()

        fnr = 1 - rec

        print(
            f"[INFO] Best Safety Model Updated (STRICT) | "
            f"Recall: {rec:.4f} | "
            f"Precision: {prec:.4f} | "
            f"Safety Score: {safety_score:.4f} | "
            f"FNR: {fnr:.4f}"
        )

    # RELAXED CONDITION
    elif (
        safety_score > best_safety_score
        and prec > 0.65
        and acc > 0.65
    ):

        best_safety_score = safety_score
        best_weights_fnr = global_model.get_weights()

        fnr = 1 - rec

        print(
            f"[INFO] Best Safety Model Updated (RELAXED) | "
            f"Recall: {rec:.4f} | "
            f"Precision: {prec:.4f} | "
            f"Safety Score: {safety_score:.4f} | "
            f"FNR: {fnr:.4f}"
        )
if best_weights is None:
    print("[WARNING] Tidak ada BEST F1 MODEL valid")
    best_weights = global_model.get_weights()

if best_weights_fnr is None:
    print("[WARNING] Tidak ada BEST FNR MODEL valid")
    best_weights_fnr = global_model.get_weights()

# ==============================
# SETELAH SEMUA ROUND SELESAI
# ==============================

print("\n===== TRAINING SELESAI =====")


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

final_loss, final_acc, final_prec, final_rec = global_model.evaluate(
    x_test,
    y_test,
    verbose=1
)

# Prediksi probabilitas
y_pred_prob = global_model.predict(x_test)

# Konversi ke label
y_pred = (y_pred_prob > 0.5).astype(int)

# Hitung FPR & FNR
final_fpr, final_fnr = calculate_final_metrics(
    y_test,
    y_pred
)

# Hitung F1
final_f1 = calculate_f1(
    final_prec,
    final_rec
)

print(
    f"[FINAL MODEL] "
    f"Loss: {final_loss:.4f} | "
    f"Accuracy: {final_acc:.4f} | "
    f"Precision: {final_prec:.4f} | "
    f"Recall: {final_rec:.4f} | "
    f"FPR: {final_fpr:.4f} | "
    f"FNR: {final_fnr:.4f} | "
    f"F1: {final_f1:.4f}"
)

# ==============================
# SIMPAN MODEL TERAKHIR
# ==============================

print("\n[INFO] Menyimpan GLOBAL MODEL TERAKHIR...")
save_final_model(global_model)

# ==============================
# TEST DENGAN BEST F1 MODEL
# ==============================

print("\n[TEST] Evaluasi dengan BEST F1 MODEL")

global_model.set_weights(best_weights)

best_loss, best_acc, best_prec, best_rec = global_model.evaluate(
    x_test,
    y_test,
    verbose=1
)

# Prediksi probabilitas
y_pred_prob = global_model.predict(x_test)

# Konversi ke label
y_pred = (y_pred_prob > 0.5).astype(int)

# Hitung FPR & FNR
best_fpr, best_fnr = calculate_best_metrics(
    y_test,
    y_pred
)

# Hitung F1
best_f1 = calculate_f1(
    best_prec,
    best_rec
)

print(
    f"[BEST F1 MODEL] "
    f"Loss: {best_loss:.4f} | "
    f"Accuracy: {best_acc:.4f} | "
    f"Precision: {best_prec:.4f} | "
    f"Recall: {best_rec:.4f} | "
    f"FPR: {best_fpr:.4f} | "
    f"FNR: {best_fnr:.4f} | "
    f"F1: {best_f1:.4f}"
)

# ==============================
# SIMPAN BEST F1 MODEL
# ==============================

print("\n[INFO] Menyimpan BEST F1 MODEL...")
save_best_model(global_model, best_weights)

# ==============================
# TEST DENGAN BEST FNR MODEL
# ==============================

print("\n[TEST] Evaluasi dengan BEST FNR MODEL")

global_model.set_weights(best_weights_fnr)

fnr_loss, fnr_acc, fnr_prec, fnr_rec = global_model.evaluate(
    x_test,
    y_test,
    verbose=1
)

# Prediksi probabilitas
y_pred_prob = global_model.predict(x_test)

# Konversi ke label
y_pred = (y_pred_prob > 0.5).astype(int)

# Hitung FPR & FNR
fnr_fpr, fnr_fnr = calculate_best_metrics(
    y_test,
    y_pred
)

# Hitung F1
fnr_f1 = calculate_f1(
    fnr_prec,
    fnr_rec
)

print(
    f"[BEST FNR MODEL] "
    f"Loss: {fnr_loss:.4f} | "
    f"Accuracy: {fnr_acc:.4f} | "
    f"Precision: {fnr_prec:.4f} | "
    f"Recall: {fnr_rec:.4f} | "
    f"FPR: {fnr_fpr:.4f} | "
    f"FNR: {fnr_fnr:.4f} | "
    f"F1: {fnr_f1:.4f}"
)

# ==============================
# SIMPAN BEST FNR MODEL
# ==============================

print("\n[INFO] Menyimpan BEST FNR MODEL...")
save_best_fnr_model(global_model, best_weights_fnr)

# ==============================
# ROC + PR + DISTRIBUTION ANALYSIS
# AUTO DETECT IID / NON-IID
# ==============================


# ==============================
# AUTO DETECT MODE DARI client.py
# ==============================

if mode == 1:
    FL_MODE = "iid"

elif mode == 2:
    FL_MODE = "non_iid"

else:
    FL_MODE = "unknown"

print(f"\n[INFO] FL Mode Detected: {FL_MODE}")

# ==============================
# RESULT DIRECTORY
# ==============================

RESULT_DIR = f"results/{FL_MODE}"

os.makedirs(
    RESULT_DIR,
    exist_ok=True
)

# ==============================
# FLATTEN PROBABILITY
# ==============================

y_pred_prob = y_pred_prob.ravel()

# ==============================
# SAVE ROC DATA
# ==============================

roc_df = pd.DataFrame({
    "y_true": y_test,
    "y_prob": y_pred_prob
})

roc_csv_path = f"{RESULT_DIR}/roc_data.csv"

roc_df.to_csv(
    roc_csv_path,
    index=False
)

print(f"[INFO] ROC data disimpan: {roc_csv_path}")

# ==============================
# ROC CURVE
# ==============================

fpr_curve, tpr_curve, thresholds = roc_curve(
    y_test,
    y_pred_prob
)

roc_auc = auc(
    fpr_curve,
    tpr_curve
)

print(f"[ROC] AUC Score: {roc_auc:.4f}")

plt.figure(figsize=(7,7))

plt.plot(
    fpr_curve,
    tpr_curve,
    label=f"AUC = {roc_auc:.4f}"
)

plt.plot(
    [0,1],
    [0,1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(f"ROC Curve - {FL_MODE.upper()} FL")

plt.legend()

plt.grid(True)

roc_image_path = f"{RESULT_DIR}/roc_curve_{FL_MODE}.png"

plt.savefig(
    roc_image_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"[INFO] ROC curve disimpan: {roc_image_path}")

plt.show()

# ==============================
# PRECISION-RECALL CURVE
# ==============================

precision_curve, recall_curve, _ = precision_recall_curve(
    y_test,
    y_pred_prob
)

plt.figure(figsize=(7,7))

plt.plot(
    recall_curve,
    precision_curve
)

plt.xlabel("Recall")
plt.ylabel("Precision")

plt.title(f"PR Curve - {FL_MODE.upper()} FL")

plt.grid(True)

pr_image_path = f"{RESULT_DIR}/pr_curve_{FL_MODE}.png"

plt.savefig(
    pr_image_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"[INFO] PR curve disimpan: {pr_image_path}")

plt.show()

# ==============================
# PROBABILITY DISTRIBUTION
# ==============================

plt.figure(figsize=(8,5))

sns.histplot(
    y_pred_prob[y_test == 0],
    bins=50,
    stat="density",
    alpha=0.5,
    label="Normal"
)

sns.histplot(
    y_pred_prob[y_test == 1],
    bins=50,
    stat="density",
    alpha=0.5,
    label="Attack"
)

plt.xlabel("Predicted Probability")
plt.ylabel("Density")

plt.title(f"Probability Distribution - {FL_MODE.upper()} FL")

plt.legend()

plt.grid(True)

dist_image_path = f"{RESULT_DIR}/prob_distribution_{FL_MODE}.png"

plt.savefig(
    dist_image_path,
    dpi=300,
    bbox_inches="tight"
)

print(f"[INFO] Distribution plot disimpan: {dist_image_path}")

plt.show()


del x_test, y_test
gc.collect()


# ==============================
# SIMPAN HASIL KE CSV
# ==============================

print("\n[INFO] Menyimpan hasil ke CSV...")


# Simpan hasil test
final_metrics = {
    "loss": final_loss,
    "accuracy": final_acc,
    "precision": final_prec,
    "recall": final_rec,
    "fpr": final_fpr,
    "fnr": final_fnr,
    "f1": final_f1
}

best_metrics = {
    "loss": best_loss,
    "accuracy": best_acc,
    "precision": best_prec,
    "recall": best_rec,
    "fpr": best_fpr,
    "fnr": best_fnr,
    "f1": best_f1
}
fnr_metrics = {
    "loss": fnr_loss,
    "accuracy": fnr_acc,
    "precision": fnr_prec,
    "recall": fnr_rec,
    "fpr": fnr_fpr,
    "fnr": fnr_fnr,
    "f1": fnr_f1
}

save_test_results_to_csv(
    final_metrics,
    best_metrics,
    fnr_metrics
)


write_final_results(
    note_path,
    final_metrics,
    best_metrics,
    fnr_metrics
)
# ==============================
# OUTPUT AKHIR
# ==============================
df_result = save_test_results_to_csv(
    final_metrics,
    best_metrics,
    fnr_metrics
)
print("\n===== HASIL AKHIR =====")
print(df_result)

print("\n===== SELESAI =====")