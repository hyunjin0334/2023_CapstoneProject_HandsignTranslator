import cv2
import numpy as np
import os
import mediapipe as mp
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy
from tensorflow.keras.activations import gelu

DATA_PATH = os.path.join('Data')
# Action
actions = np.array(['angry', 'beautiful', 'believe', 'busy', 'cold',
                    'cool', 'crazy', 'cute', 'divide', 'familiar',
                    'fine', 'full', 'give', 'go', 'hello',
                    'help', 'hit', 'hot', 'hug', 'hungry',
                    'imagine', 'lie', 'like', 'pretty', 'receive',
                    'regret', 'respect', 'right', 'run', 'scary',
                    'sick', 'sleepy', 'sorry', 'thankyou', 'tiresome',
                    'visible', 'walk', 'wrong'])

no_sequences = 200
sequence_length = 40

label_map = {label: num for num, label in enumerate(actions)}

sequences, labels = [], []
for action in actions:
    for sequence in np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(int):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

X = np.array(sequences)
y = np.array(labels)
num_classes = len(actions)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# Transformer Neural Network
def positional_encoding(sequence_length, d_model):
    pos = np.arange(sequence_length)[:, np.newaxis]
    i = np.arange(d_model)[np.newaxis, :]
    angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(d_model))
    angle_rads = pos * angle_rates
    sines = np.sin(angle_rads[:, 0::2])
    cosines = np.cos(angle_rads[:, 1::2])
    pos_encoding = np.concatenate([sines, cosines], axis=-1)
    return pos_encoding

d_model = 1662
num_heads = 4
dense_units = 64

train_samples = X_train.shape[0]
test_samples = X_test.shape[0]

X_train_pe = np.repeat(np.expand_dims(positional_encoding(sequence_length, d_model), axis=0), train_samples, axis=0)
X_test_pe = np.repeat(np.expand_dims(positional_encoding(sequence_length, d_model), axis=0), test_samples, axis=0)


def transformer_model(sequence_length, d_model, num_heads, dense_units, num_classes):
    inputs = Input(shape=(sequence_length, d_model))
    pos_encoding = Input(shape=(sequence_length, d_model))
    attention = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=d_model)
    attention_out = attention(inputs, inputs)
    add1 = tf.keras.layers.Add()([inputs, attention_out])
    norm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)(add1)
    dense1 = tf.keras.layers.Dense(units=dense_units, activation=gelu)(norm1)
    dense2 = tf.keras.layers.Dense(units=d_model, activation=gelu)(dense1)
    add2 = tf.keras.layers.Add()([norm1, dense2])
    norm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)(add2)
    output = tf.keras.layers.GlobalAveragePooling1D()(norm2)
    output = tf.keras.layers.Dense(units=num_classes, activation='softmax')(output)
    model = Model(inputs=[inputs, pos_encoding], outputs=output)
    return model

model = transformer_model(sequence_length, d_model, num_heads, dense_units, num_classes)

optimizer = Adam(learning_rate=0.0001)
loss = SparseCategoricalCrossentropy()
accuracy = SparseCategoricalAccuracy()

model.compile(optimizer=optimizer, loss=loss, metrics=[accuracy])

model.fit([X_train, X_train_pe], y_train, validation_data=([X_test, X_test_pe], y_test),
          batch_size=32, epochs=700)

# Save
model.save('Transformer.h5')