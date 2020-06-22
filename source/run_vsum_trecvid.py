import os,glob
import numpy as np
import pandas as pd

from utilities.create_VSUM_submission import gen_video_sum
from utilities.trecvid_tools import *
from config.config import cfg
from uit.mmlab.vsum.segment import segment_shot
from uit.mmlab.vsum.scoring import score_shot
from uit.mmlab.vsum.selection import select_shot

def mapping_bbc_shot(seg_data,selected_idx,thres=0.5):
    segment = [np.copy(x) for x in seg_data]
    selected_bbc_idx = []
    for i in range(len(segment)):
        segment[i][:]= 1 if i in selected_idx else 0

    frames_idx = np.concatenate(segment,axis=None)
    bbc_seg = np.split(frames_idx,np.load(cfg.TRECVID_BBC_SEGMENT_PATH))
    for ind,s in enumerate(bbc_seg):
        if s.mean() > thres:
            selected_bbc_idx.append(ind)
    print("len",len(selected_bbc_idx))
    return selected_bbc_idx

def summarize(seg_data, shot_score, sum_lenght, use_sum=False):
    capacity = int(sum_lenght/0.04)
    weights = [x.size for x in seg_data]

    if use_sum:
        values = [x.sum() for x in seg_data]
    else:
        values = [x.mean() for x in seg_data]
    # values = np.asarray(values) + shot_score
    # values = shot_score
    _, selected_cut = select_shot.knapsack([(v, w) for v, w in zip(values, weights)], capacity)

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

def main(time_shot_path,char_name,write_shot=True):
    shots = get_shot_id(cfg.TRECVID_SHOT_ID_PATH)
    skip_shot = get_skipped_shot(cfg.SKIPPED_TRECVID_SHOT_PATH)

    print(len(shots))

    seg_data = []
    person_scores = np.empty(0)

    for i in range(175,186):
        seg_data = seg_data + get_segment_data(i,skip_shot[str(i)])
        person_scores = np.hstack((person_scores,np.load(os.path.join(cfg.PERSON_SCORE_PATH,"{}/video{}.npy".format(char_name,i)))))

    for sum_len in [150,300,450,600]:
        select_shot_idx = summarize(seg_data,person_scores,sum_len)

        select_shot_idx = mapping_bbc_shot(seg_data,select_shot_idx,thres=0.25)

        selected_shot_id = list(map(shots.__getitem__,select_shot_idx))

        if write_shot:
            write_selected_shot(selected_shot_id,time_shot_path,sum_len)

if __name__ == '__main__':
    # main(cfg.PATH_TIME_SELECTION_BBC,'janine')

    for t in [150,300,450,600]:
       gen_trecvid_vsum(cfg.PATH_TIME_SELECTION_BBC,t,cfg.PATH_RESULT_VSUM_BBC)

    # df = pd.read_csv(cfg.VIDEO_CSV_BBC_PATH)
    # for i in range(175,186):
    #     gen_segment_score(i,df)
    # gen_video_sum('aa.mp4',['shot175_1101','shot175_1102','shot175_1103','shot175_1104','shot175_1105','shot175_1106','shot175_1107','shot175_1108'],cfg.PATH_SHOT_BBC,'./')
