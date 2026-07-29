import tensorflow as tf
from tensorflow.keras import layers, models

def build_model():
    def composite_conv(x, filters, kernel_size, groups=1):

        x = layers.Conv2D(
            filters,
            kernel_size,
            padding="same",
            groups=groups
        )(x)

        x = layers.BatchNormalization()(x)

        x = layers.ReLU()(x)

        return x


    def factorized_conv(x, f1, f2):

        x = composite_conv(x, f1, (1,3))

        x = composite_conv(x, f2, (3,1))

        return x

    def DGC_block(x):

        # branch 1
        b1 = composite_conv(x, 16, (1,3))
        b2 = composite_conv(x, 16, (3,1))

        concat = layers.Concatenate()([b1, b2])

        conv = composite_conv(concat, 32, (1,1))

        pool = layers.MaxPooling2D((2,2))(conv)

        g1 = composite_conv(pool, 64, (1,3), groups=4)


        # residual branch
        res = composite_conv(x, 32, (1,1))

        res = layers.MaxPooling2D((2,2))(res)

        g2 = composite_conv(res, 64, (3,1), groups=4)


        out = layers.Add()([g1, g2])

        return out


    input_layer = layers.Input(shape=(64,64,3))

    x_factor = factorized_conv(input_layer, 32, 16)

    x_max= layers.MaxPooling2D((2,2))(x_factor)

    x_dgc1 = DGC_block(x_max)

    x_dgc2 = DGC_block(x_dgc1)

    x_comconv = composite_conv(x_dgc2, 32, (1,1))

    del x_factor, x_max, x_dgc1, x_dgc2

    x_average = layers.GlobalAveragePooling2D()(x_comconv)

    x_flatten = layers.Flatten()(x_average)

    x_fcon = layers.Dense(128, activation="relu")(x_flatten)

    output_layer = layers.Dense(1, activation="sigmoid")(x_fcon)

    del x_comconv, x_average, x_flatten, x_fcon

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


