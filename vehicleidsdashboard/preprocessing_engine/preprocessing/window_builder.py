import numpy as np


class WindowBuilder:
    """
    Membangun satu window berdasarkan
    packet yang dipilih user.
    """
    # =====================================================
    # RESIZE SINGLE PACKET
    # =====================================================

    def resize_packet(
        self,
        packet,
        packet_size
    ):

        if len(packet) < packet_size:

            packet = packet + bytes(packet_size - len(packet))

        else:

            packet = packet[:packet_size]

        return np.frombuffer(
            packet,
            dtype=np.uint8
        )



    def build_window(
        self,
        packets,
        packet_number,
        position,
        window_size
    ):

        # ----------------------------------------
        # Validasi Position
        # ----------------------------------------

        if position < 1 or position > window_size:
            raise ValueError(
                f"Position harus berada pada rentang 1-{window_size}"
            )

        # ----------------------------------------
        # Hitung packet awal
        # ----------------------------------------

        start_packet = packet_number - (position - 1)

        # ----------------------------------------
        # Hitung packet akhir
        # ----------------------------------------

        end_packet = start_packet + window_size - 1

        # ----------------------------------------
        # Validasi awal dataset
        # ----------------------------------------

        if start_packet < 1:
            raise ValueError(
                "Window melewati awal dataset."
            )

        # ----------------------------------------
        # Validasi akhir dataset
        # ----------------------------------------

        if end_packet > len(packets):
            raise ValueError(
                "Window melewati akhir dataset."
            )

        # ----------------------------------------
        # Ambil packet
        # ----------------------------------------

        selected_packets = packets[
            start_packet - 1 : end_packet
        ]

        if len(selected_packets) != window_size:
            raise RuntimeError(
                f"Jumlah packet tidak valid. "
                f"Expected {window_size}, "
                f"Got {len(selected_packets)}"
            )

        window = []

        for packet in selected_packets:

            resized_packet = self.resize_packet(

                packet,

                window_size

            )

            window.append(
                resized_packet
            )

        window = np.array(window)
        if len(window) != window_size:
            raise RuntimeError(
                f"Jumlah packet hasil resize tidak valid. "
                f"Expected {window_size}, "
                f"Got {len(window)}"
            )

        # ----------------------------------------
        # Validasi ukuran
        # ----------------------------------------

        if window.shape != (window_size, window_size):
            raise RuntimeError(
                f"Window tidak valid. Shape = {window.shape}"
            )

        return window