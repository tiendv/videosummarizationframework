#!/usr/bin/env python
# coding: utf-8
import os,sys,glob
sys.path.append("../../../../libs/rethinking-evs/")
from tools.summarizer import summarize
from tools.io import load_summe_mat
from tools.io import load_tvsum_mat
from tools.segmentation import get_segment
import pandas as pd
from sklearn.metrics import f1_score
import numpy as np
import json
from joblib import Parallel, delayed
import pandas
import argparse
sys.path.append("../../../config")
from config import cfg
from random_method_lib import run_random_methods

def run_methods(vid_id,method):
    #************************************************************************
    # Purpose: select shots for video base on random method
    # Inputs:
    # - vid_id: id of the bbc video
    # - method: Methods: one-peak || two-peak || KTS || randomized-KTS || uniform
    # Output: the result time selection for summarization will be stored
    # Author: Trivl
    #************************************************************************
    try:
        os.system("echo test > {}/test.txt".format(cfg.PATH_DSF_BBC))
        os.remove("{}/test.txt".format(cfg.PATH_DSF_BBC))
    except Exception as e:
        raise "permission deny to write in {}".format(cfg.PATH_DSF_BBC)
    
    # video_name of bbc_dataset
    if vid_id != "":
        with open(os.path.join(cfg.INPUT_VIDEO_LIST_BBC,"video{}.txt".format(vid_id)),'r') as f:
            data = f.readlines()
        for video_name in data:
            video_name = (video_name.rstrip()).replace(".mp4","")
            boundaries = []
            if method == "KTS" or method ==  "randomized-KTS":
                boundaries = np.load(os.path.join(cfg.BOUNDARIES_BBC,vid_id+".npy"))
            run_random_methods(cfg.ONE-PEAK_BBC,cfg.VIDEO_CSV_BBC_PATH,video_name,boundaries,path_score="",method=method)
            os.system("echo video{} >> {}/log_random_method.txt".format(vid_id,cfg.LOG_DIR_PATH))
    else:
        data = pandas.read_csv(os.path.join(cfg.VIDEO_CSV_SUMME_PATH),header=None)
        for i in range(1,data.shape[0]):
            vid_id = (data[0][i]).replace(".mp4","")
            boundaries = []
            #if method == "KTS" or method ==  "randomized-KTS":
            boundaries = np.load(os.path.join("/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/boundaries/SumMe/Uniform",vid_id+".npy"))
            run_random_methods("",cfg.VIDEO_CSV_SUMME_PATH,vid_id,boundaries,path_score="/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/data/vsumm-reinforce",method=method)
    
    # Tvsum and SumMe
    """
    else:
        data = pandas.read_csv(os.path.join(cfg.VIDEO_CSV_TVSUM_PATH),header=None)
        for i in range(1,data.shape[0]):
            vid_id = (data[0][i]).replace(".mp4","")
            boundaries = []
            #if method == "KTS" or method == "randomized-KTS":
            boundaries = np.load(os.path.join("/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/boundaries/TVSum/randomized-KTS",vid_id+".npy"))
            run_random_methods("",cfg.VIDEO_CSV_TVSUM_PATH,vid_id,boundaries,path_score="/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/data/VASNet",method=method)
#            os.system("echo {} >> {}/log_random_method.txt".format(vid_id,cfg.LOG_DIR_PATH))
    """


def main():
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('--st', type=int, help='ID of start video')
    parser.add_argument('--en', type=int, help='ID of end video')
    parser.add_argument('method', type=str, help='Methods: one-peak || two-peak || KTS || randomized-KTS || uniform')
    args = parser.parse_args()

    if args.st and args.en:
        for i in range(args.st,args.en+1):
            run_methods(i,args.method)
    else:
        run_methods("",args.method)

if __name__ == "__main__":
    main()
    # python random_method.py 0 243 one-peak bbc || python random_method.py uniform || python random_method.py two-peak
    # or 
    # run_dsf(path_save,path_video,datatype,path_npy,path_reference,seg_l,feat_type,video_name)

