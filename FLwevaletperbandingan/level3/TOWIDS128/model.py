import tensorflow as tf
from tensorflow.keras import layers, models


def build_model():

    ukuran = 16

    inputs = layers.Input(shape=(ukuran, ukuran, 3))

    # =========================================================
    # Block A
    # =========================================================

    x = layers.SeparableConv2D(
        32,
        (3,3),
        padding="same",
        use_bias=False
    )(inputs)

    x = layers.ReLU()(x)

    x = layers.SeparableConv2D(
        32,
        (3,3),
        padding="same",
        use_bias=False
    )(x)

    x = layers.ReLU()(x)

    x = layers.BatchNormalization()(x)

    x = layers.MaxPooling2D((2,2))(x)

    # =========================================================
    # Block B (Residual)
    # =========================================================

    shortcut = layers.Conv2D(
        64,
        (1,1),
        padding="same",
        use_bias=False
    )(x)

    shortcut = layers.BatchNormalization()(shortcut)

    y = layers.SeparableConv2D(
        64,
        (3,3),
        padding="same",
        use_bias=False
    )(x)

    y = layers.ReLU()(y)

    y = layers.SeparableConv2D(
        64,
        (3,3),
        padding="same",
        use_bias=False
    )(y)

    y = layers.ReLU()(y)

    y = layers.BatchNormalization()(y)

    x = layers.Add()([y, shortcut])

    x = layers.ReLU()(x)

    # =========================================================
    # Block C
    # =========================================================

    x = layers.SeparableConv2D(
        128,
        (3,3),
        padding="same",
        use_bias=False
    )(x)

    x = layers.ReLU()(x)

    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dense(
        512,
        activation="relu"
    )(x)

    x = layers.Dense(
        256,
        activation="relu"
    )(x)

    x = layers.Dropout(0.5)(x)

    outputs = layers.Dense(
        1,
        activation="sigmoid"
    )(x)

    # =========================================================
    # BUILD MODEL
    # =========================================================

    model = models.Model(
        inputs=inputs,
        outputs=outputs
    )

    # =========================================================
    # COMPILE
    # =========================================================

    model.compile(

        optimizer="adam",

        loss="binary_crossentropy",

        metrics=[
            "accuracy",

            tf.keras.metrics.Precision(
                name="precision"
            ),

            tf.keras.metrics.Recall(
                name="recall"
            )
        ]
    )

    return model