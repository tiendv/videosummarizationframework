import cv2
import os,sys,glob
import random
from multiprocessing import Process

from utilities.convert_time import sec2time
from utilities.get_data_ref_bbc import get_data_ref_bbc
from src.baseline.segmentation.create_json_from_time_shots import create_json4shots
# from src.baseline.selection.get_data_to_selection import create_json_selection_file,selection_shot_knapsack_file,get_data_to_selection,selection_shot_knapsack, create_json_selection
from config.config import cfg
from main_baseline import main_baseline

def run_GT_TVSum():
    paths = glob.glob("src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video/*.mp4")
    for p in paths:
        pro = Process(target=main_baseline,args=(p,cfg.PATH_JSON_SHOT_GT,cfg.PATH_JSON_SELECT_GT,"shot_gt","seg_gt"))
        pro.start()

def create_json_for_event(path_dir_event,path_json_save):
    event_videos = glob.glob(os.path.join(path_dir_event,"*"))
    event_videos.sort(key=lambda x: int(os.path.basename(x).replace("video","")))
    ref_id, time_shots = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    for p in event_videos:
        name_vid = ref_id[os.path.basename(p).replace("video","")]
        shots = glob.glob(os.path.join(p,"*.txt"))
        list_title = []
        list_begin = []
        for s in shots:
            with open(s,"r") as f:
                list_title.append(f.read())
                list_begin.append(time_shots[os.path.basename(s).split(".")[0]][0])
        create_json4shots(path_json_save, name_vid, list_begin, list_title, 'event_bbc')

if __name__ == '__main__':
    # run_GT_TVSum()
    create_json_for_event(cfg.PATH_EVENT_SHOT_BBC,cfg.PATH_JSON_EVENT_BBC)
