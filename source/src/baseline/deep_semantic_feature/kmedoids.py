#!/usr/bin/env python
# coding: utf-8

import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/deep_semantic_feature/")
from bbc_kmedoids_lib import run_kmedoids
from bbc_kmedoids_lib import write_data
from bbc_kmedoids_lib import create_feature
from joblib import Parallel, delayed
from config import cfg

def run_bbc_kmedoids(vid_id,k):
    #************************************************************************
    # Purpose: select shots from shots of a bbc video base on emotion or event
    # Inputs:
    # - vid_id: id of the bbc video
    # - k: Value K in K-medoids
    # Output: the result time selection for summarization will be store in path_save
    # Author: Trivlm
    #************************************************************************
    #Check permission
    try:
        os.system("echo test > {}/test.txt".format(cfg.PATH_EVENT_KMEDOIDS_BBC))
        os.remove("{}/test.txt".format(cfg.PATH_EVENT_KMEDOIDS_BBC))
    except Exception as e:
        raise "permission deny to write in {}".format(cfg.PATH_EVENT_KMEDOIDS_BBC)
    with open(os.path.join("/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/test","video{}.txt".format(vid_id)),'r') as f:
        data = f.readlines()
    for video_name in data:
        video_name = video_name.rstrip()
    print(video_name)
    feature,total_time = create_feature(cfg.OUTPUT_PATH,cfg.PATH_DATA_REF_BBC_FILE,"video"+str(vid_id))
    selected = run_kmedoids(feature,k,vid_id,total_time)
    write_data(selected,cfg.PATH_EVENT_KMEDOIDS_BBC,cfg.PATH_DATA_REF_BBC_FILE,video_name)
    os.system("echo video{} >> {}/events_kmedoids.txt".format(vid_id,cfg.LOG_DIR_PATH))


def main():
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('st', type=int, help='ID of start video')
    parser.add_argument('en', type=int, help='ID of end video')
    parser.add_argument('--k', type=int, help='Value K in K-medoids')

    args = parser.parse_args()
#    for i in range(args.st,args.en+1):
#        run_bbc_kmedoids(i,args.k)
    Parallel(n_jobs=-1)( [delayed(run_bbc_kmedoids)(i,args.k) for i in range(args.st,args.en+1)] )


if __name__ == "__main__":
    main()
    # python kmedoids.py start end seg_l || EX: python kmedoids.py 0 243 10
    # or
    # run_kmedoids(path_save,path_video,path_csv,path_reference,seg_l,vid_id=0) replace  main() line 42

