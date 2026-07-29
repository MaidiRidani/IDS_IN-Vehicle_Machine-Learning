# ==========================================================
# SERVER
#
# Tugas:
# - Menyimpan global model
# - Mengirim global weights
# - Menerima update client
# - Melakukan agregasi
# - Evaluasi validation
# ==========================================================

import gc
import os

from typing import List

import numpy as np
from tensorflow.keras.models import load_model

from config import (
    NUM_CLIENTS,
    INITIAL_GLOBAL_MODEL_PATH,
)

from dataset import load_validation_data

from strategy import fedavg_aggregate

# ==========================================================
# LOAD INITIAL MODEL
# ==========================================================

print("\nLoading Initial Global Model...")

if not os.path.exists(INITIAL_GLOBAL_MODEL_PATH):
    raise FileNotFoundError(
        INITIAL_GLOBAL_MODEL_PATH
    )

global_model = load_model(
    INITIAL_GLOBAL_MODEL_PATH
)

global_weights = global_model.get_weights()

print("Global model loaded.")

print(
    f"Total Parameters : "
    f"{global_model.count_params():,}"
)

# ==========================================================
# LOAD VALIDATION SET
# ==========================================================

x_val, y_val = load_validation_data()

print(
    f"Validation Samples : {len(y_val)}"
)

# ==========================================================
# CLIENT IDS
# ==========================================================

CLIENT_IDS = list(
    range(NUM_CLIENTS)
)

# ==========================================================
# GLOBAL WEIGHTS
# ==========================================================

def get_global_weights(
    client_id: int,
) -> List[np.ndarray]:

    if client_id not in CLIENT_IDS:

        raise ValueError(
            f"Client {client_id} tidak valid."
        )

    return global_weights


# ==========================================================
# UPDATE GLOBAL MODEL
# ==========================================================

def update_global_model(
    aggregated_weights,
):

    global global_weights

    global_weights = aggregated_weights

    global_model.set_weights(
        aggregated_weights
    )


# ==========================================================
# VALIDATION
# ==========================================================

def evaluate_validation():

    print()

    print("=" * 60)
    print("GLOBAL VALIDATION")
    print("=" * 60)

    loss, acc = global_model.evaluate(

        x_val,

        y_val,

        verbose=1,

    )

    print()

    print(
        f"Validation Loss     : {loss:.6f}"
    )

    print(
        f"Validation Accuracy : {acc:.4f}"
    )

    return loss, acc


# ==========================================================
# ONE ROUND
# ==========================================================

def run_one_round(
    client_update_fn,
):

    print()

    print("=" * 70)
    print("START FEDERATED ROUND")
    print("=" * 70)

    # ------------------------------------------------------
    # Snapshot global model
    # ------------------------------------------------------

    base_weights = global_model.get_weights()

    client_weights = []

    client_sizes = []

    client_ids = []

    # ------------------------------------------------------
    # Local Training
    # ------------------------------------------------------

    for client_id in CLIENT_IDS:

        updated_weights, data_size = client_update_fn(

            client_id,

            base_weights,

        )

        client_weights.append(
            updated_weights
        )

        client_sizes.append(
            data_size
        )

        client_ids.append(
            client_id
        )

    # ------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------

    aggregated_weights = fedavg_aggregate(

        client_weights=client_weights,

        client_sizes=client_sizes,

        client_ids=client_ids,

    )

    # ------------------------------------------------------
    # Update Global Model
    # ------------------------------------------------------

    update_global_model(
        aggregated_weights
    )

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    loss, acc = evaluate_validation()

    # ------------------------------------------------------
    # Clean Memory
    # ------------------------------------------------------

    del client_weights
    del client_sizes
    del client_ids
    del aggregated_weights
    del base_weights

    gc.collect()

    print()

    print("=" * 60)
    print("ROUND FINISHED")
    print("=" * 60)

    print(
        f"Validation Loss : {loss:.6f}"
    )

    print(
        f"Validation Acc  : {acc:.4f}"
    )

    return loss, acc


# ==========================================================
# CLEAR VALIDATION DATA
# ==========================================================

def clear_validation_data():

    global x_val
    global y_val

    del x_val
    del y_val

    gc.collect()

    print(
        "Validation data cleared."
    )