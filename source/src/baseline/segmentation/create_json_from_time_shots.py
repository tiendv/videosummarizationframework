import  json
import sys,os,glob
from config.config import cfg

data_json = {
                "localisation": [
                    {
                        "sublocalisations": {
                            "localisation": []
                        },
                        "type": "keyframes",
                        "tcin": "00:00:00.0000",
                        "tcout": "00:00:15.0000",
                        "tclevel": 0
                    }
                ],
                "id": "kf-amalia01",
                "type": "keyframes",
                "algorithm": "demo-video-generator",
                "processor": "",
                "processed": 1421141589291,
                "version": 1
            }

def create_json4shots_file(path_data,path_json,id="shot_gt"):
    '''
        This function uses to create a json file from text file for shots
        input: path_data - path of txt file including time of shot
               path_json - path of json being saved
               id(optional) = id of the json file (default="shot_gt")
        output: none
    '''
    dicts_data = []
    with open(path_data,'r') as f:
        for line in f:
            dict_data = {}
            line = line.split()
            dict_data["label"] = line[-1]
            dict_data["tc"] = line[0]
            dict_data["tclevel"] = 1
            dicts_data.append(dict_data)
    data_json["localisation"][0]["sublocalisations"]["localisation"] = dicts_data
    data_json["id"] = id
    data_json["type"] = "events"

    name_vid =  path_data.split("/")[-1]
    name_file = name_vid.split(".")[0]
    name_vid = path_data.split("/")[-2]
    path_save = os.path.join(path_json,name_vid)
    if not os.path.isdir(path_save):
          os.makedirs(path_save)
    with open(os.path.join(path_save,"{}.json".format(name_file)),'w+') as f:
        json.dump(data_json, f)

def create_json4shots(path_json, name_vid,list_begin,list_score=None,id="shot_gt", ):
    '''
        This function uses to create a json file from input data for shots
        input: name_vid - the name of the input video
               list_begin - list of time begining of each shot
               list_score - list of score of each shot, enter "None" if it hasn't had the scores
               id(optional) = id of the json file (default="shot_gt")
        output: none
    '''
    dicts_data = []
    for i in range(len(list_begin)):
        dict_data = {}
        if list_score:
            dict_data["label"] = list_score[i]
        else:
            dict_data["label"] = 1

        dict_data["tc"] = list_begin[i]
        dict_data["tclevel"] = 1
        dicts_data.append(dict_data)
    data_json["localisation"][0]["sublocalisations"]["localisation"] = dicts_data
    data_json["id"] = id
    data_json["type"] = "events"

    path_save = os.path.join(path_json,name_vid)
    if not os.path.isdir(path_save):
          os.makedirs(path_save)
    with open(os.path.join(path_save,"{}.json".format(name_vid)),'w+') as f:
        json.dump(data_json, f)



def create_multi_json(path_time_shots,path_json_shot):
    print(path_time_shots)
    for path, subdirs, files in os.walk(path_time_shots):
        for name in files:
            create_json4shots(os.path.join(path,name),path_json_shot)
if __name__ == '__main__':
    create_multi_json(cfg.PATH_TIME_SHOTS,cfg.PATH_JSON_SHOT)
