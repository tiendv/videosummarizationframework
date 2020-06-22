import os
import pandas as pd
import numpy as np
from itertools import groupby
from config.config import cfg
from utilities.get_data_ref_bbc import get_data_ref_bbc
from utilities.convert_time import time2sec

def get_shot_id(path):
    with open(path,'r') as f:
        shots = f.read().splitlines()
    return shots


def get_skipped_shot(path):
    skips = {}
    with open(path,'r') as f:
        for l in f:
            p = l.rstrip().split(" ")
            skips[p[0]] = {'st':int(p[1]), 'en': int(p[2])}
    return skips

def get_bbc_segment(vid_id):
    _,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    shots = []
    segment = []
    for s in time_shot:
        if 'shot{}'.format(vid_id) in s:
            shots.append(s)
    for s in shots[:-1]:
        segment.append(int(time2sec(time_shot[s][1])/0.04))
    return segment

def gen_segment_score(vid_id,df):
    data = df.loc[vid_id]
    nFrames = int(data['nFrames'])
    # score = score_shot.random_score(nFrames)
    # print("The result score will be saved at {}".format(cfg.TRECVID_SCORE_PATH))
    # np.save(os.path.join(cfg.TRECVID_SCORE_PATH,str(vid_id)),score)

    segment = get_bbc_segment(vid_id)
    print(segment)
    # segment = segment_shot.do_twopeak(nFrames)
    print("The result segment is saved at {}".format(cfg.TRECVID_SEGMENT_PATH))
    np.save(os.path.join(cfg.TRECVID_SEGMENT_PATH,str(vid_id)),segment)

def get_trecvid_bbc_segment():
    df = pd.read_csv(cfg.VIDEO_CSV_BBC_PATH)
    segments = np.empty(0,dtype=np.int64)
    offset = 0
    for i in range(175,186):
        segment = np.load(os.path.join(cfg.TRECVID_BBC_SEGMENT_PATH,'{}.npy'.format(i)))
        nFrames = df.loc[i]['nFrames']
        segment = np.append(segment,nFrames) + offset
        segments = np.append(segments,segment)
        offset = segments[-1]
    np.save('./trecvid_bbc_shot',segments[:-1])
    return segments[:-1]


def write_time_shot(vid_id,seg_data,save_path):
    gName,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    vid_name = gName['{}'.format(vid_id)]

    if not os.path.isdir(os.path.join(save_path,vid_name)):
        os.makedirs(os.path.join(save_path,vid_name))
    with open(os.path.join(save_path,'{n}/{n}.txt'.format(n=vid_name)),'w') as f:
        for i,t in enumerate(seg_data):
            shot = time_shot['shot{}_{}'.format(vid_id,i+1)]
            st = shot[0]
            en = shot[1]
            sc = t.mean()
            f.write('{} {} {}\n'.format(st,en,sc))

def write_selected_shot(selected_shot,save_path,sum_len):
    gName,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    selected_shot = [list(i) for j,i in groupby(selected_shot,lambda x: x.partition('_')[0])]

    save_path = save_path+"_{}s".format(sum_len)
    for item in selected_shot:
        vid_id = item[0].split('_')[0][4:]
        vid_name = gName[vid_id]
        if not os.path.isdir(os.path.join(save_path,vid_name)):
            os.makedirs(os.path.join(save_path,vid_name))
        with open(os.path.join(save_path,'{n}/{n}.txt'.format(n=vid_name)),'w') as f:
            for s in item:
                shot = time_shot[s]
                st = shot[0]
                en = shot[1]
                f.write('{} {} {}\n'.format(s,st,en))
    print("the result is saved at " + save_path)
