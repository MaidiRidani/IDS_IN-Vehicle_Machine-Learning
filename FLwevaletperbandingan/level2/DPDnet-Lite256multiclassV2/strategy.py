# ==========================================================
# IMPORT
# ==========================================================

import numpy as np

from dataset import load_client_manifest

# ==========================================================
# CLASSIFIER LAYER
# ==========================================================

CLASSIFIER_KERNEL = 65
CLASSIFIER_BIAS = 66


# ==========================================================
# AGGREGATE CLASSIFIER KERNEL
# ==========================================================

def aggregate_classifier_kernel(
    client_weights,
    client_ids,
):
    """
    Agregasi kernel classifier berdasarkan manifest.

    Shape:
        (64, 8)

    Setiap neuron output hanya menerima
    update dari client yang memiliki class tersebut.
    """

    kernel_shape = client_weights[0][CLASSIFIER_KERNEL].shape

    aggregated = np.zeros_like(
        client_weights[0][CLASSIFIER_KERNEL]
    )

    client_manifests = {

        cid: load_client_manifest(cid)

        for cid in client_ids

    }

    num_classes = kernel_shape[1]

    print()

    print("=" * 60)
    print("CLASSIFIER KERNEL AGGREGATION")
    print("=" * 60)

    for cls in range(num_classes):

        contributors = []

        for idx, client_id in enumerate(client_ids):

            if cls in client_manifests[client_id]:

                contributors.append(idx)

        if len(contributors) == 0:

            raise RuntimeError(
                f"Tidak ada client yang memiliki class {cls}"
            )

        column = np.zeros_like(
            aggregated[:, cls]
        )

        for idx in contributors:

            column += (

                client_weights[idx][CLASSIFIER_KERNEL][:, cls]

                / len(contributors)

            )

        aggregated[:, cls] = column

        print(
            f"Class {cls} <- "
            f"{[client_ids[i] for i in contributors]}"
        )

    return aggregated


# ==========================================================
# AGGREGATE CLASSIFIER BIAS
# ==========================================================

def aggregate_classifier_bias(
    client_weights,
    client_ids,
):
    """
    Agregasi bias classifier berdasarkan manifest.

    Shape:
        (8,)
    """

    bias_shape = client_weights[0][CLASSIFIER_BIAS].shape

    aggregated = np.zeros_like(
        client_weights[0][CLASSIFIER_BIAS]
    )

    client_manifests = {

        cid: load_client_manifest(cid)

        for cid in client_ids

    }

    num_classes = bias_shape[0]

    print()

    print("=" * 60)
    print("CLASSIFIER BIAS AGGREGATION")
    print("=" * 60)

    for cls in range(num_classes):

        contributors = []

        for idx, client_id in enumerate(client_ids):

            if cls in client_manifests[client_id]:

                contributors.append(idx)

        if len(contributors) == 0:

            raise RuntimeError(
                f"Tidak ada client yang memiliki class {cls}"
            )

        value = 0.0

        for idx in contributors:

            value += (

                client_weights[idx][CLASSIFIER_BIAS][cls]

                / len(contributors)

            )

        aggregated[cls] = value

        print(
            f"Class {cls} <- "
            f"{[client_ids[i] for i in contributors]}"
        )

    return aggregated


# ==========================================================
# FEDAVG + MANIFEST AGGREGATION
# ==========================================================

def fedavg_aggregate(
    client_weights,
    client_sizes,
    client_ids,
):
    """
    Backbone:
        FedAvg berbobot jumlah data.

    Classifier:
        Manifest-aware aggregation.
    """

    # ======================================================
    # VALIDASI INPUT
    # ======================================================

    if len(client_weights) == 0:
        raise ValueError(
            "client_weights kosong."
        )

    if len(client_weights) != len(client_sizes):
        raise ValueError(
            "Jumlah client_weights dan client_sizes berbeda."
        )

    if len(client_weights) != len(client_ids):
        raise ValueError(
            "Jumlah client_weights dan client_ids berbeda."
        )

    # ======================================================
    # VALIDASI MODEL
    # ======================================================

    num_layers = len(client_weights[0])

    for client_idx, weights in enumerate(client_weights):

        if len(weights) != num_layers:

            raise ValueError(

                f"Jumlah layer Client "

                f"{client_ids[client_idx]} berbeda."

            )

        for layer_idx in range(num_layers):

            expected = client_weights[0][layer_idx].shape

            current = weights[layer_idx].shape

            if expected != current:

                raise ValueError(

                    f"Layer {layer_idx} "

                    f"shape mismatch "

                    f"(expected={expected}, "

                    f"got={current})"

                )

    # ======================================================
    # FEDAVG
    # ======================================================

    total_size = np.sum(client_sizes)

    if total_size == 0:

        raise ValueError(
            "Total sample = 0."
        )

    aggregated_weights = []

    print()

    print("=" * 60)
    print("FEDERATED AGGREGATION")
    print("=" * 60)

    print("Client IDs   :", client_ids)
    print("Client Sizes :", client_sizes)
    print("Total Sample :", total_size)

    # ======================================================
    # BACKBONE
    # ======================================================

    for layer_idx in range(CLASSIFIER_KERNEL):

        layer = np.zeros_like(
            client_weights[0][layer_idx]
        )

        for weights, size in zip(
            client_weights,
            client_sizes
        ):

            layer += (

                weights[layer_idx]

                * (size / total_size)

            )

        aggregated_weights.append(layer)

    print()

    print(
        "[Aggregation] Backbone -> FedAvg"
    )

    # ======================================================
    # CLASSIFIER
    # ======================================================

    aggregated_weights.append(

        aggregate_classifier_kernel(

            client_weights,

            client_ids,

        )

    )

    aggregated_weights.append(

        aggregate_classifier_bias(

            client_weights,

            client_ids,

        )

    )

    # ======================================================
    # SANITY CHECK
    # ======================================================

    assert len(aggregated_weights) == num_layers

    print()

    print("=" * 60)
    print("AGGREGATION SUMMARY")
    print("=" * 60)

    print("Backbone          : FedAvg")
    print("Classifier Kernel : Manifest-aware")
    print("Classifier Bias   : Manifest-aware")

    print()

    print("Aggregation selesai.")

    return aggregated_weights