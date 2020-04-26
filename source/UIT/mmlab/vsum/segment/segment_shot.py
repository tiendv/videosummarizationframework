import sys
import os
import cv2
from utilities.convert_time import sec2time
sys.path.append("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/baseline/segmentation/")
from TransNet.run_trainsnet import run_trainsnet

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

def doTrainsnet(vid_path):
    shots,total_frame = run_trainsnet(vid_path)
    vid_name = os.path.basename(vid_path)

    cap=cv2.VideoCapture(vid_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    begins = []
    ends = []
    for s in shots:
        begins.append(sec2time(s[0]/fps))
        ends.append(sec2time(s[1]/fps))
    return vid_name,begins,ends
