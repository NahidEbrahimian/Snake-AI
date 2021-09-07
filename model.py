
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

data = pd.read_csv('Dataset.csv')
X = data.drop(['direction'], axis = 1)
Y = data['direction']

X = np.array(X)
Y = np.array(Y)

X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size = 0.2)
Y_train = Y_train.reshape(-1, 1)
Y_val = Y_val.reshape(-1, 1)

model = tf.keras.models.Sequential([
                        tf.keras.layers.Dense(20, input_dim = 20, activation='relu'),
                        tf.keras.layers.Dense(64, activation='relu'),
                        tf.keras.layers.Dense(128, activation='relu'),
                        tf.keras.layers.Dense(256, activation='relu'),
                        tf.keras.layers.Dense(512, activation='relu'), 
                        tf.keras.layers.Dense(4, activation='softmax')
                                    ])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss=tf.keras.losses.sparse_categorical_crossentropy,  metrics=['accuracy'])

model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=5)
model.save('Train/model.h5')