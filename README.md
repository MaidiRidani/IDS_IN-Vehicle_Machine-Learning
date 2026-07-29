# IDS_IN-Vehicle_Machine-Learning

A research repository for developing machine learning-based Intrusion Detection Systems (IDS) for modern In-Vehicle Networks.

This repository contains the implementation, experiments, and supporting tools developed throughout my undergraduate final project. The research focuses on improving intrusion detection for modern in-vehicle communication using deep learning and Federated Learning.

---

## About the Project

Modern vehicles are no longer composed of isolated Electronic Control Units (ECUs). They rely on high-speed communication networks to exchange data between sensors, controllers, and safety-critical applications. As vehicle connectivity continues to increase, protecting these internal communication networks from cyber attacks becomes increasingly important.

This research investigates the use of machine learning and deep learning techniques to detect malicious network traffic within modern in-vehicle networks. The proposed approach is evaluated using the **TOW-IDS** dataset and extended with **Federated Learning** to study collaborative model training while preserving data locality.

---

## Repository Contents

This repository includes:

- Reference implementations of existing IDS models from previous studies.
- The proposed **DPDNet_Lite** architecture.
- Experiments using the TOW-IDS dataset.
- Wavelet-based preprocessing experiments.
- Federated Learning experiments.
- A web-based dashboard for preprocessing and inference.

---

## Project Structure

```
.
├── tow_ids/                     # Proposed DPDNet_Lite model and TOW-IDS experiments
├── mrtcn_ids/                   # MRTCN reference implementation
├── swin_ids/                    # Swin Transformer reference implementation
├── WaveletPerbandingan/         # Wavelet preprocessing experiments
├── FLwaveletperbandingan/       # Federated Learning experiments
├── ReplikasiNewModel(gambar)/   # DPDNet_Lite architecture design
├── vehicleidsdashboard/         # Dashboard (React + FastAPI)
├── README.md
├── dashboard.jpeg
└── event.jpeg
```

---

## Proposed Model

The main contribution of this research is **DPDNet_Lite**, a lightweight deep learning architecture designed for intrusion detection in modern in-vehicle networks.

Reference models (MRTCN and Swin Transformer) are included for benchmarking and comparative evaluation.

---

## Dataset

Primary dataset:

- TOW-IDS

---

## Contact

For questions, discussions, collaboration, or additional information about this research, please feel free to contact me.

**Author:** Maidi Ridani

GitHub: https://github.com/MaidiRidani

Email: *your email here*

LinkedIn: *optional*
