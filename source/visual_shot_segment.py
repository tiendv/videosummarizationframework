import glob,os
from config.config import cfg
from utilities.trecvid_tools import create_json_from_result_VSUM,create_json_from_result_event
from uit.mmlab.vsum.visualization import create_json



def visual_shot(shot_time_path,json_path,json_id):
    paths = glob.glob(shot_time_path+"/*/*.txt")

    for p in paths:
        print(p)
        vid_name = p.split("/")[-3]

        # create_json_from_result_VSUM(p,json_path,vid_name,json_id)
        create_json_from_result_event(p,json_path,vid_name,json_id)

def visual_segment(time_selection_path,lenght,json_id):
    paths = glob.glob(time_selection_path+"_{}s".format(i)+"/*/*.txt")

    dir_name = os.path.basename(time_selection_path)
    for p in paths:
        create_json.create_json_selections(p,os.path.join(cfg.TRECVID_SEGMENT_JSON_PATH,"{}_{}s").format(dir_name,lenght),json_id)

def visual_person_segment():
    paths = glob.glob(cfg.PATH_PERSON_SHOTS_BBC+"/*/*.txt")
    for p in paths:
        char_name = os.path.basename(p)[:-4]
        create_json.create_json_selections(p,cfg.TRECVID_SEGMENT_JSON_PATH,char_name)

if __name__ == '__main__':
    # for i in [20]:
        # visual_segment(cfg.PATH_TIME_SELECTION_BBC,i,"{}_{}".format(os.path.basename(cfg.PATH_TIME_SELECTION_BBC),i))
    visual_shot(cfg.PATH_TIME_SELECTION_BBC,cfg.TRECVID_SHOT_JSON_PATH,"event_bbc")
    # print("AAA")
