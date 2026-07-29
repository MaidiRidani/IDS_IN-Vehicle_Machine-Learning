# ==============================
# IMPORT
# ==============================

import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model

from config import (
    INITIAL_GLOBAL_MODEL_PATH,
    BATCH_SIZE,
    RANDOM_SEED
)

from dataset import (
    load_dataset21,
    load_validation_data21,
    remap_dataset21_labels
)


# ==============================
# RANDOM SEED
# ==============================

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)


# ==============================
# LOAD DATASET21 TRAIN
# ==============================

print("\n===== LOAD DATASET21 TRAIN =====")

x_train21, y_train21 = load_dataset21()

# Dataset21 asli:
# 0 = Normal
# 1 = F_I
#
# Model global:
# 0 = Normal
# 3 = F_I

y_train21 = remap_dataset21_labels(
    y_train21
)

print(f"Train shape: {x_train21.shape}")

unique, counts = np.unique(
    y_train21,
    return_counts=True
)

for cls, count in zip(unique, counts):
    print(f"Class {cls}: {count}")


# ==============================
# LOAD DATASET21 VALIDATION
# ==============================

print("\n===== LOAD DATASET21 VALIDATION =====")

x_val21, y_val21 = load_validation_data21()

print(f"Validation shape: {x_val21.shape}")


# ==============================
# LOAD MODEL V1
# ==============================

print("\n===== LOAD INITIAL MODEL V1 =====")

model = load_model(
    INITIAL_GLOBAL_MODEL_PATH
)

print(
    f"Total parameter: "
    f"{model.count_params():,}"
)


# ==============================
# COMPILE ULANG
# ==============================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ==============================
# EVALUASI SEBELUM FINE-TUNING
# ==============================

print("\n===== BEFORE FINE-TUNING =====")

loss_before, acc_before = model.evaluate(
    x_val21,
    y_val21,
    verbose=1
)

print(
    f"Loss     : {loss_before:.4f}\n"
    f"Accuracy : {acc_before:.4f}"
)


# ==============================
# FINE-TUNING DATASET21 ONLY
# ==============================

print("\n===== FINE-TUNING DATASET21 ONLY =====")

history = model.fit(
    x_train21,
    y_train21,
    validation_data=(
        x_val21,
        y_val21
    ),
    epochs=20,
    batch_size=BATCH_SIZE,
    verbose=1,
    shuffle=True
)


# ==============================
# EVALUASI AKHIR
# ==============================

print("\n===== AFTER FINE-TUNING =====")

loss_after, acc_after = model.evaluate(
    x_val21,
    y_val21,
    verbose=1
)

print(
    f"Loss     : {loss_after:.4f}\n"
    f"Accuracy : {acc_after:.4f}"
)


# ==============================
# DISTRIBUSI PREDIKSI
# ==============================

y_prob = model.predict(
    x_val21,
    verbose=0
)

y_pred = np.argmax(
    y_prob,
    axis=1
)

unique, counts = np.unique(
    y_pred,
    return_counts=True
)

print("\n===== PREDICTION DISTRIBUTION =====")

for cls, count in zip(unique, counts):
    print(f"Class {cls}: {count}")


# ==============================
# CONFUSION MATRIX SEDERHANA
# ==============================

print("\n===== CONFUSION MATRIX =====")

cm = tf.math.confusion_matrix(
    y_val21,
    y_pred,
    num_classes=6
)

print(cm.numpy())