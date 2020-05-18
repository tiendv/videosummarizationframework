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
import json
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



def evaluate_summary(machine_summary, user_summary, eval_metric='avg'):
    """Compare machine summary with user summary (keyshot-based).
    Args:
    --------------------------------
    machine_summary and user_summary should be binary vectors of ndarray type.
    eval_metric = {'avg', 'max'}
    'avg' averages results of comparing multiple human summaries.
    'max' takes the maximum (best) out of multiple comparisons.
    """
    machine_summary = machine_summary.astype(np.float32)
    user_summary = user_summary.astype(np.float32)
    n_users,n_frames = user_summary.shape

    # binarization
    machine_summary[machine_summary > 0] = 1
    user_summary[user_summary > 0] = 1

    if len(machine_summary) > n_frames:
        machine_summary = machine_summary[:n_frames]
    elif len(machine_summary) < n_frames:
        zero_padding = np.zeros((n_frames - len(machine_summary)))
        machine_summary = np.concatenate([machine_summary, zero_padding])

    f_scores = []
    prec_arr = []
    rec_arr = []

    for user_idx in range(n_users):
        gt_summary = user_summary[user_idx,:]
        overlap_duration = (machine_summary * gt_summary).sum()
        precision = overlap_duration / (machine_summary.sum() + 1e-8)
        recall = overlap_duration / (gt_summary.sum() + 1e-8)
        if precision == 0 and recall == 0:
            f_score = 0.
        else:
            f_score = (2 * precision * recall) / (precision + recall)
        f_scores.append(f_score)
        prec_arr.append(precision)
        rec_arr.append(recall)

    if eval_metric == 'avg':
        final_f_score = np.mean(f_scores)
        final_prec = np.mean(prec_arr)
        final_rec = np.mean(rec_arr)
    elif eval_metric == 'max':
        final_f_score = np.max(f_scores)
        max_idx = np.argmax(f_scores)
        final_prec = prec_arr[max_idx]
        final_rec = rec_arr[max_idx]
    print (final_f_score, final_prec, final_rec)
    return final_f_score, final_prec, final_rec

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
#        f1.append(f1_mean)
#        p.append(sum(pre)/len(pre))
#        r.append(sum(recall)/len(recall))
        f1.append(np.max(score))
        max_idx = np.argmax(score)
        p.append(pre[max_idx])
        r.append(recall[max_idx])
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
#    with open('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/evaluation/SumMe/Randomized-KTS_DR-DSN_Knapsack/Randomized-KTS_DR-DSN_Knapsack.json', 'w') as f:
#        json.dump(json_summe, f)
if __name__=='__main__':
    eval_random_summary(path_gt=cfg.PATH_GT_SUMME,path_label_predicted="/mmlabstorage/workingspace/VideoSum/trivlm/rethinking-evs/label/summe_two-peak_vasnet_knapsack",sum_len=.15)
