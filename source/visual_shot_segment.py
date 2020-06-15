import glob,os
from config.config import cfg
from uit.mmlab.vsum.visualization import create_json

def visual_shot():
    paths = glob.glob(cfg.PATH_TIME_SHOTS_BBC+"/*/*.txt")
    for p in paths:
        vid_name = p.split("/")[-2]
        create_json.create_shot_json_from_file(p,cfg.TRECVID_SHOT_JSON_PATH,vid_name,"shot_bbc")

def visual_segment(lenght):
    paths = glob.glob(cfg.PATH_TIME_SELECTION_BBC+"_{}s".format(i)+"/*/*.txt")
    for p in paths:
        create_json.create_json_selections(p,cfg.TRECVID_SEGMENT_JSON_PATH+"_{}s".format(lenght),"bbc_drdsn_knapsack_{}".format(lenght))

def visual_person_segment():
    paths = glob.glob(cfg.PATH_PERSON_SHOTS_BBC+"/*/*.txt")
    for p in paths:
        char_name = os.path.basename(p)[:-4]
        create_json.create_json_selections(p,cfg.TRECVID_SEGMENT_JSON_PATH,char_name)

if __name__ == '__main__':
    # for i in [150,300,450,600]:
    #     visual_segment(i)
    visual_person_segment()
