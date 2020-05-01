#!/usr/bin/env python
# coding: utf-8

import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/detect_emotion/")
from config import cfg
import load_model_and_processing
from load_model_and_processing import detect_emotion

def main():
    #************************************************************************
    # Purpose: detect emotion from shots of a bbc video
    # Inputs:
    # - vid_id: id of the bbc video
    # Output: the result csv file stored in cfg.PATH_EMOTION_SHOT_BBC
    # Author: Trivlm
    #************************************************************************

    parser = argparse.ArgumentParser(description='Optional description "BBC start = 0 & end = 243"')
    parser.add_argument('start', type=int, help='ID of start video')
    parser.add_argument('end', type=int, help='ID of end video')
    args = parser.parse_args()

    list_name_video = []
    for i in range(args.start,args.end +1):
        vid_id = "video"+str(i)
        detect_emotion(cfg.PATH_FACES_SHOT_BBC,cfg.PATH_KF_SHOT_BBC,cfg.PATH_EMOTION_SHOT_BBC,vid_id)
        os.system("echo {} >> {}/logemotion.txt".format(vid_id,cfg.LOG_DIR_PATH))

if __name__ == '__main__':
    # CUDA_VISIBLE_DEVICES=1 python3 detect_emotion.py 0 243
    main()
