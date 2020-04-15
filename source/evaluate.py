import os
import json
from utilities.convert_time import time2sec
from config.config import cfg

def compute_shot_iou(gt_shot,pd_shot):
    x_gt = time2sec(gt_shot['tcin'])
    y_gt = time2sec(gt_shot['tcout'])

    x_pd = time2sec(pd_shot['tcin'])
    y_pd = time2sec(pd_shot['tcout'])

    latest_start = max(x_gt,x_pd)
    earliest_end = min(y_gt,y_pd)

    earliest_start = min(x_gt,x_pd)
    latest_end = max(y_gt,y_pd)
    inter = max(earliest_end-latest_start,0)
    union = latest_end - earliest_start
    return round(inter/union,2)

def evaluate(gt_path,pd_path,thres=0.5):
    with open(gt_path,'r') as f:
        gt_data = json.load(f)
    with open(pd_path,'r') as f:
        pd_data = json.load(f)

    name_vid = os.path.basename(pd_path).split(".")[0]
    # len_shots = data_bl["localisation"][0]["tclevel"]

    #get data shots
    gt_shot_data = gt_data["localisation"][0]["sublocalisations"]["localisation"]
    pd_shot_data = pd_data["localisation"][0]["sublocalisations"]["localisation"]

    i = 0
    j = 0
    correct_cnt = 0
    while i < len(pd_shot_data):
        j=0
        while (j < len(gt_shot_data)) and (time2sec(pd_shot_data[i]['tcout']) > time2sec(gt_shot_data[j]['tcin'])):
            if compute_shot_iou(pd_shot_data[i],gt_shot_data[j]) >= thres:
                correct_cnt = correct_cnt + 1
                break
            j = j + 1
        i = i + 1

    precision = correct_cnt/len(pd_shot_data)
    recall = correct_cnt/len(gt_shot_data)
    if precision+recall:
        fscore = (2*precision*recall)/(precision+recall)
    else:
        fscore=0
    return name_vid,precision,recall,fscore

def evaluateAllDS(eval_dir_path,gt_path,pd_path,thres=0.5):
    result = {'result': {}, 'thres': thres}
    vid_names = os.listdir(gt_path)
    vid_names.sort()
    pres = []
    rcs = []
    f1s = []

    for n in vid_names:
        gt_json_path = os.path.join(gt_path,"{n}/{n}.json".format(n=n))
        pd_json_path = os.path.join(pd_path,"{n}/{n}.json".format(n=n))
        if os.path.isfile(pd_json_path):
            _,pre,rc,f1 = evaluate(gt_json_path,pd_json_path,thres)

            d = {}
            d['pre']  = round(pre,2)
            d['rc'] = round(rc,2)
            d['f1'] = round(f1,2)
            pres.append(round(pre,2))
            rcs.append(round(rc,2))
            f1s.append(round(f1,2))
            result['result'][n] = d
    d = {}
    d['pre']  = round(sum(pres)/len(pres),2)
    d['rc'] = round(sum(rcs)/len(rcs),2)
    d['f1'] = round(sum(f1s)/len(f1s),2)
    result['result']['mean'] = d

    method = pd_path.split("/")[-1]

    if not os.path.isdir(os.path.join(eval_dir_path,method)):
        os.makedirs(os.path.join(eval_dir_path,method))
    save_path = os.path.join(eval_dir_path,"{n}/{n}.json".format(n=method))
    with open(save_path,'w') as f:
        json.dump(result,f)
    print("The result file is saved at {}".format(save_path))


def write_evaluated_result(name,pr,rc,f1,path_evaluate_dir):
    if not os.path.isdir(path_evaluate_dir):
        os.makedirs(path_evaluate_dir)
    path_save = os.path.join(path_evaluate_dir,"{}.json".format(name))

    data =  {"precision":round(pr,2), "recall":round(rc,2), "fscore":round(f1,2)}
    with open(path_save,'w+') as f:
        json.dump(data,f)
    print("The result file is saved at {}".format(path_save))

if __name__ == '__main__':
    # name,pr,rc,f1 = evaluate(os.path.join(cfg.PATH_JSON_SELECT_GT,'EE-bNr36nyA/EE-bNr36nyA.json'),os.path.join(cfg.PATH_JSON_SELECT_BL,'EE-bNr36nyA/EE-bNr36nyA.json'))
    # write_evaluated_result(name,pr,rc,f1,os.path.join(cfg.PATH_JSON_EVALUATE,name))
    evaluateAllDS(cfg.PATH_EVALUATE_TVSUM,cfg.PATH_JSON_SELECT_GT,cfg.PATH_JSON_SELECT_BL)
