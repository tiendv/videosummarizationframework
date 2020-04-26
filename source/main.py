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
from UIT.mmlab.vsum.segment import segment_shot
from UIT.mmlab.vsum.selection import select_shot
from UIT.mmlab.vsum.scoring import score_shot
from UIT.mmlab.vsum.visualization import create_json


def sum_video(path_video,path_saved_json_shot="./",path_saved_json_segment='./',path_result_segment_txt="./",id_shot="shot_gt",id_seg="seg_gt"):
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
    video_name, begin_list, end_list = segment_shot.doTrainsnet(path_video)

    # #cacl score
    score_list = score_shot.random_score(begin_list) ##list score for BL

    #create json to visual shots
    create_json.create_shot_json(shot_json_path,video_name,begin_list,score_list, shot_id)

    #excuting knapsack to select the shots for summarize
    select_shot.doKnapsack(video_name,begin_list, end_list,score_list,path_result_segment_txt)

def sum_multi_video():
    paths = glob.glob(cfg.PATH_SUMME_VIDEOS+"/*.mp4")
    for p in paths:
        sum_video(p,cfg.PATH_JSON_SHOT_RANDOM_SUMME,cfg.PATH_JSON_SELECT_RANDOM_SUMME,cfg.PATH_TIME_SEG_RANDOM_SUMME,"shot_rd","seg_rd")

def main():
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

if __name__ == '__main__':
    # main()
    path_video = "src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video/sTEELN-vY30.mp4"
    sum_video(path_video)
