# ==============================
# DEBUG LOCAL ADAPTATION CLIENT 3
# Tanpa FedAvg
# ==============================

import gc
import numpy as np
import tensorflow as tf

from config import (
    NUM_CLIENTS,
    BATCH_SIZE,
    INITIAL_GLOBAL_MODEL_PATH
)

from tensorflow.keras.models import load_model

from dataset import (
    initialize_partitions,
    load_client_data,
    load_validation_data,
    load_validation_data21
)


# ==============================
# KONFIGURASI EKSPERIMEN
# ==============================

TARGET_CLIENT = 3
LOCAL_EPOCHS = 10


# ==============================
# RANDOM SEED
# ==============================

np.random.seed(42)
tf.random.set_seed(42)


# ==============================
# BANGUN MEMORY CLIENT 3
# Penting:
# initialize_partitions() akan memanggil
# simulate_vehicle_memory_shift().
# ==============================

initialize_partitions(
    num_clients=NUM_CLIENTS
)


# ==============================
# LOAD INITIAL MODEL V1
# ==============================

print("\n[DEBUG] Loading initial V1 model...")

model = load_model(
    INITIAL_GLOBAL_MODEL_PATH
)
# ==============================
# RE-COMPILE MODEL UNTUK TRAINING
# ==============================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
    run_eagerly=False
)
print(
    f"[DEBUG] Model loaded. "
    f"Total parameter: {model.count_params():,}"
)


# ==============================
# LOAD DATA CLIENT 3
# ==============================

x_client, y_client = load_client_data(
    TARGET_CLIENT
)

print("\n===== CLIENT 3 TRAINING DATA =====")

unique, counts = np.unique(
    y_client,
    return_counts=True
)

for cls, count in zip(unique, counts):
    print(f"Class {cls}: {count}")

print(f"Total sample: {len(y_client)}")


# ==============================
# LOAD VALIDATION DATA
# ==============================

x_val23, y_val23 = load_validation_data()

x_val21, y_val21 = load_validation_data21()


# ==============================
# HELPER EVALUASI
# ==============================

def evaluate_domain(
    model,
    x_data,
    y_data,
    domain_name
):
    """
    Evaluasi loss, accuracy, dan distribusi prediksi.
    """

    loss, accuracy = model.evaluate(
        x_data,
        y_data,
        verbose=0
    )

    y_prob = model.predict(
        x_data,
        verbose=0
    )

    y_pred = np.argmax(
        y_prob,
        axis=1
    )

    classes, counts = np.unique(
        y_pred,
        return_counts=True
    )

    print(f"\n[{domain_name}]")
    print(f"Loss     : {loss:.4f}")
    print(f"Accuracy : {accuracy:.4f}")
    print("Prediction distribution:")

    for cls, count in zip(classes, counts):
        print(f"  Class {cls}: {count}")

    return loss, accuracy


# ==============================
# ROUND 0: BASELINE
# ==============================

print("\n" + "=" * 55)
print("ROUND 0 — BEFORE LOCAL TRAINING")
print("=" * 55)

evaluate_domain(
    model,
    x_val23,
    y_val23,
    "Dataset23 Validation"
)

evaluate_domain(
    model,
    x_val21,
    y_val21,
    "Dataset21 Validation"
)


# ==============================
# LOCAL TRAINING CLIENT 3 ONLY
# ==============================

train_ds = tf.data.Dataset.from_tensor_slices(
    (x_client, y_client)
).shuffle(
    buffer_size=len(y_client),
    seed=42,
    reshuffle_each_iteration=True
).batch(
    BATCH_SIZE
)


for epoch in range(1, LOCAL_EPOCHS + 1):

    print("\n" + "=" * 55)
    print(f"LOCAL EPOCH {epoch}/{LOCAL_EPOCHS}")
    print("=" * 55)

    model.fit(
        train_ds,
        epochs=1,
        verbose=1
    )

    evaluate_domain(
        model,
        x_val23,
        y_val23,
        "Dataset23 Validation"
    )

    evaluate_domain(
        model,
        x_val21,
        y_val21,
        "Dataset21 Validation"
    )


# ==============================
# CLEANUP
# ==============================

del x_client
del y_client
del x_val23
del y_val23
del x_val21
del y_val21
del train_ds

gc.collect()

print("\n[DEBUG] Selesai.")