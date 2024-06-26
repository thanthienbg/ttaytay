# -*- coding: utf-8 -*-
"""BTL_DSS_Using-CNN_.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EaI3SeucCMNb9xJq_ux2T-vGXymmHk_m
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import RMSprop

data = pd.read_csv('/content/drive/MyDrive/HaUI Subject/Hệ hỗ trợ quyết định (DSS)/BTL/Dataset/A_Z Handwritten Data.csv')

data.head(5)

data.info()

data['0'].unique()

# classes hashmap
classes = {i:chr(i+65) for i in range(26)}
classes

# get images (x) & labels (y)
# the first column contains labels, while the remaining are the flattened array of 28 x 28 image pixels
y = data.values[:, 0]
x = data.values[:, 1:]

# reshape images
x = np.reshape(x, (x.shape[0], 28, 28, 1))

x[0]

# split data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# training & testing generators
datagen_train = ImageDataGenerator(rescale=1./255,
                                   validation_split=0.2,
                                   rotation_range=15,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   shear_range=0.1,
                                   zoom_range=0.2,
                                   horizontal_flip=False,
                                   fill_mode='nearest')
datagen_test = ImageDataGenerator(rescale=1./255)

data_train = datagen_train.flow(x_train, y_train, subset='training',
                                batch_size=64, shuffle=True)
data_valid = datagen_train.flow(x_train, y_train, subset='validation',
                                batch_size=64, shuffle=True)
data_test = datagen_test.flow(x_test, y_test, batch_size=1, shuffle=False)

model = Sequential([
                Conv2D(32, (3,3), activation='relu', input_shape=(28, 28, 1)),
                MaxPooling2D(2,2),
                Conv2D(32, (3,3), activation='relu'),
                MaxPooling2D(2,2),
                Flatten(),
                Dense(512, activation='relu'),
                Dense(26, activation='softmax')])  # 26 = total english letters
model.summary()

# compile model
model.compile(optimizer=RMSprop(learning_rate=1e-4),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# fit model
history = model.fit(data_train,
                    epochs=50,
                    validation_data=data_valid,
                    steps_per_epoch=500,
                    validation_steps=50,
                    verbose=2)

from tensorflow.keras.models import load_model
model.save('/content/drive/MyDrive/HaUI Subject/Hệ hỗ trợ quyết định (DSS)/BTL/saveModel/modela_z_50epoch.h5')

eval_model = model.evaluate(data_test, return_dict=True)
eval_model

# training and validation loss
plt.figure(figsize=(5, 4))
plt.plot(history.history['loss'], label='training')
plt.plot(history.history['val_loss'], label='validation')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend(loc='best')
plt.title('Training & Validation Loss')

# get an image and its actual label/class
# the batch size in data_test is 1, each batch contains 1 sample
# each sample is a 2d nested array. index 0= image features(x), index 1= label(y)
test_img = data_test[26][0]          # data_test[i][x] i=ith sample, x=features
test_label = data_test[0][1][0]     # data_test[i][y] i=ith sample, y=label array

test_label_pred = np.argmax(model.predict(test_img))

# plot results
plt.figure(figsize=(2, 2))
plt.imshow(test_img.reshape(28, 28), cmap='binary')
plt.title(f'actual:{classes[test_label]}, predicted:{classes[test_label_pred]}')

classes[test_label]

test_img = data_test[263][0]

test_label_pred = np.argmax(model.predict(test_img))

plt.imshow(test_img.reshape(28, 28), cmap='binary')

print(classes[test_label_pred])