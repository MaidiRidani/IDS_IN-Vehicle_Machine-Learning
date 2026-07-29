from core.engine import PreprocessingEngine


def main():

    engine = PreprocessingEngine()

    engine.load_dataset("tow_ids_test")

    print("\n===== DATASET =====")

    print(f"Name          : {engine.state.dataset.name}")
    print(f"Total Packet  : {engine.state.dataset.total_packets}")
    print(f"Labels        : {engine.state.dataset.labels}")
    print(f"Total Raw Packet : {len(engine.state.dataset.packets)}")

    print(
        f"First Packet Length : {len(engine.state.dataset.packets[0])} bytes"
    )

    print(f"Index Label   : {list(engine.state.dataset.packet_index.keys())}")

    print(
        f"Normal Packet : {len(engine.state.dataset.packet_index['Normal'])}"
    )
    print(f"Status        : {engine.state.status}")

    print("\n===== WINDOW CONFIGURATION =====")

    engine.add_window_configuration(
        packet_number=500,
        position=100
    )

    engine.add_window_configuration(
        packet_number=1200,
        position=50
    )

    print(engine.state.window_configurations)
    print("\n===== PREPROCESSING =====")

    outputs = engine.run_preprocessing()

    print(f"Total Output : {len(outputs)}")

    for i, output in enumerate(outputs, start=1):

        print(f"Output {i}")

        print(f"Shape : {output.shape}")

        print(f"DType : {output.dtype}")

        print(f"Min   : {output.min()}")

        print(f"Max   : {output.max()}")

        print()

if __name__ == "__main__":
    main()