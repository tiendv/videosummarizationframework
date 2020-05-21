import os, json
from src.baseline.segmentation.create_shot_json import create_json4shots,create_json4shots_file
from src.baseline.selection.get_data_selection import create_json_selections

def create_shot_json(json_path, vid_name,begin_list,score_list=None,json_id="shot_gt"):
    create_json4shots(json_path, vid_name,begin_list,score_list,json_id)
    print("The result file is saved at " + json_path + "/"+vid_name)

def create_shot_json_from_file(file_path,json_path,vid_name,json_id="shot_gt"):
    create_json4shots_file(file_path,json_path,vid_name,json_id)

def write_eval_result(eval_dir_path,method,vid_names,precisions,recalls,fscores):
    result = {'result': {}, 'thres': 0.5}

    for i in range(len(vid_names)):
        d = {}
        d['pre']  = round(precisions[i],2)
        d['rc'] = round(recalls[i],2)
        d['f1'] = round(fscores[i],2)
        result['result'][vid_names[i]] = d
    d = {}
    d['pre']  = round(sum(precisions)/len(precisions),2)
    d['rc'] = round(sum(recalls)/len(recalls),2)
    d['f1'] = round(sum(fscores)/len(fscores),2)
    result['result']['mean'] = d

    if not os.path.isdir(os.path.join(eval_dir_path,method)):
        os.makedirs(os.path.join(eval_dir_path,method))
    save_path = os.path.join(eval_dir_path,"{n}/{n}.json".format(n=method))
    with open(save_path,'w') as f:
        json.dump(result,f)
    print("The result file is saved at {}".format(save_path))
