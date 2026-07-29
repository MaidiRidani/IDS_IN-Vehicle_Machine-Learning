import os
import re
import time
import shutil
from datetime import datetime

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==========================================================
# CONFIG
# ==========================================================

MODEL_PATH = "model/global_model.h5"

WATCH_FOLDER = "watch"
PROCESSED_FOLDER = "processed"

SAVE_NPY = True
SAVE_VISUALIZATION = True
IMAGE_FORMAT = "PNG"       # Ganti menjadi "JPEG" jika diperlukan
IMAGE_EXTENSION = ".png"   # Jika JPEG: ".jpg"

os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

LABELS = {
    0: "Normal",
    1: "F_I",
    2: "P_I",
    3: "M_F",
    4: "C_D",
    5: "C_R"
}

def create_detection_visual(
    image_data,
    source_name,
    ground_truth,
    prediction,
    confidence,
    inference_ms,
    class_probabilities,
    output_path,
    timestamp,
):
    """
    Membuat output detector berupa:
    - 4 visualisasi wavelet dalam grid 2x2
    - panel informasi hasil prediksi di pojok kiri atas
    """

    # ---------------------------------------------------------
    # 1. Normalisasi khusus visualisasi
    #    Jangan mengubah image_data yang masuk ke model.
    # ---------------------------------------------------------
    vis = image_data.astype(np.float32).copy()
    vis = (vis - vis.min()) / (vis.max() - vis.min() + 1e-8)

    # ---------------------------------------------------------
    # 2. Status prediksi
    # ---------------------------------------------------------

    if ground_truth == "Unknown":
        status_text = "GT NOT AVAILABLE"
        status_color = "#ffc107"

    elif prediction == ground_truth:
        status_text = "CORRECT"
        status_color = "#00d26a"

    else:
        status_text = "WRONG"
        status_color = "#ff4d4d"

    # ---------------------------------------------------------
    # 3. Figure 2x2
    # ---------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    fig.patch.set_facecolor("#161616")

    for ax in axes.flat:
        ax.set_facecolor("#161616")
        ax.axis("off")

    # kiri atas: hasil gabungan RGB
    axes[0, 0].imshow(vis)
    axes[0, 0].set_title(
        "3 Wavelet (RGB)",
        color="white",
        fontsize=12,
        fontweight="bold",
        pad=10,
    )

    # kanan atas: channel coif1
    axes[0, 1].imshow(vis[:, :, 0], cmap="viridis")
    axes[0, 1].set_title(
        "LL - coif1",
        color="white",
        fontsize=12,
        fontweight="bold",
        pad=10,
    )

    # kiri bawah: channel db3
    axes[1, 0].imshow(vis[:, :, 1], cmap="viridis")
    axes[1, 0].set_title(
        "LL - db3",
        color="white",
        fontsize=12,
        fontweight="bold",
        pad=10,
    )

    # kanan bawah: channel rbio1.3
    axes[1, 1].imshow(vis[:, :, 2], cmap="viridis")
    axes[1, 1].set_title(
        "LL - rbio1.3",
        color="white",
        fontsize=12,
        fontweight="bold",
        pad=10,
    )

    # Ruang atas khusus panel informasi
    plt.subplots_adjust(
        left=0.05,
        right=0.98,
        bottom=0.05,
        top=0.66,      # gambar dan judul subplot turun
        wspace=0.08,
        hspace=0.18,   # beri jarak sedikit lebih besar antarbaris
    )

    # ---------------------------------------------------------
    # 4. Panel informasi prediksi
    # ---------------------------------------------------------
    panel_x = 0.06
    panel_y = 0.75
    panel_w = 0.88
    panel_h = 0.20
    # Padding internal panel dalam koordinat figure
    pad_x = 0.025
    pad_y = 0.010

    panel = FancyBboxPatch(
        (panel_x, panel_y),
        panel_w,
        panel_h,
        boxstyle="round,pad=0.012,rounding_size=0.015",
        transform=fig.transFigure,
        facecolor="#080d0a",
        edgecolor=status_color,
        linewidth=2.0,
        alpha=0.94,
    )
    fig.add_artist(panel)

    # Urutkan probabilitas terbesar ke terkecil
    sorted_probs = sorted(
        class_probabilities.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    probability_text = "\n".join(
        [f"{label}: {prob * 100:.2f}%" for label, prob in sorted_probs]
    )

    info_left = (
        "FL-IDS IoV DETECTION RESULT\n"
        f"Source      : {source_name}\n"
        f"Image Size  : {image_data.shape[0]}×{image_data.shape[1]}×{image_data.shape[2]}\n"
        f"Ground Truth: {ground_truth}\n"
        f"Prediction  : {prediction}\n"
        f"Confidence  : {confidence * 100:.2f}%\n"
        f"Inference   : {inference_ms:.2f} ms\n"
        f"Timestamp   : {timestamp}"
    )

    fig.text(
        panel_x + pad_x,
        panel_y + panel_h - pad_y,
        info_left,
        color="#e8e8e8",
        fontsize=9,
        family="monospace",
        va="top",
        ha="left",
        linespacing=1.35,
    )
    right_x = panel_x + 0.55
    top_y = panel_y + panel_h - pad_y

    fig.text(
        right_x,
        top_y,
        "STATUS",
        color="#e8e8e8",
        fontsize=9,
        fontweight="bold",
        family="monospace",
        va="top",
        ha="left",
    )

    fig.text(
        right_x,
        top_y - 0.030,
        status_text,
        color=status_color,
        fontsize=12,
        fontweight="bold",
        family="monospace",
        va="top",
        ha="left",
    )

    fig.text(
        right_x,
        top_y - 0.070,
        "CLASS PROBABILITIES",
        color="#e8e8e8",
        fontsize=9,
        fontweight="bold",
        family="monospace",
        va="top",
        ha="left",
    )

    fig.text(
        right_x,
        top_y - 0.095,
        probability_text,
        color="#d0d0d0",
        fontsize=8,
        family="monospace",
        va="top",
        ha="left",
        linespacing=1.25,
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    plt.close(fig)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_ground_truth_from_filename(filename):
    """
    Mengambil GT dari nama file.

    Contoh:
    sample_001_GT-Normal.npy
    sample_002_GT-C_D.npy
    """

    match = re.search(r"_GT-([A-Za-z0-9_]+)", filename)

    if match:
        gt_label = match.group(1)

        if gt_label in LABELS.values():
            return gt_label

    return "Unknown"



# ==========================================================
# LOAD MODEL
# ==========================================================

print("=" * 60)
print("Loading Global Federated Model...")
print("=" * 60)

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

print("Model Loaded Successfully")
print()

print(f"Watching Folder   : {WATCH_FOLDER}")
print(f"Processed Folder  : {PROCESSED_FOLDER}")
print("\nWaiting for sample...\n")


# ==========================================================
# EVENT HANDLER
# ==========================================================

def print_waiting_status():
    """
    Menampilkan status bahwa detector kembali siap
    menerima file sample berikutnya.
    """

    print("\n" + "=" * 60)
    print("Waiting for next sample...")
    print("=" * 60 + "\n")

class SampleHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.endswith(".npy"):
            return

        time.sleep(0.2)

        print("=" * 60)
        print("New Sample Detected")
        print("=" * 60)

        old_name = os.path.basename(event.src_path)
        print(f"File : {old_name}")

        try:

            # --------------------------------------------------
            # LOAD SAMPLE
            # --------------------------------------------------

            sample = np.load(event.src_path)
            if sample.shape != (64, 64, 3):

                print("\nERROR")
                print("-" * 30)
                print(
                    f"Invalid sample shape: {sample.shape}\n"
                    "Expected shape       : (64, 64, 3)"
                )

                filename, extension = os.path.splitext(old_name)

                error_destination = os.path.join(
                    PROCESSED_FOLDER,
                    f"{filename}_ERROR-INVALID_SHAPE{extension}"
                )

                shutil.move(
                    event.src_path,
                    error_destination
                )

                print("\nInvalid file moved to:")
                print(error_destination)

                print("\nReturning to waiting mode...")
                time.sleep(2)

                print_waiting_status()
                return

            # Simpan sebelum batch dimension ditambahkan
            original_sample = sample.copy()
            print("\nDWT Value Range")
            print("-" * 30)

            for channel in range(sample.shape[-1]):

                channel_data = sample[:, :, channel]

                print(
                    f"Channel {channel} | "
                    f"min={channel_data.min():.6f} | "
                    f"max={channel_data.max():.6f} | "
                    f"mean={channel_data.mean():.6f}"
                )

            gt_label = get_ground_truth_from_filename(old_name)

            sample_batch = np.expand_dims(sample, axis=0)

            # --------------------------------------------------
            # INFERENCE
            # --------------------------------------------------

            start = time.perf_counter()

            prediction = model.predict(
                sample_batch,
                verbose=0
            )

            inference_time = (
                time.perf_counter() - start
            ) * 1000

            pred_idx = int(np.argmax(prediction[0]))
            pred_label = LABELS[pred_idx]
            confidence = float(prediction[0][pred_idx] * 100)

            # --------------------------------------------------
            # TERMINAL OUTPUT
            # --------------------------------------------------

            print("\nPrediction Result")
            print("-" * 30)
            print(f"Ground Truth : {gt_label}")
            print(f"Prediction   : {pred_label}")
            print(f"Confidence   : {confidence:.2f}%")
            print(f"Inference    : {inference_time:.2f} ms")

            if gt_label != "Unknown":
                print(
                    f"Status       : "
                    f"{'CORRECT' if gt_label == pred_label else 'WRONG'}"
                )

            # --------------------------------------------------
            # BUILD OUTPUT NAME
            # --------------------------------------------------

            filename, extension = os.path.splitext(old_name)

            confidence_text = (
                f"{confidence:.2f}"
                .replace(".", "p")
            )

            base_output_name = (
                f"{filename}"
                f"_PRED-{pred_label}"
                f"_CONF-{confidence_text}"
            )

            # --------------------------------------------------
            # SAVE NPY
            # --------------------------------------------------

            if SAVE_NPY:

                npy_destination = os.path.join(
                    PROCESSED_FOLDER,
                    base_output_name + extension
                )

                shutil.move(
                    event.src_path,
                    npy_destination
                )

                print("\nNPY Saved")
                print("-" * 30)
                print(npy_destination)

            # --------------------------------------------------
            # SAVE VISUALIZATION IMAGE
            # --------------------------------------------------

            if SAVE_VISUALIZATION:

                image_destination = os.path.join(
                    PROCESSED_FOLDER,
                    base_output_name + IMAGE_EXTENSION
                )

                # Ubah output softmax menjadi dictionary agar
                # dapat ditampilkan pada panel class probabilities.
                class_probabilities = {
                    LABELS[index]: float(probability)
                    for index, probability in enumerate(prediction[0])
                }

                create_detection_visual(
                    image_data=original_sample,
                    source_name=old_name,
                    ground_truth=gt_label,
                    prediction=pred_label,

                    # create_detection_visual mengharapkan confidence
                    # dalam skala 0-1, bukan persen.
                    confidence=confidence / 100.0,

                    inference_ms=inference_time,
                    class_probabilities=class_probabilities,
                    output_path=image_destination,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )

                print("\nVisualization Saved")
                print("-" * 30)
                print(image_destination)

            print("\nWaiting for next sample...\n")

        except Exception as e:

            print("\nERROR")
            print("-" * 30)
            print(e)

            try:
                if os.path.exists(event.src_path):

                    filename, extension = os.path.splitext(old_name)

                    error_destination = os.path.join(
                        PROCESSED_FOLDER,
                        f"{filename}_ERROR-PROCESSING{extension}"
                    )

                    shutil.move(
                        event.src_path,
                        error_destination
                    )

                    print("\nProblematic file moved to:")
                    print(error_destination)

            except Exception as move_error:
                print("\nFailed to move problematic file:")
                print(move_error)

            print_waiting_status()


# ==========================================================
# START WATCHDOG
# ==========================================================

observer = Observer()

observer.schedule(
    SampleHandler(),
    WATCH_FOLDER,
    recursive=False
)

observer.start()

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("\nStopping detector...")
    observer.stop()

observer.join()