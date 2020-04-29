import sys,os
import argparse

sys.path.append("../../../config")
sys.path.append("../../../../libs/moments_model/")
from config import cfg
from test_video import test_model as detect_event

def run_detect_event(vid_id):
    #************************************************************************
    # Purpose: detect event from shots of a bbc video
    # Inputs:
    # - vid_id: id of the bbc video
    # Output: the result csv file stored in cfg.OUTPUT_PATH
    # Author: Dungmn
    #************************************************************************

    with open(os.path.join(cfg.BBC_SHOT_PATH,"video{}.txt".format(vid_id)),'r') as f:
        data = f.readlines()
    for s in data:
        s = s.rstrip()
        detect_event(s,cfg.OUTPUT_PATH)
    os.system("echo video{} >> {}/detect_event_log.txt".format(vid_id,cfg.LOG_DIR_PATH))

def main():
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('st', type=int, help='ID of start video')
    parser.add_argument('en', type=int, help='ID of end video')

    args = parser.parse_args()
    for i in range(args.st,args.en+1):
        run_detect_event(i)

if __name__ == '__main__':
    # main()
    detect_event(cfg.EXAMPLE_BBC_SHOT_PATH,cfg.EXAMPLE_OUTPUT_PATH)
