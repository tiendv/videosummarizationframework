import numpy as np
import numpy as np, h5py
from itertools import groupby
import datetime
import time
import cv2
import os,sys,glob
import pandas as pd
from config.config import cfg
from utilities.convert_time import sec2time
import scipy.io
import tables

def create_txt_gt_summe(path_summe,path_save):
    paths = glob.glob(path_summe + "/*.mat")
    for path_matlab in paths:
        time_shot = []
        score_shot = []

        f = scipy.io.loadmat(path_matlab)
        name_video = (path_matlab.split("/")[-1]).split(".")[0]
        print(name_video)
        #print(f['FPS'][0][0])
        #print(f['video_duration'][0][0])
        #print(f['nFrames'][0][0])
        #print(f['gt_score'].shape)

        second_per_frame = f['video_duration'][0][0]/f['nFrames'][0][0]

        # get length frames per shot
        time_shot = np.array([len(list(group)) for key, group in groupby(f["gt_score"])])*second_per_frame


        # create list ground truth score parallel list_shot
        score_shot = np.array([k for k, g in groupby(f["gt_score"], key=lambda x: x)])
        dir_save = os.path.join(path_save,name_video)

        if not os.path.isdir(dir_save):
            os.makedirs(dir_save)
        with open(os.path.join(dir_save,name_video+".txt"),"w") as f:
            time = 0
            for i in range(len(time_shot)):
                f.write(str(sec2time(time))+" "+str(sec2time(time+time_shot[i]))+" "+str(score_shot[i][0]*5)+"\n")
                time += time_shot[i]
        
       
if __name__ == '__main__':
    create_txt_gt_summe("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/SumMe/GT","/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_shots_summe/GT")
