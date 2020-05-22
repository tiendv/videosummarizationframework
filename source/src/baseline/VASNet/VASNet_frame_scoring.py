import os,sys,glob
sys.path.append("../../../../libs/VASNet/")
from VASNet_frame_scoring_lib import *
sys.path.append("../../../config")
from config import *


if __name__ == '__main__':
    #************************************************************************
    # Purpose: frame scoring (Summarizing Videos with Attention)
    # Inputs:
    # - path_pretrained_model: path pretrained model
    # - path_feature: path feature extraction of video(' .npy' with shape: x,1024 (GoogLeNet)) 
    # Output: Score
    # Author: Trivl
    #************************************************************************

    path_feature = "/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/data/feature/googlenet_summe"
    path_pretrained_model="/mmlabstorage/workingspace/VideoSum/trivlm/VASNet/data/models/summe_aug_splits_0_0.5122454899922037.tar.pth"
    from os import walk
    f = []
    for (dirpath, dirnames, filenames) in walk(path_feature):
        f.extend(filenames)
        break
    for i in f:
        features =  np.load(os.path.join(path_feature,i))
        score = get_VASNet_score(features,path_pretrained_model=path_pretrained_model)
    sys.exit(0)

