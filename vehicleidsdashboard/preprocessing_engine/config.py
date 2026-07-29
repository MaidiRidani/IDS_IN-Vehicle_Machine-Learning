# =====================================================
# DATASET CONFIGURATION
# =====================================================

BASE_PATH = "/home/dani/Documents/tugas akhir/TugasAkhir/DataTugasAkhirku2026/dataTOWIDSmentah/"
BASE_PATH_CACHE = "/home/dani/Documents/tugas akhir/TugasAkhir/Website/vehicleids/preprocessing_engine/cache/"


DATASETS = {

    "tow_ids_test": {

        "display_name": "TOW-IDS Test (6 Classes)",

        "pcap_path":
            BASE_PATH + "Automotive_Ethernet_with_Attack_original_10_17_20_04_test.pcap",

        "label_path":
            BASE_PATH + "y_test.csv",

        "label_column": 2,

        # lokasi cache packet hasil ekstraksi
        "packet_cache":
            BASE_PATH_CACHE + "tow_ids_test_packets.npz"

    },

    "tow_ids_train": {

        "display_name": "TOW-IDS Train (6 Classes)",

        "pcap_path":
            BASE_PATH + "Automotive_Ethernet_with_Attack_original_10_17_19_50_training.pcap",

        "label_path":
            BASE_PATH + "y_train.csv",

        "label_column": 2,

        # lokasi cache packet hasil ekstraksi
        "packet_cache":
            BASE_PATH_CACHE + "tow_ids_train_packets.npz"

    }


}





# =====================================================
# MODEL CONFIGURATION
# =====================================================

MODELS = {

    "dpdnet_lite_256": {

        "display_name": "DPDNet-Lite 256",

        "framework": "TensorFlow",

        "window_size": 256,

        "dwt_level": 2,

        "input_size": 64,

        "classes": 6,

        "file_size": "24.5 MB"

    },

    "dpdnet_lite_128": {

        "display_name": "DPDNet-Lite 128",

        "framework": "TensorFlow",

        "window_size": 128,

        "dwt_level": 1,

        "input_size": 64,

        "classes": 6,

        "file_size": "18.3 MB"

    }

}



