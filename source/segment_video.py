import os
import pandas as pd
from multiprocessing import Process
from uit.mmlab.vsum.segment import segment_shot
from uit.mmlab.vsum.visualization import create_json
from config.config import cfg

def segment_video(vid_path,saved_shot_json_path,json_id):
    video_name, begin_list, end_list = segment_shot.do_trainsnet(vid_path)

    create_json.create_shot_json(saved_shot_json_path,video_name,begin_list,None, json_id)

def segment_multi_videos(input_path,saved_shot_json_path,json_id):
    df = pd.read_csv(input_path)
    for i, row in df.iterrows():
        P = Process(target=segment_video, args=(row['path'],saved_shot_json_path,"shot_trsnet"))
        P.start()
        os.system("echo {} >> log/transnet_segment_log.txt".format(row['path']))

if __name__ == '__main__':
    # vid_path = "src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video/sTEELN-vY30.mp4"
    # segment_video(vid_path,cfg.PATH_JSON_SHOT_BL,"shot_trsnet")
    segment_multi_videos(cfg.VIDEO_CSV_PATH,cfg.PATH_JSON_SHOT_BL,"shot_trsnet")
