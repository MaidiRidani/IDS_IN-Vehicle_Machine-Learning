from pyexpat import model

import tensorflow as tf
from tensorflow.keras import layers, models
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dropout, MaxPooling1D, Flatten, Dense

def build_model():
    def build_mr_tcn(input_shape=(256, 256), dropout_rate=0.55):
        model = Sequential()

        # Conv1D #1
        model.add(Conv1D(
            filters=64,
            kernel_size=3,
            strides=1,
            dilation_rate=1,
            padding="same",
            activation="relu",
            input_shape=input_shape
        ))
        model.add(Dropout(dropout_rate))

        # Conv1D #2
        model.add(Conv1D(
            filters=64,
            kernel_size=3,
            strides=1,
            dilation_rate=2,
            padding="same",
            activation="relu"
        ))
        model.add(Dropout(dropout_rate))

        # Conv1D #3
        model.add(Conv1D(
            filters=64,
            kernel_size=3,
            strides=1,
            dilation_rate=4,
            padding="same",
            activation="relu"
        ))
        model.add(Dropout(dropout_rate))

        # MaxPooling
        model.add(MaxPooling1D(pool_size=8, strides=8))

        # Flatten
        model.add(Flatten())

        # Dropout
        model.add(Dropout(dropout_rate))

        # Linear → Sigmoid
        model.add(Dense(1, activation="sigmoid"))
        
        return model

    model = build_mr_tcn()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall")]
)
    return model




