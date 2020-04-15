import os
import random
from multiprocessing import Process
from config.config import cfg
from src.baseline.selection.get_data_to_selection import selection_shot_knapsack,create_json_selection,get_data_from_time_shot_file

def calc_score(list_begin,list_ending):
    print("The score is generated randomly")
    list_score = []
    for _ in range(len(list_begin)):
        list_score.append(round(random.randint(10,50)/10,1))
    return list_score

def select_shots(time_shot_path,save_json_file,id_json='seg_sf'):
    '''
        This function uses to select shots for summarizing video from file
        input: time_shot_path - the path of the file including the shot times of each shot
               save_json_file - the path that uses to save the result json file
               id_json - the id of the json file for visualization
        output: none
    '''

    name_vid,begin_list,end_list,_ = get_data_from_time_shot_file(time_shot_path)

    # if os.path.isdir(os.path.join(save_json_file,name_vid)):
    #     print("Done " + os.path.join(save_json_file,name_vid))
    #     return 0

    score_list = calc_score(begin_list,end_list)
    result = selection_shot_knapsack(begin_list,end_list,score_list)
    create_json_selection(name_vid,begin_list,end_list,result,save_json_file,id_json)

if __name__ == '__main__':
    for path, subdirs, files in os.walk(cfg.PATH_TIME_SHOTS_GT_SUMME):
        for name in files:
            print(os.path.join(path,name))
            select_shots(os.path.join(path,name),cfg.PATH_JSON_SELECT_BL_SUMME,"seg_rd")
            # pro = Process(target=select_shots,args=(os.path.join(path,name),cfg.PATH_JSON_SELECT_BL,"seg_sf"))
            # pro.start()
    # select_shots(os.path.join(cfg.PATH_TIME_SHOTS_GT,"sTEELN-vY30/sTEELN-vY30.txt"),cfg.PATH_JSON_SELECT_GT,"seg_gt")
