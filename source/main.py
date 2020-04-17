import cv2
import os,sys,glob
import random
import pandas as pd
import pickle
from multiprocessing import Process

from utilities.convert_time import sec2time
from utilities.get_data_ref_bbc import get_data_ref_bbc
from src.baseline.segmentation.create_json_from_time_shots import create_json4shots,create_json4shots_file
from src.baseline.selection.get_data_to_selection import selection_shot_knapsack,create_json_selection,get_data_from_time_shot_file
from src.baseline.segmentation.segment_video import create_segment,create_segments_tvsum
from config.config import cfg
from main_baseline import main_baseline

def run_GT_TVSum():
    paths = glob.glob("src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video/*.mp4")
    for p in paths:
        main_baseline(p,cfg.PATH_JSON_SHOT_BL,cfg.PATH_JSON_SELECT_BL,"shot_rd","seg_rd")
        # pro = Process(target=main_baseline,args=(p,cfg.PATH_JSON_SHOT_BL,cfg.PATH_JSON_SELECT_BL,"shot_rd","seg_rd"))
        # pro.start()

def create_json_for_bbc_event(path_dir_event,path_json_save,topK=5,id_json='event_bbc'):
    '''
        This function uses to create json file for events detected
        input: path_dir_event - the event directory path
               path_json_save - the directory path that the json file will be saved
               topK - the value of the k-top you want to write
        output: none
    '''
    event_videos = glob.glob(os.path.join(path_dir_event,"*"))
    event_videos.sort(key=lambda x: int(os.path.basename(x).replace("video","")))
    ref_id, time_shots = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    for p in event_videos:
        name_vid = ref_id[os.path.basename(p).replace("video","")]
        print(p)
        shots = glob.glob(os.path.join(p,"*.csv"))
        list_title = []
        list_begin = []
        for s in shots:
            data = pd.read_csv(s,header=None,nrows=topK)
            title=''
            for i in range(topK):
                ev = data.iloc[i][0] #get event
                sc = data.iloc[i][1] #get score
                title = title + "{}({})\n".format(ev,round(sc,3))
            list_title.append(title)
            list_begin.append(time_shots[os.path.basename(s).split(".")[0]][0])
        create_json4shots(path_json_save, name_vid, list_begin, list_title, id_json)

def create_json_for_shot_boundary(path_dir_sbd,path_json_save,id_json='shot_bl'):
    for path, subdirs, files in os.walk(path_dir_sbd):
        for name in files:
            create_json4shots_file(os.path.join(path,name),path_json_save,name.split(".")[0],id_json)



if __name__ == '__main__':
    run_GT_TVSum()
    # create_json_for_shot_boundary(cfg.PATH_TIME_SHOTS_GT_SUMME,cfg.PATH_JSON_SHOT_GT_SUMME,'shot_gt_summe')
    # create_json_for_bbc_event(cfg.PATH_EVENT_EMOTION_BBC,cfg.PATH_JSON_EVENT_EMOTION_BBC,7,'emotions')
    # ref_id, time_shots = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    # print(ref_id['121'])
    # path_face = os.path.join(cfg.PATH_FACES_SHOT_BBC,"video1/shot1_1790.pickle")

# create video segment selection:
# input: tcin,tcout
# output: .json

    # for path, subdirs, files in os.walk(cfg.PATH_TIME_SHOTS_RGB_VSUM_DSF_BBC):
    #     for name in files:
    #         with open(os.path.join(path,name)) as f:
    #             lines = list(f)
    #             list_begin = []
    #             list_ending = []
    #             name_vid = name.split(".txt")[0]
    #             for line in lines :
    #                 list_begin.append(line.split(" ")[0])
    #                 list_ending.append(line.split(" ")[1])
    #         create_json_selection( name_vid, list_begin,list_ending,path_json=cfg.PATH_JSON_SHOT_RGB_SUM_DSF_BBC,id="seg_vsum_dsf_rgb")
