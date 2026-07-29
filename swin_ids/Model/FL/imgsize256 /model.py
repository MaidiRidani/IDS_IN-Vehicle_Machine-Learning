# ==============================
# IMPORT
# ==============================
import torch
import timm


# ==============================
# BUILD MODEL
# ==============================
def build_model(device=None):

    # ==============================
    # INIT MODEL (Swin Transformer)
    # ==============================
    model = timm.create_model(
        'swin_tiny_patch4_window7_224',
        pretrained=False,
        num_classes=1,     # 🔥 tetap binary output
        img_size=128,
        window_size=8
    )

    # ==============================
    # DEVICE (OPSIONAL)
    # ==============================
    if device is not None:
        model = model.to(device)

    return model