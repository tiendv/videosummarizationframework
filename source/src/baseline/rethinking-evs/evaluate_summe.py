import os,sys,glob
sys.path.append("../../../../libs/rethinking-evs/")
from tools.summarizer import summarize
from tools.io import load_summe_mat
from joblib import Parallel, delayed
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import numpy as np
sys.path.append("../../../config")
from config import cfg

def get_summe_gssummary(path_gt):
    summe_data = load_summe_mat(path_gt)
    
    gold_standard = []
    for item in summe_data:
        user_anno = item['user_anno']
        user_anno = user_anno.T
        user_anno = user_anno.astype(np.bool)
        
        gold_standard.append(
            {
                'gs_summary': user_anno,
                'video': item['video'],
                'length' : item['length'][0][0],
                'nframes' : item['nframes'][0][0]
            }
        )
        
    return gold_standard

def eval_random_summary(path_gt='',path_label_predicted='',sum_len=.15):
    #************************************************************************
    # Purpose: evaluation of KTS method for dataset SumMe
    # Inputs:
    # - path_gt: path ground truth of dataset SumMe
    # - path_label_predicted: path file ' .npy' of label 0/1 for each frame of each video
    # - sum_len: video length summary
    # Output: The dictionary save the result of evaluation
    # Author: Trivl
    #************************************************************************
    # load dataset summe
    gt_summary = get_summe_gssummary(path_gt)
    result = []
    p=[]
    r=[]
    f1=[]
    list_videos = []

    # evaluate each video
    for item in gt_summary:
        # get 0/1 label for each frame from all user_annotation
        gs_summary = item['gs_summary']
        n_fr = gs_summary.shape[1]

        # get 0/1 label for each frame which was predicted
        rand_summary = np.load(path_label_predicted+"/"+item['video']+".npy")

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
    json_summe = {}
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
    json_summe["result"] = data_json
    json_summe["thres"] = 0.5
    print (json_summe)

if __name__=='__main__':
    eval_random_summary(path_gt=cfg.PATH_GT_SUMME,path_label_predicted=cfg.PATH_LABEL_PREDICTED,sum_len=.15)
