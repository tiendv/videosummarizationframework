import cv2
import os,sys,glob
import random
import argparse
from multiprocessing import Process

from utilities.convert_time import sec2time
from src.baseline.segmentation.create_json_from_time_shots import create_json4shots
from src.baseline.segmentation.segment_video import create_segments_tvsum

from src.baseline.selection.get_data_to_selection import get_data_to_selection,selection_shot_knapsack, create_json_selection
from config.config import cfg
def split_shots(path_video):
    '''
       This function uses to get time of shots of the input video
       input: path of a video
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
    step = 2
    begining_shots.append(0)
    while k > 0:
        t = begining_shots[-1]+step
        k=k-step
        if t <=duration:
            begining_shots.append(t)
            ending_shots.append(t)
        else:
            ending_shots.append(duration)
    return name_vid, list(map(sec2time, begining_shots)), list(map(sec2time,ending_shots))

def calc_score(list_begin,list_ending):
    list_score = []
    for _ in range(len(list_begin)):
        list_score.append(round(random.randint(10,50)/10,1))
    return list_score


def main_baseline(path_video,path_saved_json_shot="./",path_saved_json_segment='./',id_shot="shot_gt",id_seg="seg_gt"):
    '''
        This function uses to summarize a video and export json files for visualization
        input: path_save - path of a input video_duration
               path_saved_json_shot - path to save json file for visualizing shots
               path_saved_json_segment -  path to save json file for visualizing segments
        output: None
    '''
    #shot detection
    name_video,list_begin, list_ending = split_shots(path_video)
    # #cacl score
    # list_name, list_begin_seg , list_end_seg , list_score_seg = create_segments_tvsum(cfg.PATH_GT_TVSUM50)
    #
    # k=0
    # for i,n in enumerate(list_name):
    #     if n==name_video:
    #         k=i
    #         break
    # list_begin = list_begin_seg[k]
    # list_ending = list_end_seg[k]
    #
    # list_score = list_score_seg[k] ##list score for GT

    list_score = calc_score(list_begin,list_ending) ##list score for BL

    if os.path.isdir(os.path.join(path_saved_json_segment,name_video)):
        print("Done shot and segment for video{}".format(name_video))
        return

    #create json to visual shots
    create_json4shots(path_saved_json_shot,name_video,list_begin,list_score, id_shot)

    #excuting knapsack to select the shots for summarize
    result = selection_shot_knapsack(list_begin,list_ending,list_score)
    create_json_selection(name_video,list_begin,list_ending,result,path_saved_json_segment,id_seg)
    print("Done shot and segment for video{}".format(name_video))

if __name__ == '__main__':
    #path_video = "src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video/sTEELN-vY30.mp4"
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('path_video', type=str,
                    help='path of input video')
    parser.add_argument('--jshot', type=str,
                    help='path to save json file for visualizing shots')
    parser.add_argument('--jseg', type=str,
                    help='path to save json file for visualizing segments')
    args = parser.parse_args()
    main_baseline(args.path_video)
