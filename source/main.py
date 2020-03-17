import cv2
import os,sys,glob
import random
from multiprocessing import Process

from utilities.convert_time import sec2time
# from src.baseline.segmentation.create_json_from_time_shots import create_json4shots
# from src.baseline.selection.get_data_to_selection import create_json_selection_file,selection_shot_knapsack_file,get_data_to_selection,selection_shot_knapsack, create_json_selection
from config.config import cfg
from main_baseline import main_baseline


def fusion(path_time_shots,path_save):
    result = selection_shot_knapsack_file(path_data=path_time_shots,L=0.15)
    print(result)
    create_json_selection_file(path_time_shots, result , path_save)
def run_multi_process():
    for path, subdirs, files in os.walk(cfg.PATH_TIME_SHOTS_GT):
        for name in files:
            print(os.path.join(path,name))
            # fusion(os.path.join(path,name),cfg.PATH_JSON_SELECT_GT)
            pro = Process(target=fusion, args=(os.path.join(path,name),cfg.PATH_JSON_SELECT_GT))
            pro.start()


if __name__ == '__main__':
    paths = glob.glob("src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video/*.mp4")
    for p in paths:
        main_baseline(p,cfg.PATH_JSON_SHOT_BL,cfg.PATH_JSON_SELECT_BL)
