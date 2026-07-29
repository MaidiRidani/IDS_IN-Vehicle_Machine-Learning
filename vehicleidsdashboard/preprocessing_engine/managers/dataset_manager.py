import os

import pandas as pd
import numpy as np
from scapy.all import rdpcap
from scapy.all import raw

from config import DATASETS


class DatasetManager:

    def __init__(self):

        self.datasets = DATASETS

    def get_available_datasets(self):

        return self.datasets

    # =====================================================
    # EXTRACT PACKET (TIDAK DIUBAH DARI NOTEBOOK)
    # =====================================================

    def extract_packets(self, pcap_path):

        packets = rdpcap(pcap_path)

        data = []

        for pkt in packets:

            pkt_bytes = raw(pkt)

            data.append(pkt_bytes)

        return data

    # =====================================================
    # LOAD CACHE ATAU EXTRACT
    # =====================================================

    def load_packets(
        self,
        dataset
    ):

        cache_path = dataset["packet_cache"]

        # jika cache sudah ada
        if os.path.exists(cache_path):

            print("Packet cache found.")
            print("Loading packets...")

            cache = np.load(cache_path)

            return cache["packets"]

        # jika cache belum ada
        print("Packet cache not found.")
        print("Extracting packets...")

        packets = self.extract_packets(
            dataset["pcap_path"]
        )
        print("Saving packet cache...")

        np.savez_compressed(
            cache_path,
            packets=packets
        )

        print("Packet cache saved.")

        return packets

    # =====================================================
    # BUILD PACKET INDEX
    # =====================================================

    def build_packet_index(self, packet_labels):

        packet_index = {}

        for packet_number, label in enumerate(packet_labels, start=1):

            if label not in packet_index:
                packet_index[label] = []

            packet_index[label].append(packet_number)

        return packet_index


    # =====================================================
    # BUILD PACKET LABEL
    # =====================================================

    def build_packet_label(
        self,
        packet_labels
    ):

        packet_label = {}

        for packet_number, label in enumerate(packet_labels, start=1):

            packet_label[packet_number] = label

        return packet_label



    # =====================================================
    # DETERMINE WINDOW LABEL
    # =====================================================

    def determine_window_label(
        self,
        start_packet,
        end_packet,
        packet_label
    ):

        attack_labels = []

        trigger_packet = None

        window_label = "Normal"

        for packet_number in range(start_packet, end_packet + 1):

            label = packet_label[packet_number]

            if label != "Normal":

                if trigger_packet is None:

                    trigger_packet = packet_number

                    window_label = label

                if label not in attack_labels:

                    attack_labels.append(label)

        return {

            "window_label": window_label,

            "trigger_packet": trigger_packet,

            "attack_labels": attack_labels

        }

    # =====================================================
    # LOAD DATASET
    # =====================================================

    def load_dataset(
        self,
        name
    ):

        if name not in self.datasets:
            raise ValueError(f"Dataset '{name}' tidak ditemukan.")

        dataset = self.datasets[name]

        labels_df = pd.read_csv(
            dataset["label_path"],
            header=None
        )

        label_column = dataset["label_column"]

        packet_labels = labels_df.iloc[:, label_column].tolist()

        available_labels = sorted(
            labels_df.iloc[:, label_column].unique().tolist()
        )

        packets = self.load_packets(
            dataset,
        )

        packet_index = self.build_packet_index(packet_labels)

        packet_label = self.build_packet_label(packet_labels)
        return {
            
            "name": dataset["display_name"],

            "pcap_path": dataset["pcap_path"],

            "label_path": dataset["label_path"],

            "total_packets": len(packet_labels),

            "labels": available_labels,

            "packets": packets,

            "packet_index": packet_index,

            "packet_label": packet_label,

        }