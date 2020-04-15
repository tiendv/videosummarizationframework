import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import math
import video_segmentation as vs
import feature_extraction as feat
import clusterization as cl
import shutil
import time
import sys


def vsumm_frames_in_memory(video):
    segmentation = vs.VideoSegmentation(video)
    frames = segmentation.read_and_keep_frames()

    if len(frames) == 0:
        return False

    features = feat.extract_features(frames)
    keyframes = cl.find_clusters(features)

    summary_folder = 'summaryM-'+video[7:-4]
    if not os.path.isdir(summary_folder):
        os.mkdir(summary_folder)

    for k in keyframes:
        frame = frames[k.frame_id-1]
        frame_name = summary_folder+'/frame-'+str(k.frame_id).zfill(6)+'.jpg'
        cv2.imwrite(frame_name,frame)

    return True
#input: Video-path and sampling-rate
def make_folder(path,name):
    p = os.path.join(path,name)
    if os.path.exists(p) is False:
        os.mkdir(p)
    
def vsumm_frames_in_disk(video,frames_folder,videoname,samplingrate,outpath):
    #Folder of frame
    '''
    frames_folder = 'frames-'+video[7:-4]
    if not os.path.isdir(frames_folder):
        os.mkdir(frames_folder)
    '''
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print ('cannot read video')
        return 0
    #frames_folder ='frames-'+video[7:-4]
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    #segmentation = vs.VideoSegmentation(video)
    #segmentation.read_and_save_frames(frames_folder)
    #frames_list = os.listdir(frames_folder)
    
    frames_list = [str(i*samplingrate)+'.jpg' for i in range(0,int(frame_count/samplingrate))]
    
    #frames_list.sort()
    print(len(frames_list),frame_count)
    features = feat.read_frames_extract_features(frames_folder,frames_list)
    keyframes = cl.find_clusters(features)
    make_folder(outpath,str(samplingrate))
    
    make_folder(os.path.join(outpath,str(samplingrate)),videoname)
    pa = os.path.join(outpath,str(samplingrate),videoname)
    with open(os.path.join(pa,videoname+'.txt'), 'a') as the_file:
        for  k in keyframes:
            the_file.write(str(k.frame_id)+'.jpg\n')



def main():
    
    path_data = sys.argv[1]
    #'H:\Thesis\DATA\\tvsum50_ver_1_1\ydata-tvsum50-v1_1\\frames'
    
    path_frames = sys.argv[2]
    #'H:\Thesis\DATA\\tvsum50_ver_1_1\ydata-tvsum50-v1_1\\video'

    outpath = sys.argv[3]
    sam_rate = int(sys.argv[4])
    videos_list = os.listdir(path_data)
    for idx,video in enumerate(videos_list):
        print("%s/%s :%s"%(idx+1,len(videos_list),video))
        fName_no_ex=os.path.splitext(video)[0]
        start = time.time()
        video_dir = os.path.join(path_data,video)
        p_f = os.path.join(path_frames,fName_no_ex)
        vsumm_frames_in_disk(video_dir,p_f,fName_no_ex,sam_rate,outpath)
        end = time.time()
        elapsed_time = end-start
        print ('Time:', elapsed_time)

if __name__ == '__main__':
    main()