# If you want change code to summarize your video, you should consider main.py, vsum.py, summe.py ### Important note from Trivlm 10/4/2020

import numpy as np
import os
import json
import cv2
import glob
import sys
from chainer import serializers
sys.path.append('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/libs/deep_semantic_feature/script/')
from summarize import get_flabel
from func.sampling.vsum_events import VSUM
from func.nets import vid_enc
from func.nets import vid_enc_vgg19
import chainer
from chainer import configuration
import datetime
import pandas
import time

def sec2time(sec, n_msec=4):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec,'__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)

def write_data_bbc(label,time_per_frames,path_save_txt,real_name):
    time_start=0
    time_end = 0
    in_seg = False
    if not os.path.isdir(os.path.join(path_save_txt,real_name.replace(".mp4",""))):
        os.makedirs(os.path.join(path_save_txt,real_name.replace(".mp4","")))
    with open(os.path.join(path_save_txt,real_name.replace(".mp4",""),real_name.replace(".mp4","")+".txt"),"w+") as f:
        print os.path.join(path_save_txt,real_name.replace(".mp4",""),real_name.replace(".mp4","")+".txt")
        for i in range(len(label)):
            if label[i]==True and in_seg==False:
                time_start = i*time_per_frames
                in_seg=True
            if label[i]==False and in_seg==True:
                time_end = i*time_per_frames
                print(str(sec2time(time_start))+ " " +str(sec2time(time_end)) + " 1\n")
                f.write(str(sec2time(time_start))+ " " +str(sec2time(time_end)) + " 1\n")
                time_start=0
                time_end = 0
                in_seg = False
            if i+1 == len(label) and in_seg ==True:
                time_end = i*time_per_frames
                end.append(str(sec2time(time_end)))
                score.append(1)
                time_start=0
                time_end = 0
                in_seg = False

def run_kmedoids(path_save_txt,path_bbc_info,path_csv,path_reference,seg_l,video_id):
    feat_type="vgg"
    video_id = "video"+str(video_id)
    # Load model
    if feat_type == 'smt_feat':
        model = vid_enc.Model(b_size = {'video': seg_l})
        serializers.load_npz('data/trained_model/model_par', model)
    elif feat_type == 'vgg':
        model = vid_enc_vgg19.Model(b_size = {'video': seg_l})
    else:
        raise RuntimeError('[invalid feat_type] use smt_feat or vgg')

    # Load a dictionary: { 'video_id' : 'real name of video' }
    dict_refer= {}
    with open(path_reference,"r") as f:
        Lines = f.readlines() 
        for line in Lines:
            dict_refer[str("video"+((line.split("    ")[1]).split("_")[0]).replace("shot",""))] = str(line.split("    ")[0])
    real_name = dict_refer[video_id]

    fps = 0
    total_frames = 0
    duration = 0
    data = pandas.read_csv(os.path.join(path_bbc_info),header=None)
    for i in range(data.shape[0]):
        if data[0][i] == real_name:
            fps = float(data[2][i])
            total_frames = int(float(data[3][i]))
            duration = float(data[4][i])

    with configuration.using_config('train', False):
        with chainer.no_backprop_mode():
            vsum = VSUM( video_id, model,fps,duration,path_csv,int(total_frames),path_reference,dataset='summe',seg_l=seg_l)

    _, frames, _ = vsum.summarizeRep(seg_l=seg_l, weights=[1.0, 0.0])


    # get 0/1 label for each frame
    fps = vsum.dataset.data['fps']
    fnum = vsum.dataset.data['fnum']
    label = get_flabel(frames, fnum, fps, seg_l=seg_l)


    label = label.ravel().astype(np.bool)
    time_per_frames = duration/total_frames
    write_data_bbc(label,time_per_frames,path_save_txt,real_name)

