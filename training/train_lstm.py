import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import mediapipe as mp
import tensorflow as tf

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

from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

label_map = {label:num for num, label in enumerate(actions)}

sequences, labels = [], []
for action in actions :
    for sequence in range(no_sequences) :
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

X = np.array(sequences)
y = to_categorical(labels).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# LSTM Neural Network
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(40,1662)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

model.fit(X_train, y_train, epochs=700)

# Save
model.save('LSTM.h5')