#!/usr/bin/env python
# coding: utf-8

from tools.summarizer import summarize
from tools.io import load_summe_mat
from tools.io import load_tvsum_mat
from tools.segmentation import get_segment
import pandas as pd
from sklearn.metrics import f1_score
import numpy as np
import json
from joblib import Parallel, delayed
import pandas
import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/deep_semantic_feature/")
from config import cfg

def write_data(label,time_per_frames,path_save_txt,real_name):
    time_start=0
    time_end = 0
    in_seg = False
    if not os.path.isdir(os.path.join(path_save_txt,real_name.replace(".mp4",""))):
        os.makedirs(os.path.join(path_save_txt,real_name.replace(".mp4","")))
    with open(os.path.join(path_save_txt,real_name.replace(".mp4",""),real_name.replace(".mp4","")+".txt"),"w+") as f:
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
                time_start=0
                time_end = 0
                in_seg = False
        print (os.path.join(path_save_txt,real_name.replace(".mp4",""),real_name.replace(".mp4","")+".txt"))
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

def run_random_methods(path_save,path_infor,video_id,datatype,path_score="",method='uniform'):
    fps = 0
    total_frames = 0
    duration = 0
    data = pandas.read_csv(os.path.join(path_infor),header=None)
    
    for i in range(data.shape[0]):
        if data[0][i] == str(video_id+".mp4"):
            fps = float(data[2][i])
            total_frames = int(float(data[3][i]))
            duration = float(data[4][i])
    if path_score == "":
        rand_score = np.random.random((total_frames,))
    else:
        rand_score = np.load(os.path.join(path_score,video_id+".npy"))
    segment = get_segment(total_frames,video_id,datatype,method)
    rand_summary = summarize(rand_score, segment, int(float(total_frames) * .15))
    time_per_frames = duration / total_frames
    write_data(rand_summary,time_per_frames,path_save,video_id)


