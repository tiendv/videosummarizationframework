from keras.applications import vgg16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
import glob, os
import json
from PIL import Image
from matplotlib import cm
import cv2
import imutils
import random
import tensorflow as tf
import os
import keras.backend.tensorflow_backend as K
from tensorflow.python.client import device_lib
import tensorflow as tf

tf.debugging.set_log_device_placement(True)

gpus = tf.config.experimental.list_logical_devices('GPU')
if gpus:
  # Replicate your computation on multiple GPUs
  c = []
  for gpu in gpus:
    print(gpu.name)

path_mp4 = "/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video"

list_mp4 = glob.glob(path_mp4+"/*.mp4")

model = vgg16.VGG16(weights='imagenet', include_top=True)
for p in list_mp4:
    file_name = os.path.basename(p).split(".")[0]

    vidcap = cv2.VideoCapture(p)

    success,image = vidcap.read()
    image = cv2.resize(image,(224,224))
    check = 0
    temp = []
    np.array(temp)
    while success:
        x = image
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        print check
        if check == 10:
            break
        with tf.device('/device:GPU:2'):
            features = model.predict(x)

        model_extractfeatures = Model(inputs=model.input, outputs=model.get_layer('fc2').output)
        with tf.device('/device:GPU:2'):
            fc2_features = model_extractfeatures.predict(x)

        fc2_features = fc2_features.reshape((4096,))
        temp.append(fc2_features)
        success,image = vidcap.read()
        image = cv2.resize(image,(224,224))
        check += 1

    np.save(file_name,temp)

    print(np.load("tvsum/"+file_name+'.npy').shape)
    raw_input()
