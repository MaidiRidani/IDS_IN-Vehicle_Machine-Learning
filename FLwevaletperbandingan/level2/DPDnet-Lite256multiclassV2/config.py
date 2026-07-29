# ==========================
# Federated Learning Config
# ==========================

import os

NUM_CLIENTS = 4

MODE = 1          # 1=IID, 2=Non-IID

NUM_ROUNDS = 200

LOCAL_EPOCHS = 1

BATCH_SIZE = 16

RANDOM_SEED = 42

# ==========================
# Non-IID Config
# ==========================

DIRICHLET_ALPHA = 0.3

# ==========================
# PRETRAINED MODEL (Global V1)
# ==========================

MODEL_BASE_PATH = (
    "/home/dani/Documents/tugas akhir/"
    "TugasAkhir/FLwevaletperbandingan/"
    "level2/DPDnet-Lite256multiclass/"
    "saved_models1"
)

INITIAL_GLOBAL_MODEL_PATH = os.path.join(
    MODEL_BASE_PATH,
    "model_best_iid.h5"
)