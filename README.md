# IDS_IN-Vehicle_Machine-Learning

A research repository for developing machine learning-based Intrusion Detection Systems (IDS) for modern In-Vehicle Networks.

This repository contains the implementation, experiments, and supporting tools developed throughout my undergraduate final project. The research focuses on improving intrusion detection for modern in-vehicle communication using deep learning and Federated Learning.

---

## Overview

Modern vehicles rely on high-speed in-vehicle communication networks to exchange data among Electronic Control Units (ECUs), sensors, and safety-critical applications. As these networks become increasingly connected and complex, they also become more vulnerable to cyber attacks.

This research investigates a deep learning-based Intrusion Detection System (IDS) for modern Automotive Ethernet networks. The proposed approach combines packet preprocessing, multi-wavelet feature extraction, and a lightweight neural network architecture to improve attack detection while maintaining computational efficiency.

---

## Proposed Preprocessing Pipeline

The following figure illustrates the complete preprocessing pipeline used to transform raw packet traffic into image representations suitable for deep learning models.

<p align="center">
    <img src="preprocessing%20pipeline.jpg" width="100%">
</p>

The preprocessing pipeline consists of:

- Raw packet collection from Automotive Ethernet traffic.
- Packet parsing and byte extraction.
- Packet standardization using padding or truncation.
- Construction of packet-byte matrices.
- Sliding window generation.
- Normalization.
- Multi-wavelet decomposition.
- RGB image generation for model input.

---

## Proposed Model: DPDNet-Lite

The primary contribution of this research is **DPDNet-Lite**, a lightweight deep learning architecture specifically designed for intrusion detection in modern in-vehicle networks.

<p align="center">
    <img src="structure%20DPDNet-Lite.jpg" width="100%">
</p>

DPDNet-Lite is designed to:

- Learn spatial packet representations extracted from multi-wavelet images.
- Reduce computational complexity using factorized convolutions.
- Capture directional packet features through Dual-Path Directional Blocks.
- Provide lightweight inference while maintaining competitive detection performance.

---

## Repository Contents

This repository includes:

- **DPDNet_Lite**, the proposed IDS architecture.
- Reference implementations of existing IDS models for comparison:
  - MRTCN
  - Swin Transformer
- Experiments using the TOW-IDS dataset.
- Wavelet preprocessing studies.
- Federated Learning experiments.
- A web-based dashboard for preprocessing and inference.

---

## Repository Structure

```text
.
├── tow_ids/                     # Proposed DPDNet_Lite model and TOW-IDS experiments
├── mrtcn_ids/                   # MRTCN reference implementation
├── swin_ids/                    # Swin Transformer reference implementation
├── WaveletPerbandingan/         # Wavelet preprocessing experiments
├── FLwaveletperbandingan/       # Federated Learning experiments
├── ReplikasiNewModel(gambar)/   # DPDNet-Lite architecture design
├── vehicleidsdashboard/         # Dashboard (React + FastAPI)
├── README.md
```

---

## Dataset

The primary dataset used in this research is:

- **TOW-IDS**

The dataset represents modern Automotive Ethernet communication and includes both normal traffic and multiple attack scenarios for intrusion detection research.

---

## Contact

If you have any questions, suggestions, or would like to discuss this research, please feel free to contact me.

**Maidi Ridani**

- GitHub: https://github.com/MaidiRidani
- Email: dani.maidiridani@gmail.com

> **Note:** If you contact me via email regarding this repository, please use **"GitHub Q&A"** as the email subject to help me identify and prioritize your message.
