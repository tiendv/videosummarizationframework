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

def write_data(label,path_save_txt,path_reference,real_name):
    if not os.path.isdir(os.path.join(path_save_txt,real_name.replace(".mp4",""))):
        os.makedirs(os.path.join(path_save_txt,real_name.replace(".mp4","")))
    with open(os.path.join(path_save_txt,real_name.replace(".mp4",""),real_name.replace(".mp4","")+".txt"),"w") as f:
            with open(path_reference,"r") as refer:        
                Lines = refer.readlines() 
                for line in Lines:
                    if line.split("    ")[1] in label:
                        f.write(sec2time(time2sec(line.split("    ")[2]))+" "+sec2time(time2sec((line.split("    ")[3]).replace("\n","")))+"\n")
                        print(sec2time(time2sec(line.split("    ")[2]))+" "+sec2time(time2sec((line.split("    ")[3]).replace("\n","")))+"\n")
    print(os.path.join(path_save_txt,real_name.replace(".mp4",""),real_name.replace(".mp4","")+".txt"))
def create_feature(path_csv,path_reference,video_id):
    data = []
    file_csv = [f for f in listdir(os.path.join(path_csv,video_id)) if isfile(join(os.path.join(path_csv,video_id), f))]
    temp = []
    for i in file_csv:
        temp.append(int((i.split("_")[1]).split(".")[0]))
    temp=sorted(temp)
    file_csv = []
    for i in temp:
        file_csv.append("shot"+str(video_id.replace("video",""))+"_"+str(i)+".csv")
    vector = []
    dict_refer = {}
    with open(path_reference,"r") as f:
        Lines = f.readlines() 
        time_filter = 0
        start = 0
        end = 0
        total = 0
        total_shot = 0
        for line in Lines:    
            if int(((line.split("    ")[1]).split("_")[0]).replace("shot","")) != int(video_id.replace("video","")) :
                continue
            start = end
            end = float(time2sec((line.split("    ")[3]).replace("\n","")))
            if time_filter + ((end-start)-int(end-start)) >= 1 :
                time_filter  =  ((end-start)-int(end-start)) + time_filter -1
                dict_refer[str("video"+((line.split("    ")[1]).split("_")[0]).replace("shot",""))+str(line.split("    ")[1])] = (int(end-start)+1)
                total += (int(end-start)+1)
            else:
                time_filter += ((end-start)-int(end-start))
                dict_refer[str("video"+((line.split("    ")[1]).split("_")[0]).replace("shot",""))+str(line.split("    ")[1])] = (int(end-start))
                total +=int(end-start)
            if int(((line.split("    ")[1]).split("_")[0]).replace("shot","")) == int(video_id.replace("video","")) :
                total_shot = int((line.split("    ")[1]).split("_")[1])
    list_events = []
    totals = 0
    for i in file_csv:
        f = pandas.read_csv(os.path.join(os.path.join(path_csv,video_id,i)),header=None)
        for name_feature in f[0]:
            list_events.append(name_feature)
        if len(list_events) != 0 :
            break
    for i in range (1,total_shot+1):
        name_shot = str("shot"+video_id.replace("video","")+"_"+str(i))
        key_frames = dict_refer[str(video_id)+str(name_shot)]
        temp = [0] * len(list_events)
        try:
            f=  pandas.read_csv(os.path.join(os.path.join(path_csv,video_id),name_shot+".csv"),header=None)             
            for j in range(len(list_events)):
                id = 0
                for event  in f[0]:
                    if event == list_events[j]:
                        temp[j] = f[1][id]
                    id+=1
        except:
            a = 0
        for k in range(1):
            totals+=key_frames
            vector.append(temp)
    return np.array(vector),totals

def run_kmedoids(data,k,video_id,totals):
    seg_l = 1
    fps = 1
    video_id = "video"+str(video_id)

    duration = int(np.array(data).shape[0])
    k = int(totals*0.15/float(totals/float(np.array(data).shape[0])))
    with configuration.using_config('train', False):
        with chainer.no_backprop_mode():
            ### k-medoids
            vsum = VSUM( video_id,data,duration,k,seg_l,fps)

    _, frames, _ = vsum.summarizeRep(weights=[1.0, 0.0],seg_l=seg_l)
    temp = []

    for i in range(len(frames)):
        if (len(frames[i])>0):
            temp.append("shot"+str(video_id.replace("video",""))+"_"+str(int(frames[i][0][0:-4])))
    frames = temp
    return frames
    # get 0/1 label for each frame
    fps = vsum.dataset.data['fps']
    fnum = vsum.dataset.data['fnum']
    label = get_flabel(frames, fnum, fps, seg_l=seg_l)
    label = label.ravel().astype(np.bool)



