import cv2
import os,sys,glob
import random
from multiprocessing import Process

from utilities.convert_time import sec2time
# from src.baseline.segmentation.create_json_from_time_shots import create_json4shots
# from src.baseline.selection.get_data_to_selection import create_json_selection_file,selection_shot_knapsack_file,get_data_to_selection,selection_shot_knapsack, create_json_selection
from config.config import cfg
from main_baseline import main_baseline

def run_GT_TVSum():
    paths = glob.glob("src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video/*.mp4")
    for p in paths:
        pro = Process(target=main_baseline,args=(p,cfg.PATH_JSON_SHOT_GT,cfg.PATH_JSON_SELECT_GT))
        pro.start()

if __name__ == '__main__':
    run_GT_TVSum()
