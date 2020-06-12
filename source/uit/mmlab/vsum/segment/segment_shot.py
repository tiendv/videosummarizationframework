import sys
import os
import cv2
import numpy as np
from utilities.convert_time import sec2time
sys.path.append("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/baseline/segmentation/")
sys.path.append("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/libs/rethinking-evs/")

def sampling_shot(path_video,len_shot=2):
    '''
       This function uses to get time of shots of the input video
       input:
            path_video - path of a input video
            len_shot - length of each shot
       output: name(srt), begining time of shots (list), ending time of shots (list)
    '''
    name_vid = os.path.basename(path_video).split(".")[0]
    begining_shots = []
    ending_shots = []

    vid =cv2.VideoCapture(path_video)
    fps = vid.get(cv2.CAP_PROP_FPS)
    frames_cnt = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frames_cnt/fps
    k = duration
    step = lenshot
    begining_shots.append(0)

    while k > 0:
        t = begining_shots[-1]+step
        k=k-step
        if t <=duration:
            begining_shots.append(t)
            ending_shots.append(t)
        else:
            ending_shots.append(duration)
    if len(begining_shots) > len(ending_shots):
        del begining_shots[-1]
    return name_vid, list(map(sec2time, begining_shots)), list(map(sec2time,ending_shots))

def do_twopeak(n_fr, lam_1=40, lam_2=80):
    '''
        Using two-peak method to segment a video
        input:
            save_path -- path saving the result
            input_path -- path of input csv file
        output:
            the result file is saved at save_path
    '''
    segment = []
    cur_pos = 0
    while(True):
        cur_pos += np.random.choice([np.random.poisson(lam_1), np.random.poisson(lam_2)])
        if cur_pos > n_fr-1:
            break
        segment.append(cur_pos)
    return segment
