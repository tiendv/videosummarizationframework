#!/usr/bin/env python
# coding: utf-8

import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/deep_semantic_feature/")
from deep_semantic_feature import run_dsf
from config import cfg


def dsf(vid_id,seg_l,feat_type,datatype):
    #************************************************************************
    # Purpose: select shots from shots of a bbc video base on feature and sub-networks
    # Inputs:
    # - vid_id: id of the bbc video
    # - seg_l: segment length (uniform segment - Ex: 4 or 5 seconds ...)
    # - feat_type: vgg or smt_feat (smt_feat: using pretrained model || vgg: not using pretrained model)
    # - datatype: bbc or tvsum or summe (get video_name for bbc dataset)
    # Output: the result time selection for summarization will be store in path_save
    # Author: Trivl
    #************************************************************************
    try:
        os.system("echo test > {}/test.txt".format(cfg.PATH_DSF_BBC))
        os.remove("{}/test.txt".format(cfg.PATH_DSF_BBC))
    except Exception as e:
        raise "permission deny to write in {}".format(cfg.PATH_DSF_BBC)
    
    # video_name of bbc_dataset
    if datatype == "bbc":
        with open(os.path.join(cfg.BBC_SHOT_PATH,"video{}.txt".format(vid_id)),'r') as f:
            data = f.readlines()
        for video_name in data:
            video_name = (video_name.rstrip()).replace(".mp4","")
            run_dsf(cfg.PATH_DSF_BBC,cfg.VIDEO_CSV_BBC_PATH,datatype,cfg.PATH_FEATURE_VGG19_BBC,seg_l,feat_type,video_name)
            os.system("echo video{} >> {}/log_dsf.txt".format(vid_id,cfg.LOG_DIR_PATH))
    
    # Tvsum and SumMe
    else:
        data = pandas.read_csv(os.path.join(cfg.VIDEO_CSV_TVSUM_PATH),header=None)
        for i in range(1,data.shape[0]):
            vid_id = (data[0][i]).replace(".mp4","")
            run_dsf(cfg.PATH_DSF_RESNET50_TVSUM,cfg.VIDEO_CSV_TVSUM_PATH,datatype,cfg.PATH_FEATURE_RESNET50_TVSUM,seg_l,feat_type,vid_id)
            os.system("echo {} >> {}/log_dsf.txt".format(vid_id,cfg.LOG_DIR_PATH))

def main():
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('st', type=int, help='ID of start video')
    parser.add_argument('en', type=int, help='ID of end video')
    parser.add_argument('seg_l', type=int, help='Length shot')
    parser.add_argument('feat_type', type=str, help='Feat_type: vgg or smt_feat')
    parser.add_argument('datatype', type=str, help='Dataset: summe or tvsum or bbc')
    args = parser.parse_args()

    if args.datatype =="bbc":
        for i in range(args.st,args.en+1):
            dsf(i,args.seg_l,args.feat_type,args.datatype)
    else:
        dsf("",args.seg_l,args.feat_type,args.datatype)

if __name__ == "__main__":
    main()
    # python dsf.py 0 244 4 smt_feat bbc || python dsf.py 1 1 2 vgg tvsum || python dsf.py 1 1 5 vgg summe
    # or 
    # run_dsf(path_save,path_video,datatype,path_npy,path_reference,seg_l,feat_type,video_name)

