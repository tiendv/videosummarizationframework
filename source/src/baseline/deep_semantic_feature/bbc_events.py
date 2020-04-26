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
from func.sampling.vsum_events import VSUM

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

def run_vsum_dsf(path_save_txt,path_video,datatype,path_npy,path_reference):
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

    if not os.path.isdir(path_save_txt):
        os.makedirs(path_save_txt)
#    for v_id in glob.glob(os.path.join(path_video,"*.mp4")):
#        try :
#    v_id = (v_id.split("/")[-1]).split(".")[0]
    fps = 0
    dict_refer= {}
    video_done=[]
    with open("logevents.txt","r") as log:
        Lines = log.readlines() 
        for line in Lines:
            video_done.append(line.replace("\n",""))
    with open(path_reference,"r") as f:
        Lines = f.readlines() 
        for line in Lines:
            dict_refer[str("video"+((line.split("    ")[1]).split("_")[0]).replace("shot",""))] = str(line.split("    ")[0])
    for i in range(1,243):          ### special and depends on path_npy
        v_id = "video"+str(i)
        real_name = dict_refer[v_id]
        video =  cv2.VideoCapture(os.path.join(path_video,real_name))
        ###
        done = False
        for j in range(len(video_done)):
            if v_id == video_done[j]:
                done = True
                break
        if done == True :        
            print "Done:" , v_id 
            continue
        else:
            print "Process:",v_id   
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
                vsum = VSUM( v_id, model,fps,datatype,duration,path_npy,int(total_frames))

        _, frames, _ = vsum.summarizeRep(seg_l=4, weights=[1.0, 0.0])


        # get 0/1 label for each frame
        fps = vsum.dataset.data['fps']
        fnum = vsum.dataset.data['fnum']
        label = get_flabel(frames, fnum, fps, seg_l=4)


        label = label.ravel().astype(np.bool)
        time_per_frames = duration/total_frames
        #print time_per_frames

        time_start=0
        time_end = 0
        in_seg = False
        if not os.path.isdir(os.path.join(path_save_txt,real_name.replace(".mp4",""))):
            os.makedirs(os.path.join(path_save_txt,real_name.replace(".mp4","")))
        with open(os.path.join(path_save_txt,real_name.replace(".mp4",""),real_name.replace(".mp4","")+".txt"),"w+") as f:
            for i in range(len(label)) :

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
            with open("logevents.txt","a") as log:
                if v_id not in video_done:
                    log.write(str(v_id)+"\n")

        # write summarized video
    #    from skvideo.io import vread, vwrite

    #    video_path = '/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/videos/5206894509409203177.mp4' #% v_id

    #    video_data = vread(video_path)

    #    sum_vid = video_data[label.ravel().astype(np.bool), :,:,:]


    #    print 'writing video to', 'sum_%s.mp4'%v_id
    #    vwrite('sum_%s.mp4'%v_id, sum_vid)
    #        except:
    #            print "error:",v_id
#        print duration
#        raw_input()



if __name__ == "__main__":

    ### config this code
    path_save_txt = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/time_shots_bbc/event_seg_vsum_dsf_fix"
    path_video = "/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/videos"
    datatype= 'bbc'  ###tvsum or summe or bbc
    path_npy = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/events_shot'
    path_reference = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/reference_bbc/master_shot_reference.txt"
    ###

    run_vsum_dsf(path_save_txt,path_video,datatype,path_npy,path_reference)


