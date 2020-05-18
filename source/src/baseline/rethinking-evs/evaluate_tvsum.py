import os,sys,glob
sys.path.append("../../../../libs/rethinking-evs/")
from tools.summarizer import summarize
from tools.io import load_tvsum_mat
from joblib import Parallel, delayed
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import numpy as np
sys.path.append("../../../config")
from config import cfg
import json

def eval_random_summary(path_gt= '',path_label_predicted='', path_boundaries='',sum_len=.15, use_sum=False):
    #************************************************************************
    # Purpose: evaluation of KTS method for dataset TVSum
    # Inputs:
    # - path_gt: path ground truth of dataset TVSum
    # - path_label_predicted: path file ' .npy' of label 0/1 for each frame of each video
    # - path_boundaries: path file ' .npy' of boundaries
    # - sum_len: video length summary
    # - use_sum: True or False || True: sum scores all frames in segment || False: average scores all frames in segment
    # Output: The dictionary save the result of evaluation
    # Author: Trivl
    #************************************************************************
    # load dataset tvsum
    tvsum_data = load_tvsum_mat(path_gt)
    result = []
    p=[]
    r=[]
    f1=[]
    list_videos = []

    # evaluate each video
    for item in tvsum_data:
        user_anno = item['user_anno'].T
        n_fr = user_anno.shape[1]
        
        # get segment
        segment = np.load(path_boundaries+"/"+item['video']+".npy")
        
        # get 0/1 label for each frame from all user_annotation
        gs_summary = [summarize(x, segment, int(n_fr * sum_len), use_sum=use_sum) for x in user_anno]
        gs_summary = np.vstack(gs_summary)

        # get 0/1 label for each frame which was predicted
        rand_summary =  np.load(path_label_predicted+"/"+item['video']+".npy")

        # get precision , recall and f1 score
        score = [f1_score(x, rand_summary) for x in gs_summary]
        pre = [precision_score(x, rand_summary) for x in gs_summary]
        recall = [recall_score(x, rand_summary,) for x in gs_summary]
        f1_min = min(score)
        f1_mean = sum(score) / len(score)
        f1_max = max(score)
        f1.append(f1_mean)
        p.append(sum(pre)/len(pre))
        r.append(sum(recall)/len(recall))
        result.append((f1_min, f1_mean, f1_max))
        if item['video'] not in list_videos:
            list_videos.append(item['video'])

    # save the evaluation as json
    data_json= {}
    json_tvsum = {}
    for i in range(len(list_videos)):
         temp = {}
         temp["pre"] = "{:.2f}".format(p[i])
         temp["rc"] = "{:.2f}".format(r[i])
         temp["f1"] = "{:.2f}".format(float(f1[i]))
         data_json[list_videos[i]] = temp
    temp = {}
    temp["pre"] = "{:.2f}".format(float(sum(p)/len(p)))
    temp["rc"] = "{:.2f}".format(float(sum(r)/len(r)))
    temp["f1"] = "{:.2f}".format(float(sum(f1)/len(f1)))
    data_json["mean"] = temp
    json_tvsum["result"] = data_json
    json_tvsum["thres"] = 0.5
    print (json_tvsum)
#    with open('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/evaluation/TVSum/Two-Peak_VASNet_Knapsack/Two-Peak_VASNet_Knapsack.json', 'w') as f:
#        json.dump(json_tvsum, f)

if __name__=='__main__':
    eval_random_summary(path_gt = cfg.PATH_GT_TVSUM50,path_label_predicted="/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/label/tvsum_kts_vasnet_knapsack",path_boundaries= "/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/boundaries/TVSum/KTS",sum_len=.15, use_sum=False)

