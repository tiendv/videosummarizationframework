# If you want change code to summarize your video, you should consider main.py, vsum.py, summe.py ### Important note from Trivlm 10/4/2020


import numpy as np
import os
import json
import cv2
import glob

from func.nets import vid_enc, vid_enc_vgg19
from chainer import serializers

import sys
sys.path.append('script/')
from summarize import get_flabel
from func.sampling.vsum import VSUM

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

def run_vsum_dsf(path_save_txt,path_video,datatype,path_npy):
    # settings
    feat_type = 'smt_feat' # smt_feat (proposed) or vgg

    # load embedding model
    if feat_type == 'smt_feat':
        model = vid_enc.Model()
        serializers.load_npz('data/trained_model/model_par', model)
    elif feat_type == 'vgg':
        model = vid_enc_vgg19.Model()

    else:
        raise RuntimeError('[invalid feat_type] use smt_feat or vgg')

    # prepair output dir
    d_name = 'summe'
    dataset_root = 'data/{}/'.format(d_name)
    out_dir = 'results/{:}/{:}/'.format(d_name, feat_type)
    print 'save to: ', out_dir

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # load dataset metadata
    dataset = json.load(open(dataset_root + 'dataset.json'))
    video_id = [d['videoID'] for d in dataset]

    #print 'Video list:'
    #for vi in video_id:
    #    print '-', vi

    # summarize video
    path_reference = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/reference_bbc/master_shot_reference.txt"
    dict_refer= {}
    with open(path_reference,"r") as f:
        Lines = f.readlines() 
        for line in Lines:
            dict_refer[str("video"+((line.split("    ")[1]).split("_")[0]).replace("shot",""))] = str(line.split("    ")[0])
    if not os.path.isdir(path_save_txt):
        os.makedirs(path_save_txt)

    for v_id in glob.glob(os.path.join(path_video,"*.mp4")):
#        try:
        fps = 0
        v_id = (v_id.split("/")[-1]).replace(".mp4","")
        video =  cv2.VideoCapture(os.path.join(path_video,v_id+".mp4"))
        ###
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        #print total_frames
    #    video.set(cv2.CAP_PROP_POS_AVI_RATIO,total_frames)
    #    duration=video.get(cv2.CAP_PROP_POS_MSEC)
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver)  < 3 :
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
            #print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
        else :
            fps = video.get(cv2.CAP_PROP_FPS)
            #print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)
        duration = total_frames/fps
        #print "duration:" , duration
        with configuration.using_config('train', False):
            with chainer.no_backprop_mode():
#                print v_id
                vsum = VSUM( v_id, model,fps,datatype,duration,path_npy)

        _, frames, _ = vsum.summarizeRep(seg_l=5, weights=[1.0, 0.0])
        print fps

        # get 0/1 label for each frame
        fps = vsum.dataset.data['fps']
        fnum = vsum.dataset.data['fnum']
        label = get_flabel(frames, fnum, fps, seg_l=5)


        label = label.ravel().astype(np.bool)
        time_per_frames = duration/total_frames
        #print time_per_frames

        time_start=0
        time_end = 0
        in_seg = False
        if not os.path.isdir(os.path.join(path_save_txt,v_id)):
            os.makedirs(os.path.join(path_save_txt,v_id))
        with open(os.path.join(path_save_txt,v_id,v_id+".txt"),"w+") as f:
            for i in range(len(label)) :
                if label[i]==True and in_seg==False:
                    time_start = i*time_per_frames
                    in_seg=True
                if label[i]==False and in_seg==True:
                    time_end = i*time_per_frames
                    f.write(str(sec2time(time_start))+ " " +str(sec2time(time_end)) + " 1\n")
                    print(str(sec2time(time_start))+ " " +str(sec2time(time_end)) + " 1\n")
                    time_start=0
                    time_end = 0
                    in_seg  = False
#        except:
#            print "error:",v_id



if __name__ == "__main__":

    ### config this code
    path_save_txt = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_shots_summe/vsum_dsf"
    path_video = "/mmlabstorage/datasets/SumMe/videos"
    datatype= 'summe'  ###tvsum or summe or bbc
    path_npy = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_shots_summe/feature_vgg'
    ###

    run_vsum_dsf(path_save_txt,path_video,datatype,path_npy)


