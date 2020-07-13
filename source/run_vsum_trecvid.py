import os,glob
import numpy as np
import pandas as pd

from utilities.create_VSUM_submission import gen_video_sum
from utilities.trecvid_tools import *
from config.config import cfg
from uit.mmlab.vsum.segment import segment_shot
from uit.mmlab.vsum.scoring import score_shot
from uit.mmlab.vsum.selection import select_shot


def chooseTopKShot(shot_data, topK=5, sum_lenght=150):
    sorted_idx = [i[0] for i in sorted(enumerate(shot_data), key=lambda x: x[1][0], reverse=True)]
    selected_cut = []

    if sum_lenght:
        capacity = int(sum_lenght/0.04)
        for i in sorted_idx:
            if capacity >=50:
                selected_cut.append(i)
                capacity=capacity - shot_data[i][1]

    if topK:
        selected_cut = sorted_idx[:topK]
    selected_cut.sort()
    return selected_cut

def summarize(shot_data, sum_lenght):
    capacity = int(sum_lenght/0.04)
    selected_cut = chooseTopKShot(shot_data,topK=None,sum_lenght=sum_lenght)
    # _, selected_cut = select_shot.knapsack([(v, w) for v, w in shot_data], capacity)

    return selected_cut



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

def get_shot_data(st,en,char_name,use_sum=False, thres=2.0):
    skip_shot = get_skipped_shot(cfg.SKIPPED_TRECVID_SHOT_PATH)
    seg_data = []
    person_scores = np.empty(0)

    for i in range(st,en+1):
        seg_data = seg_data + get_segment_data(i,skip_shot[str(i)])
        person_scores = np.hstack((person_scores,np.load(os.path.join(cfg.PERSON_SCORE_PATH,"{}/video{}.npy".format(char_name,i)))))

    weights = [x.size for x in seg_data]

    if use_sum:
        values = [x.sum() for x in seg_data]
    else:
        values = [x.mean() for x in seg_data]
    # values = np.asarray(values) + person_scores
    # values = person_scores
    for i,x in enumerate(seg_data):
        if x.size < thres//0.04:
            values[i] = 0

    shot_data = list(zip(values, weights))
    return shot_data


def main(time_shot_path,char_name,write_shot=True):
    bbc_shot_ids = get_shot_id(cfg.TRECVID_SHOT_ID_PATH,vid_id=175)

    shot_data = get_shot_data(175,175,char_name=char_name,thres=2.0)

    for sum_len in [150]:
        select_shot_idx = summarize(shot_data,sum_len)

        # select_shot_idx = mapping_bbc_shot(seg_data,select_shot_idx,thres=0.25)

        selected_shot_id = list(map(bbc_shot_ids.__getitem__,select_shot_idx))
        selected_shot_scores = list(map(shot_data.__getitem__,select_shot_idx))

        if write_shot:
            write_selected_shot(selected_shot_id,selected_shot_scores,time_shot_path,sum_len)

if __name__ == '__main__':
    #change TRECVID_SEGMENT_PATH and TRECVID_SCORE_PATH in config dir
    # main(cfg.PATH_TIME_SELECTION_BBC,'janine',write_shot=True)

    for t in [150]:
       gen_trecvid_vsum(cfg.PATH_TIME_SELECTION_BBC,t,cfg.PATH_RESULT_VSUM_BBC)

    # df = pd.read_csv(cfg.VIDEO_CSV_BBC_PATH)
    # for i in range(175,186):
    #     gen_segment_score(i,df)
    # shot_list = [
    #
    # ]
    # shot_list.sort(key=lambda x: int(x.split("_")[0][4:])*10000 + int(x.split("_")[-1]))
    # print(shot_list)
    # gen_video_sum('bbc_vasnetjanine_top20.mp4',shot_list,cfg.PATH_SHOT_BBC,cfg.PATH_RESULT_VSUM_BBC)
