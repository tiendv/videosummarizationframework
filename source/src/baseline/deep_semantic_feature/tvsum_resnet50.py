import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/deep_semantic_feature/")
from tvsum_lib import run_vsum_dsf
from config import cfg


if __name__ == "__main__":
    #************************************************************************
    # Purpose: select shots from dataset tvsum base on feature vgg
    # Inputs:
    # Output: the result time selection for summarization will be store in path_save_txt
    # Author: Trivlm
    #************************************************************************
    ### config this code
    path_save_txt = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/time_shots_tvsum50/res_net50"
    path_video = "/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video"
    datatype= 'summe'  ###tvsum or summe or bbc
    path_npy = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/time_shots_tvsum50/feature/resnet50'
    seg_l = 5
    feat_type = 'vgg'    # vgg
    ###
    run_vsum_dsf(path_save_txt,path_video,datatype,path_npy,seg_l,feat_type):


