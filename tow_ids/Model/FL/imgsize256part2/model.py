import tensorflow as tf
from tensorflow.keras import layers, models

def conv_block_a(inputs):
    x = layers.SeparableConv2D(256, (3,3), padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    x = layers.SeparableConv2D(256, (3,3), padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    x = layers.MaxPooling2D((2,2))(x)

    return x


def conv_block_b(x):
    shortcut = x

    # residual mapping
    res = layers.SeparableConv2D(256, (3,3), padding="same")(x)
    res = layers.BatchNormalization()(res)
    res = layers.ReLU()(res)

    res = layers.SeparableConv2D(256, (3,3), padding="same")(res)
    res = layers.BatchNormalization()(res)

    x = layers.Add()([shortcut, res])
    x = layers.ReLU()(x)

    return x


def conv_block_c(x):
    x = layers.SeparableConv2D(512, (3,3), padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    x = layers.GlobalAveragePooling2D()(x)

    return x


def build_model(input_shape=(128, 128, 3)):
    inputs = layers.Input(shape=input_shape)

    # ===== Block A =====
    x = conv_block_a(inputs)

    # ===== Block B (5x) =====
    for _ in range(5):
        x = conv_block_b(x)

    # ===== Block C =====
    x = conv_block_c(x)

    # ===== Dense Head =====
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dropout(0.5)(x)

    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = models.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall")
        ]
    )

    return model