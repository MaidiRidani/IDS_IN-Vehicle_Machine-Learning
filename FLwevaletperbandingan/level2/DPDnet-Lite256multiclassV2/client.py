# ==========================================================
# CLIENT V2
#
# Client mengirim:
#   - Updated Weights
#   - Jumlah Sample
#   - Class Manifest
# ==========================================================

import gc
import numpy as np
import tensorflow as tf

from model import build_model

from dataset import (
    load_client_data,
    load_client_manifest,
)

from config import (
    NUM_CLIENTS,
    BATCH_SIZE,
    LOCAL_EPOCHS,
)

# ==========================================================
# SATU MODEL UNTUK SETIAP CLIENT
# ==========================================================

CLIENT_MODELS = {
    cid: build_model()
    for cid in range(NUM_CLIENTS)
}

# ==========================================================
# LOCAL TRAINING
# ==========================================================

def client_update_fn(
    client_id: int,
    global_weights,
):
    """
    Return
    ------
    updated_weights
    data_size
    manifest
    """

    print()
    print("=" * 70)
    print(f"CLIENT {client_id}")
    print("=" * 70)

    # ======================================================
    # LOAD LOCAL DATA
    # ======================================================

    x_train, y_train = load_client_data(
        client_id
    )

    manifest = load_client_manifest(
        client_id
    )

    data_size = len(y_train)

    print(f"Total Sample : {data_size}")
    print(f"Manifest     : {manifest}")

    unique, counts = np.unique(
        y_train,
        return_counts=True
    )

    print("\nLabel Distribution")

    for cls, cnt in zip(unique, counts):

        print(
            f"Class {cls}: {cnt}"
        )

    # ======================================================
    # LOAD GLOBAL MODEL
    # ======================================================

    client_model = CLIENT_MODELS[
        client_id
    ]

    client_model.set_weights(
        global_weights
    )

    # ======================================================
    # DATASET TF
    # ======================================================

    train_ds = (
        tf.data.Dataset
        .from_tensor_slices(
            (x_train, y_train)
        )
        .batch(BATCH_SIZE)
        .prefetch(
            tf.data.AUTOTUNE
        )
    )

    # ======================================================
    # LOCAL TRAINING
    # ======================================================

    history = client_model.fit(

        train_ds,

        epochs=LOCAL_EPOCHS,

        verbose=1

    )

    print()

    print(
        f"Final Loss : "
        f"{history.history['loss'][-1]:.6f}"
    )

    if "accuracy" in history.history:

        print(
            f"Final Accuracy : "
            f"{history.history['accuracy'][-1]:.4f}"
        )

    # ======================================================
    # AMBIL WEIGHTS
    # ======================================================

    updated_weights = (
        client_model.get_weights()
    )

    # ======================================================
    # CLEAN MEMORY
    # ======================================================

    del x_train
    del y_train
    del train_ds
    del history

    gc.collect()

    print()

    print(
        f"[CLIENT {client_id}] "
        "Training Finished."
    )

    # ======================================================
    # RETURN KE SERVER
    # ======================================================

    return (

        updated_weights,

        data_size,

        manifest,

    )