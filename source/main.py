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
    if len(begining_shots) > len(ending_shots):
        del begining_shots[-1]
    return name_vid, list(map(sec2time, begining_shots)), list(map(sec2time,ending_shots))

def calc_score(list_begin,list_ending):
    '''
        This function uses to create scores for shots randomly
        input:
            list_begin - the list of start time of each shot
            list_ending - the list of end time of each shot
        output:
            A list score for each shot
    '''
    list_score = []
    for _ in range(len(list_begin)):
        list_score.append(round(random.randint(10,50)/10,1))
    return list_score

def sum_video(path_video,path_saved_json_shot="./",path_saved_json_segment='./',path_result_segment_txt=None,id_shot="shot_gt",id_seg="seg_gt"):
    '''
        This function uses to summarize a video and export json files for visualization
        input: path_save - path of a input video_duration
               path_saved_json_shot - path to save json file for visualizing shots
               path_saved_json_segment -  path to save json file for visualizing segments
               path_result_segment_txt - path to save result file for  segments
               id_shot - id of shot json for visualizing
               id_seg - id of seg json for visualizing
        output: None
    '''
    #shot detection
    name_video,list_begin, list_ending = split_shots(path_video)
    # #cacl score
    list_score = calc_score(list_begin,list_ending) ##list score for BL

    if os.path.isdir(os.path.join(path_saved_json_segment,name_video)):
        print("Done shot and segment for video{}".format(name_video))
        return

    #create json to visual shots
    create_json4shots(path_saved_json_shot,name_video,list_begin,list_score, id_shot)

    #excuting knapsack to select the shots for summarize
    result = selection_shot_knapsack(list_begin,list_ending,list_score)
    create_json_selection(name_video,list_begin,list_ending,result,path_saved_json_segment,path_result_segment_txt,id_seg)
    print("Done shot and segment for video{}".format(name_video))

def sum_multi_video():
    paths = glob.glob(cfg.PATH_SUMME_VIDEOS+"/*.mp4")
    for p in paths:
        sum_video(p,cfg.PATH_JSON_SHOT_RANDOM_SUMME,cfg.PATH_JSON_SELECT_RANDOM_SUMME,cfg.PATH_TIME_SEG_RANDOM_SUMME,"shot_rd","seg_rd")


if __name__ == '__main__':
    #path_video = "src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video/sTEELN-vY30.mp4"
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('path_video', type=str,
                    help='path of input video')
    parser.add_argument('--jshot', type=str,
                    help='path to save json file for visualizing shots')
    parser.add_argument('--jseg', type=str,
                    help='path to save json file for visualizing segments')
    parser.add_argument('--fres', type=str,
                    help='path to save result file for segments')
    parser.add_argument('--shotid', type=str,
                    help='id for visualizing shots')
    parser.add_argument('--segid', type=str,
                    help='id for visualizing segments')
    args = parser.parse_args()
    sum_video(args.path_video,args.jshot,args.jseg,args.fres,args.shotid,args.segid)
