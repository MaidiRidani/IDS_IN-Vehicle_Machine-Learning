# ==============================
# IMPORT
# ==============================
import gc
import numpy as np
import torch
from typing import List, Tuple

from model import build_model
from dataset import load_validation_data
from strategy import fedavg_aggregate


# ==============================
# DEVICE
# ==============================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ==============================
# GLOBAL MODEL
# ==============================
global_model = build_model(device)

# 🔁 ganti get_weights()
global_weights = [
    v.detach().cpu().numpy()
    for v in global_model.state_dict().values()
]


# ==============================
# VALIDATION DATA
# ==============================
x_val, y_val = load_validation_data()

# 🔁 convert ke torch (WAJIB)
x_val = torch.tensor(x_val, dtype=torch.float32).permute(0, 3, 1, 2)
y_val = torch.tensor(y_val, dtype=torch.float32).unsqueeze(1)


# ==============================
# CLIENT
# ==============================
CLIENT_IDS = [0, 1, 2, 3]


# ==============================
# GET GLOBAL WEIGHTS (TETAP)
# ==============================
def get_global_weights(client_id: int) -> List[np.ndarray]:

    if client_id not in CLIENT_IDS:
        raise ValueError(f"Client ID {client_id} tidak valid")

    return global_weights


# ==============================
# AGGREGATE (TETAP)
# ==============================
def aggregate_from_clients(
    client_weights: List[List[np.ndarray]],
    client_sizes: List[int]
) -> List[np.ndarray]:

    return fedavg_aggregate(client_weights, client_sizes)


# ==============================
# UPDATE GLOBAL MODEL
# ==============================
def update_global_model(aggregated_weights: List[np.ndarray]):

    global global_weights
    global_weights = aggregated_weights

    state_dict = global_model.state_dict()
    new_state_dict = {}

    # 🔁 ganti set_weights()
    for k, w in zip(state_dict.keys(), global_weights):
        new_state_dict[k] = torch.tensor(w)

    global_model.load_state_dict(new_state_dict)


# ==============================
# EVALUASI (GANTI evaluate())
# ==============================
def evaluate_global_model() -> Tuple[float, float, float, float]:

    print("\n[SERVER] Evaluasi Global Model (Validation)...")

    global_model.eval()
    criterion = torch.nn.BCEWithLogitsLoss()

    with torch.no_grad():

        x = x_val.to(device)
        y = y_val.to(device)

        batch_size = 32
        outputs_list = []

        for i in range(0, len(x), batch_size):
            x_batch = x[i:i+batch_size]
            outputs_batch = global_model(x_batch)
            outputs_list.append(outputs_batch)

        outputs = torch.cat(outputs_list, dim=0)

        loss = criterion(outputs, y).item()

        preds = (torch.sigmoid(outputs) > 0.5).float()

        correct = (preds == y).sum().item()
        acc = correct / len(y)

        tp = ((preds == 1) & (y == 1)).sum().item()
        fp = ((preds == 1) & (y == 0)).sum().item()
        fn = ((preds == 0) & (y == 1)).sum().item()

        prec = tp / (tp + fp) if (tp + fp) != 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) != 0 else 0.0

    return loss, acc, prec, rec


# ==============================
# RUN ONE ROUND (MINIMAL CHANGE)
# ==============================
def run_one_round(client_update_fn):

    aggregated_weights = None
    total_data = 0

    # 🔁 ganti get_weights()
    base_weights = [w.copy() for w in global_weights]

    for client_id in CLIENT_IDS:

        updated_weights, data_size = client_update_fn(client_id, base_weights)

        if aggregated_weights is None:
            aggregated_weights = [w * data_size for w in updated_weights]
        else:
            for i in range(len(aggregated_weights)):
                aggregated_weights[i] += updated_weights[i] * data_size

        total_data += data_size

        del updated_weights
        gc.collect()

    # FEDAVG
    for i in range(len(aggregated_weights)):
        aggregated_weights[i] /= total_data

    update_global_model(aggregated_weights)

    loss, acc, prec, rec = evaluate_global_model()

    print(f"[SERVER] Validation Loss: {loss:.4f} | Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f}")

    return loss, acc, prec, rec


# ==============================
# CLEAN
# ==============================
def clear_validation_data():
    global x_val, y_val

    del x_val
    del y_val

    gc.collect()

    print("[SERVER] Validation data dibersihkan dari RAM")