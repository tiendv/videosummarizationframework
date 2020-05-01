#!/usr/bin/env python
# coding: utf-8

import os,sys,glob
import numpy as np
import matplotlib.pyplot as plt
import skimage
from skimage import io
import caffe
import pickle
import cv2
import time
import csv
import argparse
sys.path.append("../../../config")
from config import cfg

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

DEMO_DIR = '.'

categories = [ 'Angry' , 'Disgust' , 'Fear' , 'Happy'  , 'Neutral' ,  'Sad' , 'Surprise']

#load model
cur_net_dir = 'VGG_S_rgb'    
mean_filename=os.path.join(DEMO_DIR,cur_net_dir,'mean.binaryproto')
proto_data = open(mean_filename, "rb").read()
caffe.set_mode_gpu()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
caffe.set_mode_gpu()
mean  = caffe.io.blobproto_to_array(a)[0]

net_pretrained = os.path.join(DEMO_DIR,cur_net_dir,'EmotiW_VGG_S.caffemodel')
net_model_file = os.path.join(DEMO_DIR,cur_net_dir,'deploy.prototxt')
caffe.set_mode_gpu()
VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
                      mean=mean,
                      channel_swap=(2,1,0),
                      raw_scale=255,
                      image_dims=(256, 256))


def detect_emotion(path_faces,path_keyframes,path_emotions, video):
    print("Processing:",video)
    for name in os.listdir(os.path.join(path_faces,video)):
        path_pickle = os.path.join(path_faces,video,name)    #read single pickle path file
        #read only pickle file, filter unnecessary file
        if(name.split(".")[-1] != "pickle"): 
            continue
        dict_temp= {}
        dict_temp["Sad"] = 0
        dict_temp["Angry"] = 0
        dict_temp["Disgust"] = 0
        dict_temp["Fear"] = 0
        dict_temp["Happy"] = 0
        dict_temp["Neutral"] = 0
        dict_temp["Surprise"] = 0
        name_video = video
        try:
            with open(path_pickle, 'rb') as f:
                data = pickle.load(f)
                for i in range(len(data)):
                    name_shot = name.split(".")[0]
                    name_frame = data[i][0]
                    img = io.imread(os.path.join(path_keyframes,name_video,name_shot,name_frame))
                    img_face = img[data[i][1][1]:data[i][1][3],data[i][1][0]:data[i][1][2]] #[ymin:ymax,xmin,xmax]
                    input_image = skimage.img_as_float(img_face).astype(np.float32)
                    caffe.set_mode_gpu()
                    prediction = VGG_S_Net.predict([input_image],oversample=False)
                    if ('{0}').format(categories[prediction.argmax()]) in categories:
                        dict_temp[str(('{0}').format(categories[prediction.argmax()]))] += 1
        except EOFError:
            print(path_pickle)
        path_save = os.path.join(path_emotions,name_video)
        if not os.path.isdir(path_save):
            os.makedirs(path_save)
        with open(os.path.join(path_emotions,name_video,name.replace("pickle","csv")), mode='w', newline='') as csv_file:
            print(os.path.join(path_emotions,name_video,name.replace("pickle","csv")))
            writer = csv.writer(csv_file)
            writer.writerow(["Sad",str(dict_temp["Sad"])])
            writer.writerow(["Angry",str(dict_temp["Angry"])])
            writer.writerow(["Disgust",str(dict_temp["Disgust"])])                    
            writer.writerow(["Fear",str(dict_temp["Fear"])])
            writer.writerow(["Happy",str(dict_temp["Happy"])])
            writer.writerow(["Neutral",str(dict_temp["Neutral"])])
            writer.writerow(["Surprise",str(dict_temp["Surprise"])])
    print("Done:",video)

