#!/usr/bin/env python
# coding: utf-8

import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/deep_semantic_feature/")
from bbc_kmedoids_lib import run_kmedoids
from config import cfg

def run_bbc_kmedoids(vid_id,seg_l,feat_type):
    #************************************************************************
    # Purpose: select shots from shots of a bbc video base on emotion
    # Inputs:
    # - vid_id: id of the bbc video
    # Output: the result time selection for summarization will be store in path_save
    # Author: Trivlm
    #************************************************************************
    #Check permission
    try:
        os.system("echo test > {}/test.txt".format(path_save))
        os.remove("{}/test.txt".format(path_save))
    except Exception as e:
        raise "permission deny to write in {}".format(path_save)
    run_kmedoids(cdg.PATH_EMOTION_KMEDOIDS_BBC,cfg.PATH_VIDEO_BBC,cfg.PATH_EVENT_EMOTION_BBC,cfg.PATH_DATA_REF_BBC_FILE,seg_l,feat_type,vid_id)
    os.system("echo video{} >> {}/emotion_kmedoids.txt".format(vid_id,cfg.LOG_DIR_PATH))


def main():
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('st', type=int, help='ID of start video')
    parser.add_argument('en', type=int, help='ID of end video')
    parser.add_argument('seg_l', type=int, help='Length shot')
    parser.add_argument('feat_type', type=str, help='Feat_type: vgg or smt_feat')

    args = parser.parse_args()
    for i in range(args.st,args.en+1):
        run_bbc_kmedoids(i,args.seg_l,args.feat_type)


if __name__ == "__main__":
    main()
    # python bbc_emotions.py start end seg_l feat_type || EX: python bbc_kmedoids.py 0 243 4 vgg
    # or
    # run_kmedoids(path_save,path_video,path_csv,path_reference,seg_l,feat_type,vid_id=0) replace  main() line 42

