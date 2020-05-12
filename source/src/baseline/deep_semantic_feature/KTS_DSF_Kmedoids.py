#!/usr/bin/env python
# coding: utf-8

import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/deep_semantic_feature/")
sys.path.append("../../../../source/utilities/")
from convert_time import sec2time
from func.nets import vid_enc, vid_enc_vgg19
from chainer import serializers
from bbc_kmedoids_lib import run_kmedoids
from joblib import Parallel, delayed
from config import cfg
import pandas
import numpy as np


def create_feature(boundaries,feature,pretrained_model):
    #************************************************************************
    # Purpose: create feature base on KTS boundaries
    # Inputs:
    # - boundaries: [0 60 120 180 ... 2400]
    # - feature: VGG16:(total_frames,4096) or Resnet50: (total_frames,2048)
    # - pretrained_model: True: using pretrained model or Fales: not using pretrained model
    # Output: feature: feature of shot will using in kmedoids || k: value of K in Kmedoids
    # Author: Trivlm
    #************************************************************************

    feature_all_shots = []
    start =0
    end = 0
    # processing each shot
    for i in range(1,len(boundaries)):
        
        # get feauture each shot [0:60][4096]
        start = end 
        end = boundaries[i]
        feature_shot = np.array(feature[start:end])

        # using pretrained model or not
        if pretrained_model == True:
            model = vid_enc.Model(b_size = {'video': feature_shot.shape[0]})
            serializers.load_npz('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/libs/deep_semantic_feature/data/trained_model/model_par', model)
        else:
            model = vid_enc_vgg19.Model(b_size = {'video': feature_shot.shape[0]})

        #  get feature of all frames that shots -> model -> 1 feature represent
        enc_x = model(feature_shot)

        # create list of feature represent
        feature_all_shots.append(enc_x.data[0])

    # get K value: K = total_time*0.15 / averange_time_per_shot
    k= int(boundaries[-1]*0.15 / (boundaries[-1]/(len(boundaries)-1) )+0.5)

    # return list of feature represent and K
    return np.array(feature_all_shots) , k
def run_KTS_DSF_Kmedoids():
    #************************************************************************
    # Purpose: select shots from KTS 
    # Inputs:
    # - path_npy : path extract feature from VGG16 or Resnet50 ,...
    # - path_boundaries: path boundaries of dataset
    # Output: the result time selection for summarization will be store in path_save
    # Author: Trivlm
    #************************************************************************

    # args
    path_npy = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/frames_feature/VGG16/'
    path_boundaries = '/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/boundaries/TVSum/'
    pretrained_model = True
    path_save_txt = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/time_segment/dsf_vgg16_kts'

    # read data
    data = pandas.read_csv(os.path.join(cfg.VIDEO_CSV_TVSUM_PATH),header=None)
    
    # processing each video
    for i in range(1,data.shape[0]):
        vid_id = (data[0][i]).replace(".mp4","")
        print "***Procesing video:", vid_id,"****"

        # get boundaries and feature extraction that video
        boundaries = np.load(path_boundaries+vid_id+".npy")
        feature =  np.load(path_npy+vid_id+".npy")
        
        # create feature for kmedoids
        feature, k = create_feature(boundaries,feature,pretrained_model)

        # run kmedoids for feature
        selected = run_kmedoids(feature,k,vid_id)
        print selected

        # code save label 0/1 each video for evaluate
        # label = np.zeros(boundaries[-1])
        # for i in selected:
        #     label[boundaries[i-1]:boundaries[i]] = 1
        # np.save(path_label+"/"+vid_id,label)

        # read dataset information to get fps 
        fps = 0
        data = pandas.read_csv(os.path.join(cfg.VIDEO_CSV_TVSUM_PATH),header=None)
        for i in range(data.shape[0]):
            if data[0][i] == vid_id+".mp4":
                fps = float(data[2][i])

        # save time output
        if not os.path.isdir(os.path.join(path_save_txt,vid_id)):
            os.makedirs(os.path.join(path_save_txt,vid_id))
        with open(os.path.join(path_save_txt,vid_id,vid_id+".txt"),"w+") as f:
            for i in selected:
                f.write(sec2time((boundaries[i-1])/fps)+" "+sec2time(boundaries[i]/fps)+"\n")
                print(sec2time((boundaries[i-1])/fps)+" "+sec2time(boundaries[i]/fps)+"\n")



if __name__ == "__main__":
    run_KTS_DSF_Kmedoids()
