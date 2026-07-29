# ==============================
# IMPORT YANG DIPERLUKAN
# ==============================

import numpy as np
import gc
import torch
from tqdm import tqdm
from model import build_model
from dataset import load_client_data


mode = 2  # 1 = IID, 2 = non-IID


# ==============================
# FUNGSI: TRAINING CLIENT
# ==============================

def client_update_fn(client_id: int, global_weights):

    print(f"\n[CLIENT {client_id}] Memulai training...")

    # ==============================
    # DEVICE
    # ==============================
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ==============================
    # LOAD DATA
    # ==============================
    x_train, y_train = load_client_data(client_id=client_id, mode=mode)

    data_size = len(x_train)
    print(f"[CLIENT {client_id}] Data loaded: {data_size} samples")

    # ==============================
    # NUMPY → TORCH
    # ==============================
    x_train = torch.tensor(x_train, dtype=torch.float32).permute(0, 3, 1, 2)
    y_train = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)

    # ==============================
    # INIT MODEL
    # ==============================
    model = build_model(device)

    # ==============================
    # SET WEIGHTS (ganti set_weights)
    # ==============================
    state_dict = model.state_dict()
    new_state_dict = {}

    for k, w in zip(state_dict.keys(), global_weights):
        new_state_dict[k] = torch.tensor(w)

    model.load_state_dict(new_state_dict)

    # ==============================
    # TRAINING SETUP
    # ==============================
    pos = y_train.sum().item()
    neg = len(y_train) - pos
    pos_weight = torch.tensor([neg / pos]).to(device)
    criterion = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.05)

    model.train()

    # ==============================
    # TRAINING (ganti model.fit)
    # ==============================
    batch_size = 16
    local_epochs = 2

    total_batches = (len(x_train) + batch_size - 1) // batch_size

    for epoch in range(local_epochs):

        print(f"\n[CLIENT {client_id}] Epoch {epoch+1}/{local_epochs}")

        pbar = tqdm(
            range(0, len(x_train), batch_size),
            total=total_batches,
            desc=f"Client {client_id} Epoch {epoch+1}",
            leave=False
        )

        for i in pbar:

            x_batch = x_train[i:i+batch_size].to(device)
            y_batch = y_train[i:i+batch_size].to(device)

            optimizer.zero_grad()

            outputs = model(x_batch)

            loss = criterion(outputs, y_batch)

            # 🔍 DEBUG HANYA DI AWAL TRAINING
            if epoch == 0 and i == 0:
                print("OUTPUT SHAPE:", outputs.shape)
                print("TARGET SHAPE:", y_batch.shape)

                print("LOGITS:", outputs[:5].detach().cpu())
                probs = torch.sigmoid(outputs)
                print("PROBS :", probs[:5].detach().cpu())
                print("MEAN  :", outputs.mean().item())
                print("STD   :", outputs.std().item())

            loss.backward()
            optimizer.step()

            # 🔥 UPDATE PROGRESS BAR
            pbar.set_postfix(loss=f"{loss.item():.4f}")


    # ==============================
    # GET WEIGHTS (ganti get_weights)
    # ==============================
    updated_weights = [
        v.detach().cpu().numpy() for v in model.state_dict().values()
    ]

    # ==============================
    # CLEANUP (ganti clear_session)
    # ==============================
    del x_train
    del y_train
    del model

    torch.cuda.empty_cache()
    gc.collect()

    print(f"[CLIENT {client_id}] Training selesai & memori dibersihkan")

    # ==============================
    # RETURN
    # ==============================
    return updated_weights, data_size