import os , sys
from config.config import cfg
from utilities.convert_time import time2sec
import knapsack
import json


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

def get_data_to_selection_file(path_data):
    shot_durations = []
    scores = []
    with open(path_data,'r') as f:
        for line in f:
            line = line.split()
            shot_durations.append(round(time2sec(line[1])-time2sec(line[0]),4))
            scores.append(float(line[-1]))
            video_duration = round(time2sec(line[1]),4)
    return shot_durations,scores, video_duration

def get_data_to_selection(list_begin,list_ending):
    shot_durations = []
    for i in range(len(list_begin)):
        shot_durations.append(round(time2sec(list_ending[i])-time2sec(list_begin[i]),4))
        video_duration = round(time2sec(list_ending[i]),4)
    return shot_durations, video_duration

def selection_shot_knapsack_file(path_data,L=0.15):
    shot_durations,scores, video_duration = get_data_to_selection_file(path_data)
    print(video_duration*L)
    result = knapsack.knapsack(shot_durations,scores).solve(video_duration*L)
    #result is a tuple (max of sum score, sum durarion less than sum_video )
    return result

def selection_shot_knapsack(list_begin,list_ending,list_score,L=0.15):
    shot_durations, video_duration = get_data_to_selection(list_begin,list_ending)
    print(video_duration*L)
    result = knapsack.knapsack(shot_durations,list_score).solve(video_duration*L)
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
    data_json["localisation"][0]["sublocalisations"]["localisation"] = dicts_data
    data_json["id"] = id
    data_json["type"] = "segments"
    path_save = os.path.join(path_json,name_vid)
    if not os.path.isdir(path_save):
          os.makedirs(path_save)
    with open(os.path.join(path_save,"{}.json".format(name_file)),'w+') as f:
        json.dump(data_json, f)
    print("the json file is saved at {}".format(os.path.join(path_save,"{}.json".format(name_file))))

def create_json_selection(name_vid, list_begin,list_ending,result_selection=None, path_json='./',id = 'shot_GT'):
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
	    for i in result_selection[1]:
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
    for path, subdirs, files in os.walk(cfg.PATH_TIME_SHOTS_BBC):
        for name in files:
            create_json_selection(path_data=os.path.join(path,name),result_selection=None ,path_json=cfg.PATH_JSON_SELECT_BBC)
