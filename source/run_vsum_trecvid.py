import os,glob
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

def select_ranking(data,capacity):
    pass

def summarize(seg_data, shot_score, sum_lenght, use_sum=False):
    capacity = int(sum_lenght/0.04)
    weights = [x.size for x in seg_data]

    if use_sum:
        values = [x.sum() for x in seg_data]
    else:
        values = [x.mean() for x in seg_data]
    # values = np.asarray(values) + shot_score
    values = shot_score


    # print(values)
    # input("CC")

    _, selected_cut = select_shot.knapsack([(v, w) for v, w in zip(values, weights)], capacity)
    # total = 0
    # for i in selected_cut:
    #     total = total + seg_data[i].size
    # print(total)
    # input("CC")
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

def gen_segment_score(vid_id,df):
    data = df.loc[vid_id]
    nFrames = int(data['nFrames'])
    # score = score_shot.random_score(nFrames)
    # print("The result score will be saved at {}".format(cfg.TRECVID_SCORE_PATH))
    # np.save(os.path.join(cfg.TRECVID_SCORE_PATH,str(vid_id)),score)

    segment = get_bbc_segment(vid_id)
    # segment = segment_shot.do_onepeak(nFrames)
    print("The result segment is saved at {}".format(cfg.TRECVID_SEGMENT_PATH))
    np.save(os.path.join(cfg.TRECVID_SEGMENT_PATH,str(vid_id)),segment)


def get_segment_data(vid_id,skip_shot=None):
    '''
        return a segment of a video with score frames
        input:
            vid_id -- id of bbc video
            skip_shot -- skipped shot file
        output:
            a segment of a video with score frames
    '''
    print("load segment from " + cfg.TRECVID_SEGMENT_PATH)
    segment = np.load(os.path.join(cfg.TRECVID_SEGMENT_PATH,'{}.npy'.format(vid_id)))

    print("load score from " + cfg.TRECVID_SCORE_PATH)
    score = np.load(os.path.join(cfg.TRECVID_SCORE_PATH,'{}.npy'.format(vid_id)))

    seg_data = np.split(score,segment)
    seg_data = list(filter(lambda x: x.size, seg_data))

    #set skipped shot score is zero
    if skip_shot:
        for i in range(skip_shot['st']):
            seg_data[i][:]=0
        for i in range(1,skip_shot['en']+1):
            seg_data[-i][:]=0

    #write_time_shot(vid_id,seg_data,cfg.PATH_TIME_SHOTS_BBC)
    return seg_data

def gen_trecvid_vsum(selected_shot_path,length,save_path):
    '''
        generate trecvid video summarization
        input:
            selected_shot_path -- path saving the selected shot
            method -- name of method
            length -- lenght of vsum
        output:
            mp4 video summarization
    '''
    method = os.path.basename(selected_shot_path)
    file_name = "{}_{}s.mp4".format(method,length)

    paths = glob.glob(os.path.join(selected_shot_path+"_{}s".format(length),"*/*.txt"))
    paths.sort(key=lambda x: float(x.split("/")[-2]))

    selected_shot_id = []
    for path in paths:
        with open(path,'r') as f:
            for l in f:
                selected_shot_id.append(l.split(" ")[0])
    gen_video_sum(file_name,selected_shot_id,cfg.PATH_SHOT_BBC,os.path.join(save_path,method))

def main(time_shot_path,char_name):
    shots = get_shot_id(cfg.TRECVID_SHOT_ID_PATH)
    skip_shot = get_skipped_shot(cfg.SKIPPED_TRECVID_SHOT_PATH)

    print(len(shots))

    seg_data = []
    person_scores = np.empty(0)

    for i in range(175,186):
        seg_data = seg_data + get_segment_data(i,skip_shot[str(i)])
        person_scores = np.hstack((person_scores,np.load(os.path.join(cfg.PERSON_SCORE_PATH,"{}/video{}.npy".format(char_name,i)))))
        # print(np.load(os.path.join(cfg.PERSON_SCORE_PATH,"{}/video{}.npy".format(char_name,i))).shape[0])
    for sum_len in [150,300,450,600]:
        select_shot_idx = summarize(seg_data,person_scores,sum_len)
        selected_shot_id = list(map(shots.__getitem__,select_shot_idx))

        write_selected_shot(selected_shot_id,time_shot_path,sum_len)

if __name__ == '__main__':
    # main(cfg.PATH_TIME_SELECTION_BBC,'janine')
    for t in [150,300,450,600]:
       gen_trecvid_vsum(cfg.PATH_TIME_SELECTION_BBC,t,cfg.PATH_RESULT_VSUM_BBC)

    # df = pd.read_csv(cfg.VIDEO_CSV_BBC_PATH)
    # for i in range(175,186):
    #     gen_segment_score(i,df)
    # gen_video_sum('aa.mp4',['shot175_1101','shot175_1102','shot175_1103','shot175_1104','shot175_1105','shot175_1106','shot175_1107','shot175_1108'],cfg.PATH_SHOT_BBC,'./')
