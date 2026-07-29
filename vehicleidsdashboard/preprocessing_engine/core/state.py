from dataclasses import dataclass, field


@dataclass
class DatasetInfo:
    """
    Informasi dataset yang sedang aktif.
    """

    name: str | None = None

    pcap_path: str | None = None

    label_path: str | None = None

    total_packets: int = 0

    labels: list = field(default_factory=list)

    packets = None

    packet_index: dict = field(default_factory=dict)

    packet_label: dict = field(default_factory=dict)


@dataclass
class Configuration:
    """
    Konfigurasi preprocessing.
    """

    window_size: int = 128

    dwt_level: int = 2


@dataclass
class EngineState:

    dataset: DatasetInfo = field(default_factory=DatasetInfo)

    configuration: Configuration = field(default_factory=Configuration)

    window_configurations: list = field(default_factory=list)

    prepared_windows: list = field(default_factory=list)

    preprocessed_images: list = field(default_factory=list)

    status: str = "Idle"