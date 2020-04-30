#!/usr/bin/env python
# coding: utf-8

import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/deep_semantic_feature/")
from bbc_emotions_lib import run_vsum_dsf
from config import cfg


def main():
    #************************************************************************
    # Purpose: select shots from shots of a bbc video base on events
    # Inputs:
    # - vid_id: id of the bbc video
    # Output: the result time selection for summarization will be store in path_save_txt
    # Author: Trivlm
    #************************************************************************
    path_save_txt = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/time_shots_bbc/event_seg_vsum_dsf_fix"
    path_video = "/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/videos"
    datatype= 'bbc'  ###tvsum or summe or bbc
    path_npy = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/events_shot"
    path_reference = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/reference_bbc/master_shot_reference.txt"
    seg_l = 4
    feat_type = 'vgg'    # smt_feat (proposed) or vgg

    parser = argparse.ArgumentParser(description='Optional description "BBC start = 1 & end = 242"')
    parser.add_argument('start', type=int, help='ID of start video')
    parser.add_argument('end', type=int, help='ID of end video')
    args = parser.parse_args()

    list_name_video = []
    for i in range(args.start,args.end +1):
        name_video = "video"+str(i)
        list_name_video.append(name_video)
    run_vsum_dsf(path_save_txt,path_video,datatype,path_npy,path_reference,seg_l,feat_type,list_name_video)


if __name__ == "__main__":
    #python bbc_events.py 1 242
    main()

