import numpy as np

from dataset import (
    load_validation_data,
    load_validation_data21
)

x23, y23 = load_validation_data()
x21, y21 = load_validation_data21()


def print_channel_statistics(name, x):

    print(f"\n===== {name} PER CHANNEL =====")

    for channel in range(x.shape[-1]):

        values = x[..., channel]

        print(
            f"Channel {channel} | "
            f"Min: {values.min():.6f} | "
            f"Max: {values.max():.6f} | "
            f"Mean: {values.mean():.6f} | "
            f"Std: {values.std():.6f}"
        )


print_channel_statistics(
    "DATASET23",
    x23
)

print_channel_statistics(
    "DATASET21",
    x21
)