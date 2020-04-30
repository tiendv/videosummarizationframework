# If you want change code to summarize your video, you should consider main.py, vsum.py, summe.py ### Important note from Trivlm 10/4/2020


import numpy as np
import os
import json
import cv2
import glob
import numpy as np
import h5py

from func.nets import vid_enc, vid_enc_vgg19
from chainer import serializers

import sys
sys.path.append('script/')
from summarize import get_flabel
from func.sampling.vsum2 import VSUM

import chainer
from chainer import configuration
import datetime
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

def run_vsum_dsf(path_save_txt,path_video,datatype,path_npy,seg_l,feat_type):
    # load embedding model
    if feat_type == 'smt_feat':
        model = vid_enc.Model(b_size = {'video': seg_l})
        serializers.load_npz('data/trained_model/model_par', model)
    elif feat_type == 'vgg':
        model = vid_enc_vgg19.Model(b_size = {'video': seg_l})
    else:
        raise RuntimeError('[invalid feat_type] use smt_feat or vgg')
    # summarize video
    if not os.path.isdir(path_save_txt):
        os.makedirs(path_save_txt)
    for v_id in glob.glob(os.path.join(path_video,"*.mp4")):
        v_id = (v_id.split("/")[-1]).split(".")[0]
        fps = 0
        video =  cv2.VideoCapture(os.path.join(path_video,v_id+".mp4"))
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver)  < 3 :
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        else :
            fps = video.get(cv2.CAP_PROP_FPS)
        duration = total_frames/fps
        with configuration.using_config('train', False):
            with chainer.no_backprop_mode():
                vsum = VSUM( v_id, model,fps,datatype,duration,path_npy)

        _, frames, _ = vsum.summarizeRep(seg_l=seg_l, weights=[1.0, 0.0])
        
        #get 0/1 label for each frame
        fps = vsum.dataset.data['fps']
        fnum = vsum.dataset.data['fnum']
        label = get_flabel(frames, fnum, fps, seg_l=seg_l)


        label = label.ravel().astype(np.bool)
        time_per_frames = duration/total_frames
        mat_lab = "/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat"
        f = h5py.File(mat_lab,'r')
        data = f.get('video')
        data_name = f.get('tvsum50/video')
        list_name = []
        for i in range(data_name.shape[0]):
            name= ''.join(map(chr,f[data_name[i][0]]))
            list_name.append(name)
        #print time_per_frames
        length_video = f.get('tvsum50/length')
        list_length = []
        for i in range(length_video.shape[0]):
            length= f[length_video[i][0]][0][0]
            list_length.append(length)

        # read total frames of each video
        nframes = f.get('tvsum50/nframes')
        list_nframes = []
        for i in range(nframes.shape[0]):
            length= f[nframes[i][0]][0]
            list_nframes.append(length)
        # get ground truth score of each video
        gt_score = f.get('tvsum50/gt_score')
        list_gt_score = []
        gt_score_video = []
        for i in range(nframes.shape[0]):
            gt_score_video= f[gt_score[i][0]][0]
            list_gt_score.append(gt_score_video)

        # get length frames per shot
        list_shot = []

        for i in range(len(list_gt_score)):
            nframes_per_2s = 100000
            len_min = 1
            for j in range(len(list_gt_score[i])):
                if(j + 1 == len(list_gt_score[i])):
                    len_min =1
                    continue
                if(list_gt_score[i][j] == list_gt_score[i][j+1]):
                    len_min += 1
                else:
                    if(len_min < nframes_per_2s):
                        nframes_per_2s = len_min
                        len_min = 1
            list_shot_temp = []
            j = nframes_per_2s
            while (True) :
                list_shot_temp.append(nframes_per_2s)
                j += nframes_per_2s
                if (j > len(list_gt_score[i])):
                    list_shot_temp.append( len(list_gt_score[i]) -j + nframes_per_2s)
                    break
            list_shot.append(np.array(list_shot_temp))

        # calculate time per frames of each video
        second_per_frame = []
        for i in range(data_name.shape[0]):
            second_per_frame.append(list_length[i]/list_nframes[i])
        time_per_frames = 0
        total_frames = 0
        for i in range(len(list_name)):
            if list_name[i] == v_id:
                temp = second_per_frame[i]*list_shot[i]
                total_frames = list_nframes[i]
#        print temp
        time_start=0
        time_end = 0
        in_seg = False
        if not os.path.isdir(os.path.join(path_save_txt,v_id)):
            os.makedirs(os.path.join(path_save_txt,v_id))
        print duration
        with open(os.path.join(path_save_txt,v_id,v_id+".txt"),"w+") as f:
            a=0
            begin=[]
            end=[]
            score=[]
            for i in range(len(temp)) :
                if label[int(i*fps*2)]==True and in_seg==False:
                    time_start = a
                    in_seg=True
                    begin.append(str(sec2time(time_start)))
                if label[int(i*fps*2)]==False and in_seg==True:
                    time_end = a
                    end.append(str(sec2time(time_end)))
                    score.append(1)
                    time_start=0
                    time_end = 0
                    in_seg = False  
                a+=temp[i]
                if i+1 == len(temp) and in_seg ==True:
                    time_end = a
                    end.append(str(sec2time(time_end)))
                    score.append(1)
            for i in range(len(begin)):
                print("{} {} {}\n".format(begin[i],end[i],score[i]))

