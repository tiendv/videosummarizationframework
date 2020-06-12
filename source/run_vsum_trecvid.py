import os
import numpy as np
import pandas as pd
from itertools import groupby

from utilities.get_data_ref_bbc import get_data_ref_bbc
from utilities.convert_time import time2sec
from utilities.create_VSUM_submission import gen_video_sum
from config.config import cfg
from uit.mmlab.vsum.segment import segment_shot
from uit.mmlab.vsum.scoring import score_shot
from uit.mmlab.vsum.selection import select_shot


def cal_iou(shot,segment):
    latest_start = max(shot[0], segment[0])
    earliest_end = min(shot[1], segment[1])
    delta_o = earliest_end - latest_start + 1
    overlap = max(0,delta_o)

    earliest_start = min(shot[0], segment[0])
    latest_end = max(shot[1], segment[1])
    intersec = latest_end - earliest_start
    print(overlap)
    print(overlap/intersec)

def mapping_shot(vid_id,time_shots,rand_summary):
        for s in time_shots:
            if 'shot{}'.format(vid_id) in s:
                print(time_shots[s])

def summarize(seg_data, sum_lenght, use_sum=False):
    capacity = int(sum_lenght/0.04)
    weights = [x.size for x in seg_data]

    if use_sum:
        values = [x.sum() for x in seg_data]
    else:
        values = [x.mean() for x in seg_data]
    _, selected_cut = select_shot.knapsack([(v, w) for v, w in zip(values, weights)], capacity)
    # total = 0
    # for i in selected_cut:
    #     total = total + seg_data[i].size
    # print(total)
    return selected_cut

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

def get_shot_id(st_id,en_id):
    _,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    shots = []
    for id in range(st_id,en_id+1):
        tmp = []
        for s in time_shot:
            if 'shot{}'.format(id) in s:
                tmp.append(s)
        shots.append(tmp)
    shots = sum(shots,[])
    return shots


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

def write_selected_shot(selected_shot,save_path):
    gName,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    selected_shot = [list(i) for j,i in groupby(selected_shot,lambda x: x.partition('_')[0])]

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
                f.write('{} {}\n'.format(st,en))

def gen_segment_score(vid_id,df):
    data = df.loc[vid_id]
    nFrames = int(data['nFrames'])
    segment = get_bbc_segment(vid_id)
    score = score_shot.random_score(nFrames)
    np.save(os.path.join(cfg.TRECVID_SEGMENT_PATH,str(vid_id)),segment)
    np.save(os.path.join(cfg.TRECVID_SCORE_PATH,str(vid_id)),score)

def get_segment_score(vid_id):
    segment = np.load(os.path.join(cfg.TRECVID_SEGMENT_PATH,'{}.npy'.format(vid_id)))
    score = np.load(os.path.join(cfg.TRECVID_SCORE_PATH,'{}.npy'.format(vid_id)))[:-2]

    seg_data = np.split(score,segment)
    seg_data = list(filter(lambda x: x.size, seg_data))
    write_time_shot(vid_id,seg_data,cfg.PATH_TIME_SHOTS_BBC)
    return seg_data

def main():
    df = pd.read_csv(cfg.VIDEO_CSV_BBC_PATH)
    shots = get_shot_id(175,185)
    seg_data = []
    for i in range(175,186):
        seg_data = seg_data + get_segment_score(i)

    select_shot_idx = summarize(seg_data,150)
    selected_shot_id = list(map(shots.__getitem__,select_shot_idx))

    write_selected_shot(selected_shot_id,cfg.PATH_TIME_SELECTION_BBC)

    method = 'bbc_vasnet_knapsack'
    file_name = method+'.mp4'
    gen_video_sum(file_name,selected_shot_id,cfg.PATH_SHOT_BBC,os.path.join(cfg.PATH_RESULT_VSUM_BBC,method))

if __name__ == '__main__':
    main()
    # get_shot_id(175,185)
    # df = pd.read_csv(cfg.VIDEO_CSV_BBC_PATH)
    # for i in range(176,186):
    #     gen_segment_score(i,df)
