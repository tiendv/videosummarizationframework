import glob,os
from config.config import cfg
from uit.mmlab.vsum.visualization import create_json

def visual_shot():
    paths = glob.glob(cfg.PATH_TIME_SHOTS_BBC+"/*/*.txt")
    for p in paths:
        vid_name = p.split("/")[-2]
        create_json.create_shot_json_from_file(p,cfg.TRECVID_SHOT_JSON_PATH,vid_name,"shot_bbc")

def visual_segment():
    paths = glob.glob(cfg.PATH_TIME_SELECTION_BBC+"/*/*.txt")
    for p in paths:
        create_json.create_json_selections(p,cfg.TRECVID_SEGMENT_JSON_PATH,"bbc_vasnet_1")

if __name__ == '__main__':
    visual_segment()
