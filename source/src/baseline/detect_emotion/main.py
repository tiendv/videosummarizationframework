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


plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


DEMO_DIR = '.'

categories = [ 'Angry' , 'Disgust' , 'Fear' , 'Happy'  , 'Neutral' ,  'Sad' , 'Surprise']


# In[ ]:


def showimage(im):
    if im.ndim == 3:
        im = im[:, :, ::-1]
    plt.set_cmap('jet')
    plt.imshow(im,vmin=0, vmax=0.2)
    

def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    showimage(data)



def create_txt_emotion(path_faces,path_keyframes,path_emotions):
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
    #read data
    list_name_video = []
    for i in range(123,244): #tà đạo quá TT
        list_name_video.append("video"+str(i))
    for video in list_name_video:
        for name in os.listdir(os.path.join(path_faces,video)):
            path_pickle = os.path.join(path_faces,video,name)    #read single pickle path file
            if(name.split(".")[-1] != "pickle"):  #read only pickle file, filter unnecessary file
                continue
            #start = time.time()
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
                        #print(name_video)
                        #print(name_shot)
                        #print(name_frame)
                        #print(data[i][1])
                        img = io.imread(os.path.join(path_keyframes,name_video,name_shot,name_frame))
                        img_face = img[data[i][1][1]:data[i][1][3],data[i][1][0]:data[i][1][2]] #[ymin:ymax,xmin,xmax]
                        input_image = skimage.img_as_float(img_face).astype(np.float32)
                        caffe.set_mode_gpu()
                        prediction = VGG_S_Net.predict([input_image],oversample=False)
                        #print (('{0}').format(categories[prediction.argmax()])+"\n")
                        #path_save = os.path.join(path_emotions,name_video,name_shot)
                        #print(path_save)
                        #print(str(str(data[i][1][0])+" "+str(data[i][1][1])+" "+str(data[i][1][2])+" "+str(data[i][1][3])+" "+('{0}').format(categories[prediction.argmax()])+"\n"))
                        if ('{0}').format(categories[prediction.argmax()]) in ["Sad","Angry","Disgust","Fear","Happy","Neutral","Surprise"]:
                            dict_temp[str(('{0}').format(categories[prediction.argmax()]))] += 1
                        #if not os.path.isdir(path_save):
                            #os.makedirs(path_save)
                        #name_save = name_frame.split(".")[0]+".txt"
                        #with open(os.path.join(path_save,"{}.txt".format(name_save)),'a') as f:
                            #caffe.set_mode_gpu()
                            #f.write(str(str(data[i][1][0])+" "+str(data[i][1][1])+" "+str(data[i][1][2])+" "+str(data[i][1][3])+" "+('{0}').format(categories[prediction.argmax()])+"\n"))
                #end = time.time()
                #print("Time prediction per pickle:" + str(end - start)+"\n")
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
               


if __name__ == '__main__':
    path_faces = "/home/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Faces"
    path_keyframes = "/home/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/Old_TRECVID_BBC_EastEnders_Keyframes"
    path_emotions = "/home/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/events_emotion"
    create_txt_emotion(path_faces,path_keyframes,path_emotions)
