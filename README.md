# IDS_IN-Vehicle_Machine-Learning

A research repository for developing machine learning-based Intrusion Detection Systems (IDS) for modern In-Vehicle Networks.

This repository contains the implementation, experiments, datasets, and supporting tools developed throughout my undergraduate final project at Politeknik Elektronika Negeri Surabaya (PENS). The research focuses on designing a lightweight deep learning-based IDS for modern Automotive Ethernet and Internet of Vehicles (IoV), with additional evaluation under Federated Learning.

---

# Overview

Modern vehicles increasingly rely on high-speed Automotive Ethernet to interconnect Electronic Control Units (ECUs), sensors, cameras, and infotainment systems. While this architecture enables advanced autonomous and connected vehicle applications, it also introduces new cybersecurity risks that cannot be addressed by traditional CAN-based security solutions.

This research proposes a lightweight Intrusion Detection System (IDS) capable of identifying multiple cyberattacks in heterogeneous in-vehicle networks. The study investigates image-based network traffic representation using Discrete Wavelet Transform (DWT), develops a custom lightweight deep learning architecture named **DPDNet-Lite**, and evaluates its performance under both centralized and Federated Learning environments.

---

# Research Objectives

The research aims to:

- Develop a lightweight IDS for modern Automotive Ethernet.
- Improve attack detection performance while maintaining low computational complexity.
- Investigate wavelet-based traffic representation for deep learning.
- Evaluate IDS performance under Centralized Learning and Federated Learning.
- Study the impact of IID and non-IID data distribution on collaborative model training.

---

# Research Environment

### Programming Language

- Python

### Deep Learning Framework

- TensorFlow
- Keras

### Federated Learning

- Flower (FedAvg)

### Supporting Libraries

- NumPy
- Pandas
- Scikit-learn
- Matplotlib

### Dashboard

- React
- FastAPI

### Development Environment

- Conda Environment
- Jupyter Notebook
- Visual Studio Code

---

# Dataset

The primary dataset used throughout this research is **TOW-IDS (Three Overlapped Wavelets Intrusion Detection System)**.

TOW-IDS represents modern heterogeneous in-vehicle communication by combining multiple Automotive Ethernet protocols instead of focusing solely on traditional CAN traffic.

### Network Protocols

The dataset contains traffic generated from:

- AVTP (Audio Video Transport Protocol)
- gPTP (General Precision Time Protocol)
- CAN over UDP

### Classification Tasks

The IDS performs multiclass classification consisting of six traffic categories:

| Class | Description |
|--------|-------------|
| Normal | Legitimate network traffic |
| F_I | Frame Injection Attack |
| P_I | gPTP Synchronization Attack |
| M_F | MAC Flooding (Switch Attack) |
| C_D | CAN Denial of Service |
| C_R | CAN Replay Attack |

### Data Representation

Instead of handcrafted features, raw packet traffic is transformed into image representations through a preprocessing pipeline before being used for deep learning.

An additional **AVTP Intrusion Dataset** is also included to evaluate model generalization and transfer learning capabilities.

---

# Proposed Preprocessing Pipeline

The following figure illustrates the preprocessing pipeline used to transform raw packet traffic into image representations suitable for deep learning.

<p align="center">
    <img src="preprocessing%20pipeline.jpg" width="100%">
</p>

The preprocessing stages include:

- Raw packet acquisition
- Packet parsing
- Packet standardization
- Packet-byte matrix construction
- Sliding window generation
- Data normalization
- Discrete Wavelet Transform (DWT)
- RGB image generation

This representation enables convolutional neural networks to learn spatial characteristics from network traffic while significantly reducing redundant information.

---

# Proposed Model — DPDNet-Lite

The primary contribution of this research is **DPDNet-Lite**, a lightweight convolutional neural network designed specifically for intrusion detection in modern in-vehicle networks.

<p align="center">
    <img src="structure%20DPDNet-Lite.jpg" width="100%">
</p>

DPDNet-Lite combines several lightweight convolution techniques to reduce computational cost while maintaining competitive detection performance.

The architecture is designed to:

- Learn spatial traffic representations extracted from DWT images.
- Reduce model complexity through lightweight convolution blocks.
- Capture directional packet features efficiently.
- Support deployment on resource-constrained edge devices.
- Maintain high detection performance under Federated Learning.

---

# Experimental Scenarios

This repository contains experiments covering several research stages:

- Centralized Learning
- Federated Learning (IID)
- Federated Learning (non-IID)
- Wavelet preprocessing comparison
- Model architecture comparison
- Cross-dataset evaluation
- Live IDS demonstration

---

# Repository Contents

This repository includes:

- Proposed **DPDNet-Lite** implementation.
- Reference implementation of **MR-TCN**.
- Reference implementation of **Swin Transformer IDS**.
- Wavelet preprocessing experiments.
- Federated Learning experiments.
- Cross-dataset evaluation.
- Live IDS dashboard.
- Supporting notebooks and utilities.

---

# Repository Structure

```text
.
├── tow_ids/                     # Proposed DPDNet-Lite implementation
├── mrtcn_ids/                   # MR-TCN baseline
├── swin_ids/                    # Swin Transformer baseline
├── WaveletPerbandingan/         # Wavelet preprocessing studies
├── FLwaveletperbandingan/       # Federated Learning experiments
├── ReplikasiNewModel(gambar)/   # Architecture illustrations
├── vehicleidsdashboard/         # React + FastAPI dashboard
├── README.md
```

---

# Research Highlights

- Lightweight IDS architecture (DPDNet-Lite)
- Automotive Ethernet intrusion detection
- Image-based network traffic representation
- Discrete Wavelet Transform preprocessing
- Centralized Learning evaluation
- Federated Learning evaluation
- IID and non-IID experiments
- Cross-dataset validation using AVTP Intrusion Dataset
- Live IDS dashboard for inference visualization

---

# Contact

If you have any questions, suggestions, collaboration opportunities, or would like to discuss this research, please feel free to contact me.

**Maidi Ridani**

- GitHub: https://github.com/MaidiRidani
- Email: dani.maidiridani@gmail.com

> **Note:** If you contact me via email regarding this repository, please use **"GitHub Q&A"** as the email subject so that your message can be identified and prioritized accordingly.
