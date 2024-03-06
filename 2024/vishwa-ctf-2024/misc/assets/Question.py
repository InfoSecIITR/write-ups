from tensorflow.keras.models import load_model

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import cv2

model = load_model('NumberRecognizer.h5')

img = cv2.imread("Image Path")
image = [img]

image = np.expand_dims(image, axis=-1)
predictions= np.argmax(model.predict(image))
plt.imshow(np.squeeze(image), cmap='gray')
plt.title(f'Predicted Value : {predictions}')

plt.show()