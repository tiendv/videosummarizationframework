import numpy as np
import json, os, glob
from sklearn.metrics import f1_score, precision_score, recall_score

def evaluate_baseline(path_bl, path_gt):
    # data_gt = json.load(path_gt)
    with open(path_gt,'r') as f:
        data_gt = json.load(f)
    with open(path_bl,'r') as f:
        data_bl = json.load(f)

    name_vid = os.path.basename(path_bl).split(".")[0]
    len_shots = data_bl["localisation"][0]["tclevel"]

    #get data shots
    data_shots_gt = data_gt["localisation"][0]["sublocalisations"]["localisation"]
    data_shots_bl = data_bl["localisation"][0]["sublocalisations"]["localisation"]

    y_true = np.zeros(len_shots)
    y_pred = np.zeros(len_shots)

    #set 1 for shots selected
    for d_gt in data_shots_gt:
        y_true[d_gt["tclevel"]]=1
    for d_bl in data_shots_bl:
        y_pred[d_bl["tclevel"]]=1

    f1 = f1_score(y_true, y_pred)
    pr = precision_score(y_true, y_pred)
    rc = recall_score(y_true, y_pred)

    return name_vid,pr,rc,f1
def write_evaluated_result(name,pr,rc,f1,path_evaluate_dir):
    if not os.path.isdir(path_evaluate_dir):
        os.makedirs(path_evaluate_dir)
    path_save = os.path.join(path_evaluate_dir,"{}.json".format(name))

    data =  {"precision":round(pr,2), "recall":round(rc,2), "fscore":round(f1,2)}
    with open(path_save,'w+') as f:
        json.dump(data,f)
    print("The result file is saved at {}".format(path_save))
if __name__ == '__main__':
    for path, subdirs, files in os.walk("../visualization/static/json/TVSum/selected/BL"):
        for name in files:
            print(os.path.join(path,name))
            path_bl = os.path.join(path,name)
            path_gt = path_bl.replace("BL","GT")
            try:
                name_vid,pr,rc, f1 = evaluate_baseline(path_bl,path_gt)
                write_evaluated_result(name_vid,pr,rc,f1,"../visualization/static/evaluation/{}/".format(name_vid))
            except Exception as e:
                break
