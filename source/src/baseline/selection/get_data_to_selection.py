import os , sys
from config.config import cfg
from utilities.convert_time import time2sec
from utilities.knapsack_ortool import knapsackGG
import knapsack
import json
import glob
import numpy as np


data_json = {
                "localisation": [
                    {
                        "sublocalisations": {
                            "localisation": []
                        },
                        "type": "keyframes",
                        "tcin": "00:00:00.0000",
                        "tcout": "00:00:15.0000",
                        "tclevel": "0"
                    }
                ],
                "id": "kf-amalia01",
                "type": "keyframes",
                "algorithm": "demo-video-generator",
                "processor": "mmlab",
                "processed": "1421141589291",
                "version": "1"
            }

def get_data_from_time_shot_file(path_data):
    list_begin = []
    list_ending = []
    scores = []
    name_vid = os.path.basename(path_data).split(".")[0]
    with open(path_data,'r') as f:
        for line in f:
            line = line.split()
            list_begin.append(line[0])
            list_ending.append(line[1])
            scores.append(round(float(line[-1]),2))
    return name_vid,list_begin,list_ending,scores

def get_data_to_selection(list_begin,list_ending):
    shot_durations = []
    video_duration=0
    for i in range(len(list_begin)):
        shot_durations.append(round(time2sec(list_ending[i])-time2sec(list_begin[i]),2))
        video_duration = round(time2sec(list_ending[i]),2)
    return shot_durations, video_duration

def selection_shot_knapsack_file(path_data,L=0.15):
    _,begin_list,end_list,score_list = get_data_from_time_shot_file(path_data)
    shot_durations, video_duration = get_data_to_selection(begin_list,end_list)
    # print(video_duration*L)
    result = knapsack.knapsack(shot_durations,scores).solve(round(video_duration*L,2))
    #result is a tuple (max of sum score, sum durarion less than sum_video )
    return result

def selection_shot_knapsack(list_begin,list_ending,list_score,L=0.15):
    pad = 100
    shot_durations, video_duration = get_data_to_selection(list_begin,list_ending)

    shot_durations = np.array(shot_durations)*pad
    shot_durations = shot_durations.astype('int')
    list_score = np.array(list_score)*pad
    list_score = list_score.astype('int')


    shot_durations = np.expand_dims(shot_durations, axis=0)
    dur,result = knapsackGG(shot_durations.tolist(),list_score.tolist(),[int(video_duration*L*pad)])

    # result = knapsack.knapsack(shot_durations,list_score).solve(int(video_duration*L*pad))[1]
    #result is a tuple (max of sum score, index of shot having sum durarion less than sum_video )
    return result


def create_json_selection_file(path_data, path_json='',id="seg_GT"):
    with open(path_data,'r') as f:
        data = f.readlines()
    dicts_data = []
    for d in data:
	    dict_data = {}
	    dict_data["tcin"] = d.split()[0]
	    dict_data["tcout"] = d.split()[1]
	    dict_data["tclevel"] = 1
	    dicts_data.append(dict_data)

    name_vid =  path_data.split("/")[-1]
    name_file = name_vid.split(".")[0]
    name_vid =  path_data.split("/")[-2]
    create_json_selection(name_file,list_begin,list_ending,result,path_json,id)

def create_json_selection(name_vid, list_begin,list_ending,result_selection=None, path_json='./',id = 'seg_GT'):
    '''
        This function uses to create a json for vusializing the selection
        input: name_vid - name of the input video
               list_begin - list the begining time of each shot
               list_ending - list the ending time of each shot
               result_selection - the output after using knapsack for selection. (None if not have)
               path_json - the path of json file being saved
        output: None
    '''

    dicts_data = []
    if result_selection:
	    for i in result_selection:
		    dict_data = {}
		    dict_data["tcin"] = list_begin[i]
		    dict_data["tcout"] = list_ending[i]
		    dict_data["tclevel"] = i
		    dicts_data.append(dict_data)
    else:
	    for i in range(len(list_begin)):
		    dict_data = {}
		    dict_data["tcin"] = list_begin[i]
		    dict_data["tcout"] = list_ending[i]
		    dict_data["tclevel"] = 1
		    dicts_data.append(dict_data)

    data_json["localisation"][0]["sublocalisations"]["localisation"] = dicts_data
    data_json["id"] = id
    data_json["type"] = "segments"
    data_json["localisation"][0]["tclevel"]= len(list_begin)
    path_save = os.path.join(path_json,name_vid)
    if not os.path.isdir(path_save):
          os.makedirs(path_save)

    with open(os.path.join(path_save,"{}.json".format(name_vid)),'w+') as f:
        json.dump(data_json, f)
    print("The json file is saved at {}".format(os.path.join(path_save,"{}.json".format(name_vid))))

if __name__ == '__main__':

    for path, subdirs, files in os.walk(cfg.PATH_TIME_SHOTS_VSUM_DSF_SUMME):
        for name in files:
            with open(os.path.join(path,name)) as f:
                lines = list(f)
                list_begin = []
                list_ending = []
                name_vid = name.split(".txt")[0]
                for line in lines :
                    list_begin.append(line.split(" ")[0])
                    list_ending.append(line.split(" ")[1])
            create_json_selection_file( name_vid, list_begin,list_ending,path_json=cfg.PATH_JSON_SHOT_SUM_DSF_SUMME,id="seg_vsum_dsf")
