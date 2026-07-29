import tensorflow as tf
from tensorflow.keras import layers, models

def build_model():
    ukuran = 16

    def composite_conv(x, filters, kernel_size):
        x = layers.Conv2D(
            filters,
            kernel_size,
            padding="same",
            use_bias=False
        )(x)

        x = layers.BatchNormalization()(x)

        x = layers.ReLU()(x)

        return x


    def SE_block(x, ratio=16):
        channels = x.shape[-1]

        se = layers.GlobalAveragePooling2D()(x)

        se = layers.Dense(
            max(channels // ratio, 4),
            activation="relu"
        )(se)

        se = layers.Dense(
            channels,
            activation="sigmoid"
        )(se)

        se = layers.Reshape((1, 1, channels))(se)

        out = layers.Multiply()([x, se])

        return out


    def DPDB_block(x, filters, pool=True):
        shortcut = x

        h = composite_conv(x, filters // 2, (1, 3))

        v = composite_conv(x, filters // 2, (3, 1))

        concat = layers.Concatenate()([h, v])

        fusion = composite_conv(concat, filters, (1, 1))

        fusion = SE_block(fusion)

        if pool:
            fusion = layers.MaxPooling2D((2, 2))(fusion)

        shortcut = layers.Conv2D(
            filters,
            (1, 1),
            padding="same",
            use_bias=False
        )(shortcut)

        shortcut = layers.BatchNormalization()(shortcut)

        if pool:
            shortcut = layers.MaxPooling2D((2, 2))(shortcut)

        out = layers.Add()([fusion, shortcut])

        out = layers.ReLU()(out)

        return out


    input_layer = layers.Input(shape=(ukuran, ukuran, 3))

    x = composite_conv(input_layer, 16, (1, 3))

    x = composite_conv(x, 16, (3, 1))

    x = DPDB_block(x, 32, pool=True)

    x = DPDB_block(x, 64, pool=False)

    x = composite_conv(x, 48, (1, 1))

    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dense(
        64,
        activation="relu"
    )(x)

    x = layers.Dropout(0.5)(x)

    output_layer = layers.Dense(
        1,
        activation="sigmoid"
    )(x)
    model = models.Model(
        inputs=input_layer,
        outputs=output_layer
    )

    model.compile(

        optimizer="adam",

        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall")]
    )

    return model

