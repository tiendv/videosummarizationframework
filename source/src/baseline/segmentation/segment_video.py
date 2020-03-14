import glob,os
import sys
import numpy as np
import numpy as np, h5py
from itertools import groupby
import datetime
import time
sys.path.append("../../../config")
sys.path.append("../../../utilities")

from config import cfg
from convert_time import sec2time

def create_segments_tvsum(path_gt_tvsum50):
    '''
    This function uses to extract time of each shot.
    input   : path_time_shot : path of dir save file (__name_video__).txt
              path_gt_tvsum50: path of dir content groundtruth tvsum50 .matlab
    output  :
    modified: 12/3/2020
    author  : Trivlm
    '''
    # read file .matlab
    f = h5py.File(path_gt_tvsum50,'r')
    ### read name of each video
    list_begin_seg= []
    list_end_seg = []
    list_score_seg = []
    data_name = f.get('tvsum50/video')
    list_name = []
    for i in range(data_name.shape[0]):
        name= ''.join(map(chr,f[data_name[i][0]]))
        list_name.append(name)

    # read length of each video
    length_video = f.get('tvsum50/length')
    list_length = []
    for i in range(length_video.shape[0]):
        length= f[length_video[i][0]][0][0]
        list_length.append(length)

    # read total frames of each video
    nframes = f.get('tvsum50/nframes')
    list_nframes = []
    for i in range(nframes.shape[0]):
        length= f[nframes[i][0]][0]
        list_nframes.append(length)

    # calculate time per frames of each video
    second_per_frame = []
    for i in range(data_name.shape[0]):
        second_per_frame.append(list_length[i]/list_nframes[i])

    # get ground truth score of each video
    gt_score = f.get('tvsum50/gt_score')
    list_gt_score = []
    gt_score_video = []
    for i in range(nframes.shape[0]):
        gt_score_video= f[gt_score[i][0]][0]
        list_gt_score.append(gt_score_video)

    # get length frames per shot
    list_shot = []
    for i in range(nframes.shape[0]):
        list_shot.append(np.array([len(list(group)) for key, group in groupby(list_gt_score[i])]))

    # create list ground truth score parallel list_shot
    list_gt = []
    for i in range(nframes.shape[0]):
        list_gt.append(np.array([k for k, g in groupby(list_gt_score[i], key=lambda x: x)]))

    #write file .txt
    for i in range(nframes.shape[0]):
        a=0
        temp = second_per_frame[i]*list_shot[i]
        #with open(os.path.join(path_time_shots,"{}/{}.txt".format(list_name[i],list_name[i])),"w") as f:
        list_begin_seg_temp= []
        list_end_seg_temp = []
        list_score_seg_temp = []
        for j in range(len(temp)):
            #f.write(str(sec2time(a))+ " " + str(sec2time(a+temp[j])) + " " +str(list_gt[i][j]) + "\n")
            list_begin_seg_temp.append(str(sec2time(a)))
            list_end_seg_temp.append(str(sec2time(a+temp[j])))
            list_score_seg_temp.append(list_gt[i][j])
            a += temp[j]
        list_begin_seg.append(list_begin_seg_temp)
        list_end_seg.append(list_end_seg_temp)
        list_score_seg.append(list_score_seg_temp)
    return list_name, list_begin_seg , list_end_seg , list_score_seg

def save_time_shots(name , begin , end ,score,path_time_shots):
    path_save = os.path.join(path_time_shots,"GT",name)
    if not os.path.isdir(path_save):
          os.makedirs(path_save)
    with open(os.path.join(path_save ,"{}.txt".format(name)),"w") as f:
        #print(os.path.join(path_save ,"{}.txt".format(name)))
        for i in range(len(begin)):
            f.write("{} {} {}\n".format(begin[i],end[i],score[i]))

def create_segment(path_gt_tvsum50,path_time_shots):
    names, begin , end ,score = create_segments_tvsum(path_gt_tvsum50)
    for i in range(len(names)) :
        save_time_shots(names[i] , begin[i] , end[i] ,score[i],path_time_shots)

if __name__ == '__main__':
    create_segment(cfg.PATH_GT_TVSUM50,cfg.PATH_TIME_SHOTS)
