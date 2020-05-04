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
from os import listdir
from os.path import isfile, join

def get_data_ref_bbc(path_ref_bbc):
    '''
        This function will return the information about video id, and time of each shot in BBC dataset
        input: path_ref_bbc - the path of the master processed of bbc file
        output: ret - a dictionary with the key and value is the video_id and video_name, respectively
                dict_time - a dictionary with the key and value is the shot_id and its time, respectively
    '''
    ret = dict()
    dict_time = dict()
    with open(path_ref_bbc, 'r') as f:
        for line in f:
            video_name, shot_id, st, ed = line.rstrip().split()
            video_name = video_name.split('.')[0]
            video_id = shot_id.split('_')[0][4:]
            ret[video_id] = video_name
            dict_time[shot_id] = [st,ed]
    return ret,dict_time

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

def time2sec(times):
    x = time.strptime(times.split('.')[0],'%H:%M:%S')
    range_mili = 1
    mili = 0
    if len(times.split(".")) == 2 :
        if times.split(".")[1] != '':
            for i in range(len(times.split(".")[1])):
                range_mili = 10*range_mili
            mili = float(times.split(".")[1])/range_mili
        else:
            mili =0
    else:
        mili = 0
    return float(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds() + mili)

def write_data(selected,path_refer,path_save,real_name):
    real_name = real_name.replace(".mp4","")
    ret,time = get_data_ref_bbc(path_refer)
    if not os.path.isdir(os.path.join(path_save,real_name)):
        os.makedirs(os.path.join(path_save,real_name))
    for shot in selected:
        with open(os.path.join(path_save,real_name,real_name+".txt"),"a") as f:
            f.write(sec2time(time2sec(time[shot][0])) + " " + sec2time(time2sec(time[shot][1]))+"\n")


def run_kmedoids(path_csv,k,video_id):
    feat_type="vgg"
    video_id = "video"+str(video_id)
    # Load model
    data = []
    file_csv = [f for f in listdir(os.path.join(path_csv,video_id)) if isfile(join(os.path.join(path_csv,video_id), f))]
    temp = []
    for i in file_csv:
        temp.append(int((i.split("_")[1]).split(".")[0]))
    temp=sorted(temp)
    file_csv = []
    for i in temp:
        file_csv.append("shot"+str(video_id.replace("video",""))+"_"+str(i)+".csv")
    list_name_feature = []
    list_name_file = []
    for i in file_csv:
        f = pandas.read_csv(os.path.join(os.path.join(path_csv,video_id,i)),header=None)
        for name_feature in f[0]:
            list_name_feature.append(name_feature)
        if len(list_name_feature) != 0 :
            break
    for i in file_csv:
        f = pandas.read_csv(os.path.join(os.path.join(path_csv,video_id,i)),header=None)
        list_name_file.append(i)
        data.append(list(f[1]))
    with configuration.using_config('train', False):
        with chainer.no_backprop_mode():
            vsum = VSUM( video_id,data,int(np.array(data).shape[0]),k)

    _, frames, _ = vsum.summarizeRep(weights=[1.0, 0.0])

    # get 0/1 label for each frame
    fps = vsum.dataset.data['fps']
    fnum = vsum.dataset.data['fnum']
    label = get_flabel(frames, fnum, fps, seg_l=1)
    label = label.ravel().astype(np.bool)
    return [(list_name_file[i]).replace(".csv","")  for i in range(len(label)) if label[i] == 1]
#    write_data_bbc(label,time_per_frames,path_save_txt,real_name)

