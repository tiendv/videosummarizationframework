import cv2
import os,sys,glob
import random
import argparse
from multiprocessing import Process

from config.config import cfg
from uit.mmlab.vsum.segment import segment_shot
from uit.mmlab.vsum.selection import select_shot
from uit.mmlab.vsum.scoring import score_shot
from uit.mmlab.vsum.visualization import create_json


def sum_video(vid_path,saved_shot_json_path="./",saved_seg_json_path='./',result_seg_file_path="./",shot_id="shot_gt",seg_id="seg_gt"):
    '''
        This function uses to summarize a video and export json files for visualization
        input: vid_path - path of a input video
               saved_shot_json_path - path to save json file for visualizing shots
               saved_seg_json_path -  path to save json file for visualizing segments
               result_seg_file_path - path to save result file for  segments
               id_shot - id of shot json for visualizing
               id_seg - id of seg json for visualizing
        output: None
    '''
    #shot detection
    video_name, begin_list, end_list = segment_shot.do_trainsnet(vid_path)

    # #cacl score
    score_list = score_shot.random_score(begin_list) ##list score for BL

    #create json to visual shots
    create_json.create_shot_json(saved_shot_json_path,video_name,begin_list,score_list, shot_id)

    #excuting knapsack to select the shots for summarize
    select_shot.do_knapsack(video_name,begin_list, end_list,score_list,result_seg_file_path)

    #create json to visual segments
    create_json.create_shot_json_from_file(result_seg_file_path,saved_seg_json_path)

def sum_multi_video(videos_file_path):
    with open(videos_file_path,'r') as f:
        paths = f.readlines()
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
