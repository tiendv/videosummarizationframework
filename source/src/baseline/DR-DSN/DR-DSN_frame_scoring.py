import os,sys,glob
sys.path.append("../../../../libs/DR_DSN/")
from DR_DSN_frame_scoring_lib import *
sys.path.append("../../../config")
from config import cfg


if __name__ == '__main__':
    #************************************************************************
    # Purpose: frame scoring (unsupervised video summarization with REINFORCE)
    # Inputs:
    # - path_pretrained_model: path pretrained model
    # - path_feature: path feature extraction of video(' .npy' with shape: x,1024 (GoogLeNet)) 
    # Output: Score
    # Author: Trivl
    #************************************************************************

    path_pretrained_model = cfg.PATH_DRDSN_PRETRAINED_MODEL
    path_feature = cfg.PATH_FEATURE_GOOGLENET
    from os import walk
    f = []
    for (dirpath, dirnames, filenames) in walk(path_feature):
        f.extend(filenames)
        break
    for i in f:
        feature =  np.load(os.path.join(path_feature,i))
        score = get_DR_DSN_frame_scoring(feature,path_pretrained_model=path_pretrained_model)

