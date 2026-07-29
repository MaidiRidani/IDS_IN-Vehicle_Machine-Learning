import os
import random
import time
from prompt_toolkit import prompt
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn
)

DATASET_FOLDER = "datasetdwt"


def list_dataset():
    """
    Mencari seluruh file dataset (.npz) yang berada
    di folder datasetdwt.

    Returns
    -------
    list[str]
        Daftar nama file dataset yang telah diurutkan.
    """

    if not os.path.exists(DATASET_FOLDER):
        os.makedirs(DATASET_FOLDER)

    datasets = [
        file
        for file in os.listdir(DATASET_FOLDER)
        if file.endswith(".npz")
    ]

    datasets.sort()

    return datasets

def choose_dataset():
    """
    Menampilkan daftar dataset kemudian meminta
    pengguna memilih salah satu dataset.

    Returns
    -------
    str
        Path lengkap menuju dataset yang dipilih.
    """

    while True:

        datasets = list_dataset()

        print("\n" + "=" * 55)
        print("              AVAILABLE DATASET")
        print("=" * 55)

        if len(datasets) == 0:
            print("\nTidak ada dataset di folder datasetdwt.")
            input("\nTekan ENTER untuk refresh...")
            continue

        for i, file in enumerate(datasets, start=1):
            print(f"[{i}] {file}")

        choice = input("\nPilih dataset : ")

        if not choice.isdigit():
            print("\nInput harus berupa angka.")
            continue

        choice = int(choice)

        if choice < 1 or choice > len(datasets):
            print("\nNomor dataset tidak tersedia.")
            continue

        return os.path.join(DATASET_FOLDER, datasets[choice - 1])
    
import numpy as np


def load_dataset(dataset_path):
    """
    Membaca dataset DWT dari file NPZ.

    Parameters
    ----------
    dataset_path : str
        Path menuju file NPZ.

    Returns
    -------
    X : ndarray
        Array DWT.

    y : ndarray
        Label setiap sample.
    """

    data = np.load(dataset_path)

    X = data["X"]
    y = data["y"]

    return X, y



LABELS = {
    0: "Normal",
    1: "F_I",
    2: "P_I",
    3: "M_F",
    4: "C_D",
    5: "C_R"
}


def show_dataset_info(dataset_path, X, y):
    """
    Menampilkan informasi lengkap dataset yang dipilih.
    """

    print("\n" + "=" * 55)
    print("              DATASET INFORMATION")
    print("=" * 55)

    print(f"File      : {os.path.basename(dataset_path)}")
    print(f"Samples   : {len(X)}")
    print(f"Shape     : {X.shape[1:]}")
    print(f"Channels  : {X.shape[-1]}")

    print("\nLabel Distribution")

    unique, counts = np.unique(y, return_counts=True)

    for label, count in zip(unique, counts):

        name = LABELS.get(int(label), f"Unknown({label})")

        print(f"{name:<10}: {count}")


def choose_mode():
    """
    Menampilkan menu mode pengiriman sample.

    Returns
    -------
    str
        "single" atau "multiple"
    """

    while True:

        print("\n" + "=" * 55)
        print("                 SELECT MODE")
        print("=" * 55)

        print("[1] Single Sample")
        print("[2] Multiple Sample")

        choice = input("\nPilih mode : ").strip()

        if choice == "1":
            return "single"

        elif choice == "2":
            return "multiple"

        else:
            print("\nPilihan tidak tersedia.")


def choose_selection_method(mode):
    """
    Memilih cara menentukan sample.

    Parameters
    ----------
    mode : str
        "single" atau "multiple"

    Returns
    -------
    str
        "manual" atau "random_label"
    """

    while True:

        print("\n" + "=" * 55)
        print("            SELECT SAMPLE METHOD")
        print("=" * 55)

        print("[1] Manual Sample Number")

        if mode == "single":
            print("[2] Random Sample by Label")
        else:
            print("[2] Random Samples by Label Quantity")

        choice = prompt("\nPilih metode : ").strip()

        if choice == "1":
            return "manual"

        if choice == "2":
            return "random_label"

        print("\nERROR : Pilihan tidak tersedia.")


def build_label_index(y):
    """
    Membuat mapping label ke seluruh indeks sample
    yang memiliki label tersebut.

    Parameters
    ----------
    y : ndarray
        Label seluruh sample dataset.

    Returns
    -------
    dict[int, list[int]]
        Contoh:
        {
            0: [0, 1, 4, ...],
            1: [2, 3, 8, ...]
        }
    """

    label_index = {}

    for label_id in LABELS:
        label_index[label_id] = np.where(y == label_id)[0].tolist()

    return label_index

def show_label_menu(label_index):
    """
    Menampilkan label yang tersedia beserta jumlah
    sample pada dataset aktif.
    """

    print("\n" + "=" * 55)
    print("               AVAILABLE LABELS")
    print("=" * 55)

    for label_id, label_name in LABELS.items():

        available = len(label_index[label_id])

        print(f"[{label_id}] {label_name:<10} ({available} sample)")
    



def choose_random_single(label_index):
    """
    Memilih satu sample acak berdasarkan label yang dipilih.

    Returns
    -------
    list[int]
        Satu indeks sample dalam list.
    """

    while True:

        show_label_menu(label_index)

        text = prompt("\nPilih label : ").strip()

        if not text.isdigit():
            print("\nERROR : Label harus berupa angka.")
            continue

        label_id = int(text)

        if label_id not in LABELS:
            print("\nERROR : Label tidak tersedia.")
            continue

        available_samples = label_index[label_id]

        if len(available_samples) == 0:
            print("\nERROR : Tidak ada sample untuk label tersebut.")
            continue

        selected_idx = random.choice(available_samples)

        print(
            f"\nRandom sample selected: {selected_idx} "
            f"({LABELS[label_id]})"
        )

        return [selected_idx]
    

def parse_label_request(text, label_index):
    """
    Memvalidasi permintaan jumlah sample acak per label.

    Format
    ------
    label_id:jumlah,label_id:jumlah

    Contoh
    -------
    0:10,1:20,2:5

    Returns
    -------
    valid : bool

    result :
        Jika valid:
            dict[int, int]

        Jika tidak valid:
            str
    """

    text = text.strip()

    if text == "":
        return False, "Input tidak boleh kosong."

    requests = {}

    parts = text.split(",")

    for part in parts:

        part = part.strip()

        if part == "":
            return False, "Input mengandung bagian kosong."

        if ":" not in part:
            return (
                False,
                f"Format '{part}' salah. Gunakan label:jumlah."
            )

        label_text, quantity_text = part.split(":", 1)

        label_text = label_text.strip()
        quantity_text = quantity_text.strip()

        if not label_text.isdigit():
            return False, f"Label '{label_text}' harus berupa angka."

        if not quantity_text.isdigit():
            return False, (
                f"Jumlah '{quantity_text}' harus berupa angka."
            )

        label_id = int(label_text)
        quantity = int(quantity_text)

        if label_id not in LABELS:
            return False, f"Label {label_id} tidak tersedia."

        if quantity <= 0:
            return False, (
                f"Jumlah untuk {LABELS[label_id]} harus lebih dari 0."
            )

        if label_id in requests:
            return False, (
                f"Label {LABELS[label_id]} ditulis lebih dari sekali."
            )

        available = len(label_index[label_id])

        if quantity > available:
            return False, (
                f"Permintaan {quantity} sample {LABELS[label_id]} "
                f"melebihi stok tersedia ({available})."
            )

        requests[label_id] = quantity

    return True, requests


def choose_random_multiple(label_index):
    """
    Memilih beberapa sample acak sesuai jumlah yang
    diminta pada setiap label.

    Returns
    -------
    list[int]
        Indeks sample terpilih.
    """

    previous_input = ""

    while True:

        show_label_menu(label_index)

        print("\nFormat request : label:jumlah,label:jumlah")
        print("Contoh         : 0:10,1:20,2:5,3:5,4:5,5:5")

        text = prompt(
            "\nRequest sample : ",
            default=previous_input
        )

        ok, result = parse_label_request(
            text,
            label_index
        )

        if not ok:

            previous_input = text

            print(f"\nERROR : {result}")

            continue

        selected = []

        for label_id, quantity in result.items():

            chosen = random.sample(
                label_index[label_id],
                quantity
            )

            selected.extend(chosen)

        # Acak urutan pengiriman agar tidak terkumpul
        # per kelas, misalnya 10 Normal dulu lalu 20 F_I.
        random.shuffle(selected)

        return selected

def parse_sample_input(text, total_sample, mode):
    """
    Memvalidasi input nomor sample dari pengguna.

    Parameters
    ----------
    text : str
        Contoh:
            Single   : "25"
            Multiple : "4,60,70"

    total_sample : int
        Jumlah sample pada dataset.

    mode : str
        "single" atau "multiple"

    Returns
    -------
    valid : bool

    result :
        Jika valid:
            {
                "samples": list[int],
                "duplicate": bool
            }

        Jika tidak valid:
            str (pesan error)
    """

    text = text.strip()

    if text == "":
        return False, "Input tidak boleh kosong."

    parts = text.split(",")

    # ------------------------------------
    # Validasi mode Single
    # ------------------------------------
    if mode == "single" and len(parts) > 1:
        return False, "Mode Single hanya menerima satu nomor sample."

    samples = []

    for part in parts:

        part = part.strip()

        # Input kosong
        if part == "":
            return False, "Input mengandung nilai kosong."

        # Harus angka
        if not part.isdigit():
            return False, f"'{part}' bukan nomor yang valid."

        idx = int(part)

        # Rentang
        if idx < 0 or idx >= total_sample:
            return (
                False,
                f"Sample {idx} berada di luar rentang "
                f"(0 - {total_sample - 1})."
            )

        samples.append(idx)

    # ------------------------------------
    # Cek duplikasi
    # ------------------------------------
    duplicate = len(samples) != len(set(samples))

    return True, {
        "samples": samples,
        "duplicate": duplicate
    }




from collections import Counter


def preview_selection(selected, y, duplicate=False):
    """
    Menampilkan ringkasan sample yang dipilih sebelum
    dikirim ke detector.

    Parameters
    ----------
    selected : list[int]
        Daftar nomor sample yang dipilih.

    y : ndarray
        Ground truth seluruh dataset.

    duplicate : bool
        True jika terdapat sample yang dipilih lebih dari sekali.

    Returns
    -------
    bool

        True  -> lanjut kirim ke detector

        False -> kembali ke input sample
    """

    print("\n" + "=" * 60)
    print("                  SELECTED SAMPLES")
    print("=" * 60)

    print(f"\n{'No':<5}{'Sample':<12}{'Ground Truth'}")
    print("-" * 40)

    summary = []

    for no, sample_idx in enumerate(selected, start=1):

        label = LABELS.get(int(y[sample_idx]), f"Unknown ({y[sample_idx]})")

        summary.append(label)

        print(f"{no:<5}{sample_idx:<12}{label}")

    print("-" * 40)

    print(f"Total Selected : {len(selected)}")

    # =====================================================
    # Summary Label
    # =====================================================

    print("\nLabel Summary")
    print("-" * 20)

    counter = Counter(summary)

    for label in LABELS.values():

        if label in counter:
            print(f"{label:<10}: {counter[label]}")

    # =====================================================
    # Duplicate Warning
    # =====================================================

    if duplicate:

        print("\nWARNING")
        print("-" * 20)
        print("Duplicate sample detected.")
        print("Sample akan tetap dikirim.")

    print("\n" + "=" * 60)

    while True:

        choice = prompt(
            "\nContinue? [Y/N] : ",
            default="Y"
        ).strip().upper()

        if choice == "Y":
            return True

        if choice == "N":
            return False

        print("Input harus Y atau N.")



WATCH_FOLDER = "watch"

os.makedirs(WATCH_FOLDER, exist_ok=True)


def send_to_watch(selected, X, y):
    """
    Mengirim sample ke folder watch dan menunggu
    hingga detector selesai memproses setiap sample.
    """

    print()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
    ) as progress:

        task = progress.add_task(
            "Sending Samples",
            total=len(selected)
        )

        for sample_idx in selected:

            sample = X[sample_idx]

            label = LABELS[int(y[sample_idx])]

            filename = (
                f"sample_{sample_idx:06d}"
                f"_GT-{label}.npy"
            )
            final_path = os.path.join(
                WATCH_FOLDER,
                filename
            )

            np.save(final_path, sample)

            # --------------------------
            # Tunggu detector selesai
            # --------------------------

            while os.path.exists(final_path):
                time.sleep(0.05)

            progress.advance(task)

    print("\nAll samples have been processed.\n")


def run_sender():
    """
    Menjalankan proses pemilihan dan pengiriman sample
    ke Live Detector.
    """

    dataset_path = choose_dataset()

    X, y = load_dataset(dataset_path)

    print("\nRAW LABEL CHECK")
    print("y shape :", y.shape)
    print("y dtype :", y.dtype)

    unique, counts = np.unique(y, return_counts=True)

    print("\nUnique labels in selected NPZ:")

    for label, count in zip(unique, counts):
        print(f"{repr(label)} : {count}")
    show_dataset_info(dataset_path, X, y)

    mode = choose_mode()

    selection_method = choose_selection_method(mode)

    label_index = build_label_index(y)

    # ======================================================
    # RANDOM LABEL MODE
    # ======================================================

    if selection_method == "random_label":

        if mode == "single":
            selected = choose_random_single(label_index)

        else:
            selected = choose_random_multiple(label_index)

        duplicate = False

        while True:

            if preview_selection(selected, y, duplicate):

                send_to_watch(selected, X, y)

                print("\nSample berhasil dikirim.\n")
                return

            # Jika preview dibatalkan, random ulang.
            if mode == "single":
                selected = choose_random_single(label_index)
            else:
                selected = choose_random_multiple(label_index)

    # ======================================================
    # MANUAL MODE
    # ======================================================

    previous_input = ""

    while True:

        print(f"\nAvailable Sample : 0 - {len(X) - 1}")

        if mode == "single":
            print("Example : 25")
        else:
            print("Example : 4,60,70")

        text = prompt(
            "\nSample Number : ",
            default=previous_input
        )

        ok, result = parse_sample_input(
            text=text,
            total_sample=len(X),
            mode=mode
        )

        if not ok:

            previous_input = text

            print(f"\nERROR : {result}")

            continue

        selected = result["samples"]
        duplicate = result["duplicate"]

        if preview_selection(selected, y, duplicate):

            send_to_watch(selected, X, y)

            print("\nSample berhasil dikirim.\n")
            return

        print("\nPemilihan sample dibatalkan.\n")

def main():

    while True:

        print("\n" + "=" * 60)
        print("            DWT DATASET MANAGER")
        print("=" * 60)

        print("[1] Send Sample")
        print("[0] Exit")

        choice = prompt(
            "\nChoice : ",
            default="1"
        ).strip()

        if choice == "1":

            run_sender()

        elif choice == "0":

            print("\nExiting...")
            break

        else:

            print("\nERROR : Invalid menu.")

if __name__ == "__main__":
    main()