from core.state import EngineState
from managers.dataset_manager import DatasetManager
from managers.model_manager import ModelManager
from preprocessing.window_builder import WindowBuilder
from preprocessing.normalizer import Normalizer
from preprocessing.dwt_processor import DWTProcessor
import cv2
import numpy as np
import os
import glob
import random


class PreprocessingEngine:

    def __init__(self):

        self.state = EngineState()

        self.dataset_manager = DatasetManager()
        self.model_manager = ModelManager()

        self.window_builder = WindowBuilder()

        self.normalizer = Normalizer()

        self.dwt_processor = DWTProcessor()

        print("===================================")
        print(" Preprocessing Engine Initialized")
        print("===================================")


    # =====================================================
    # CONFIGURATION
    # =====================================================

    def set_configuration(

        self,

        window_size,

        dwt_level,

    ):

        self.state.configuration.window_size = window_size

        self.state.configuration.dwt_level = dwt_level

        print("\n========== ENGINE CONFIGURATION ==========")

        print(f"Window Size : {self.state.configuration.window_size}")

        print(f"DWT Level   : {self.state.configuration.dwt_level}")

        print("==========================================\n")
        


    def get_configuration(self):

        return {

            "window_size":
                self.state.configuration.window_size,

            "dwt_level":
                self.state.configuration.dwt_level,

        }



    # =====================================================
    # DATASET
    # =====================================================

    def load_dataset(self, name):

        info = self.dataset_manager.load_dataset(

            name,

        )

        self.state.dataset.name = info["name"]
        self.state.dataset.pcap_path = info["pcap_path"]
        self.state.dataset.label_path = info["label_path"]
        self.state.dataset.total_packets = info["total_packets"]
        self.state.dataset.labels = info["labels"]
        self.state.dataset.packets = info["packets"]
        self.state.dataset.packet_index = info["packet_index"]
        self.state.dataset.packet_label = info["packet_label"]

        self.state.status = "Ready"

    # =====================================================
    # WINDOW CONFIGURATION
    # =====================================================

    def add_window_configuration(
        self,
        packet_number,
        position
    ):

        if self.state.status != "Ready":

            raise ValueError(
                "Dataset belum dimuat."
            )

        # ==========================================
        # Validasi window masih berada dalam dataset
        # ==========================================

        start_packet = packet_number - (position - 1)

        end_packet = (
            start_packet
            + self.state.configuration.window_size
            - 1
        )

        if start_packet < 1 or end_packet > self.state.dataset.total_packets:

            raise ValueError(
                "Posisi tersebut tidak dapat membentuk window."
            )

        # ==========================================
        # Update jika packet sudah ada
        # ==========================================

        for config in self.state.window_configurations:

            if config["packet_number"] == packet_number:

                config["position"] = position

                config["attack_type"] = self.state.dataset.packet_label[
                    packet_number
                ]

                return

        # ==========================================
        # Tambah konfigurasi baru
        # ==========================================

        self.state.window_configurations.append({

            "packet_number": packet_number,

            "attack_type": self.state.dataset.packet_label[
                packet_number
            ],

            "position": position

        })

    def clear_window_configurations(self):

        self.state.window_configurations.clear()



    def generate_random_configurations(
        self,
        count
    ):

        if self.state.status != "Ready":

            raise ValueError(
                "Dataset belum dimuat."
            )

        self.clear_window_configurations()

        packet_index = self.state.dataset.packet_index

        labels = [

            "Normal",

            "C_D",

            "C_R",

            "F_I",

            "M_F",

            "P_I",

        ]

        selected_packets = set()

        while len(self.state.window_configurations) < count:

            label = random.choice(labels)

            packet_number = random.choice(
                packet_index[label]
            )

            if packet_number in selected_packets:

                continue

            position = random.randint(

                1,

                self.state.configuration.window_size

            )

            try:

                self.add_window_configuration(

                    packet_number=packet_number,

                    position=position

                )

                selected_packets.add(packet_number)

            except ValueError:

                continue

        return self.get_window_configurations()
    # =====================================================
    # BUILD SINGLE WINDOW
    # =====================================================

    def build_window(
        self,
        packet_number,
        position
    ):

        return self.window_builder.build_window(

            packets=self.state.dataset.packets,

            packet_number=packet_number,

            position=position,

            window_size=self.state.configuration.window_size

        )
    


# =====================================================
# PREPARE WINDOWS
# =====================================================

    def prepare_windows(self):

        if self.state.status != "Ready":

            raise ValueError(
                "Dataset belum dimuat."
            )

        if len(self.state.window_configurations) == 0:

            raise ValueError(
                "Belum ada konfigurasi window."
            )

        self.state.prepared_windows.clear()
        self.state.preprocessed_images.clear()
        os.makedirs(
            "cache/images",
            exist_ok=True
        )

        for file in glob.glob(
            "cache/images/*.png"
        ):

            os.remove(file)

        for config in self.state.window_configurations:

            window = self.build_window(

                packet_number=config["packet_number"],

                position=config["position"]

            )
            start_packet = (
                config["packet_number"]
                - (config["position"] - 1)
            )

            end_packet = (
                start_packet
                + self.state.configuration.window_size
                - 1
            )

            window_info = self.dataset_manager.determine_window_label(

                start_packet=start_packet,

                end_packet=end_packet,

                packet_label=self.state.dataset.packet_label

            )
            

            self.state.prepared_windows.append({

                "packet_number": config["packet_number"],

                "selected_label": self.state.dataset.packet_label[
                    config["packet_number"]
                ],

                "window_label": window_info["window_label"],

                "trigger_packet": window_info["trigger_packet"],

                "attack_labels": window_info["attack_labels"],

                "position": config["position"],

                "window": window

            })

        return len(self.state.prepared_windows)




    # =====================================================
    # RUN PREPROCESSING
    # =====================================================

    def run_preprocessing(self):

        if self.state.status != "Ready":

            raise ValueError(
                "Dataset belum dimuat."
            )

        if len(self.state.prepared_windows) == 0:

            raise ValueError(
                "Belum ada prepared window."
            )

        self.state.preprocessed_images.clear()

        for item in self.state.prepared_windows:

            window = item["window"]

            window = self.normalizer.normalize(window)

            image = self.dwt_processor.transform(

                window,

                level=self.state.configuration.dwt_level

            )

            self.dwt_processor.save_rgb_image(

                image,

                len(self.state.preprocessed_images)

            )

            self.state.preprocessed_images.append({

                "packet_number": item["packet_number"],

                "selected_label": item["selected_label"],

                "window_label": item["window_label"],

                "trigger_packet": item["trigger_packet"],

                "attack_labels": item["attack_labels"],

                "position": item["position"],

                "image": image

            })

        return len(self.state.preprocessed_images)
    

# =====================================================
# PUBLIC API
# =====================================================
    def get_available_datasets(self):

        datasets = []

        for key, value in self.dataset_manager.get_available_datasets().items():

            datasets.append({

                "id": key,

                "name": value["display_name"]

            })

        return datasets
    
    def get_dataset_info(self):

        if self.state.status != "Ready":

            raise ValueError(
                "Dataset belum dimuat."
            )

        return {

            "name": self.state.dataset.name,

            "total_packets": self.state.dataset.total_packets,

            "labels": self.state.dataset.labels

        }
    
    def get_labels(self):

        if self.state.status != "Ready":

            raise ValueError(
                "Dataset belum dimuat."
            )

        return self.state.dataset.labels
    
    def get_packets_by_label(
        self,
        label
    ):

        if self.state.status != "Ready":

            raise ValueError(
                "Dataset belum dimuat."
            )
        if label not in self.state.dataset.packet_index:

            raise ValueError(
                f"Label '{label}' tidak ditemukan."
            )

        return self.state.dataset.packet_index[label]
    
    def get_window_configurations(self):

        return self.state.window_configurations
    
    def remove_window_configuration(
        self,
        packet_number
    ):

        for index, config in enumerate(
            self.state.window_configurations
        ):

            if config["packet_number"] == packet_number:

                del self.state.window_configurations[index]

                return

        raise ValueError(
            "Konfigurasi tidak ditemukan."
        )
    
    def clear_window_configurations(self):

        self.state.window_configurations.clear()

    def get_prepared_window_count(self):

        return len(
            self.state.prepared_windows
        )
    
    def get_prepared_windows(self):

        return self.state.prepared_windows
    
    def get_prepared_window_info(self):

        info = []

        for item in self.state.prepared_windows:

            info.append({

                "packet_number": item["packet_number"],

                "selected_label": item["selected_label"],

                "window_label": item["window_label"],

                "trigger_packet": item["trigger_packet"],

                "attack_labels": item["attack_labels"],

                "position": item["position"],

                "shape": list(item["window"].shape)

            })

        return info
    
    def get_preprocessed_image_count(self):

        return len(
            self.state.preprocessed_images
        )
    
    def get_preprocessed_image_info(self):

        info = []

        for item in self.state.preprocessed_images:

            info.append({

                "packet_number": item["packet_number"],

                "selected_label": item["selected_label"],

                "window_label": item["window_label"],

                "trigger_packet": item["trigger_packet"],

                "attack_labels": item["attack_labels"],

                "position": item["position"],

                "shape": list(item["image"].shape)

            })

        return info
    def get_preprocessed_data(self):

        return self.state.preprocessed_images


    def get_preprocessed_image(
        self,
        index
    ):

        if index < 0 or index >= len(self.state.preprocessed_images):

            raise ValueError(
                "Image tidak ditemukan."
            )

        image = self.state.preprocessed_images[index]["image"]

        image = cv2.normalize(

            image,

            None,

            0,

            255,

            cv2.NORM_MINMAX

        )

        image = image.astype(np.uint8)

        return image
    

    # =====================================================
    # MODEL
    # =====================================================

    def get_available_models(self):

        return self.model_manager.get_available_models()
    


