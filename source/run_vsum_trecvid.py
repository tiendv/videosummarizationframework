import os,glob
import numpy as np
import pandas as pd
import random
import argparse
from eval import evalBBC

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
        print("SSSS")
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

def get_shot_data(st,en,char_name,use_sum=False, thres=2.0, norm = True, method=0):
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
    if method=="1":
        print("Method person score")
        values = person_scores
    elif method=="2":
        print("Method sum score")
        values = np.asarray(values) + person_scores

    # if norm:
    #     values = np.array(values)
    #     values[:] = (v-values.min())/(v.max()-v.min())
    print("summarize for thres = {}".format(thres))
    for i,x in enumerate(seg_data):
        if x.size <= thres//0.04:
            values[i] = 0

    shot_data = list(zip(values, weights)) #tuple(score,lenght)

    return shot_data


def main(time_shot_path,char_name,file_name=None,thres=2.0,method=0):
    bbc_shot_ids = get_shot_id(cfg.TRECVID_SHOT_ID_PATH,vid_id=175)

    shot_data = get_shot_data(175,175,char_name=char_name,thres=thres,norm=True,method=method)


    sum_lenght = 129
    ##Using random_score
    # select_shot_idx = random.sample(range(len(shot_data)),20)

    ##Using knapsack
    capacity = int(sum_lenght/0.04)
    _, select_shot_idx = select_shot.knapsack([(v, w) for v, w in shot_data], capacity)

    ##Using TopK
    # select_shot_idx = chooseTopKShot(shot_data,topK=80,sum_lenght=None)


    # select_shot_idx = mapping_bbc_shot(seg_data,select_shot_idx,thres=0.25)

    selected_shot_id = list(map(bbc_shot_ids.__getitem__,select_shot_idx))
    selected_shot_scores = list(map(shot_data.__getitem__,select_shot_idx))

    if file_name:
        write_selected_shot(selected_shot_id,selected_shot_scores,time_shot_path,file_name)

if __name__ == '__main__':
    #change TRECVID_SEGMENT_PATH and TRECVID_SCORE_PATH in config dir
    # parser = argparse.ArgumentParser()
    # parser.add_argument("thres",type=float)
    # parser.add_argument("method")
    #
    # args = parser.parse_args()
    # if args.method=="0":
    #     me = "vasnet"
    # elif args.method=="1":
    #     me = "janine"
    # elif args.method=="2":
    #     me = "vasnetjanine"
    #
    # file_name = "bbc{}_{}_knapsack80".format(args.thres,me)
    # main(cfg.PATH_TIME_SELECTION_BBC,'janine',file_name = file_name,thres=args.thres,method=args.method)
    # evalBBC(os.path.join(cfg.PATH_TIME_SELECTION_BBC,"{}.txt".format(file_name)),cfg.VIDEO175_GT)


    # for t in [150]:
       # gen_trecvid_vsum(cfg.PATH_TIME_SELECTION_BBC,t,cfg.PATH_RESULT_VSUM_BBC)

    # df = pd.read_csv(cfg.VIDEO_CSV_BBC_PATH)
    # for i in range(175,186):
    #     gen_segment_score(i,df)
#     gt_shot = [
# 'shot175_29',
# 'shot175_35',
# 'shot175_45',
# 'shot175_47',
# 'shot175_114',
# 'shot175_154',
# 'shot175_167',
# 'shot175_175',
# 'shot175_210',
# 'shot175_212',
# 'shot175_219',
# 'shot175_260',
# 'shot175_269',
# 'shot175_273',
# 'shot175_285',
# 'shot175_287',
# 'shot175_316',
# 'shot175_319',
# 'shot175_359',
# 'shot175_361',
# 'shot175_364',
# 'shot175_365',
# 'shot175_378',
# 'shot175_412',
# 'shot175_449',
# 'shot175_453',
# 'shot175_455',
# 'shot175_457',
# 'shot175_494',
# 'shot175_495',
# 'shot175_504',
# 'shot175_510',
# 'shot175_524',
# 'shot175_527',
# 'shot175_538',
# 'shot175_598',
# 'shot175_618',
# 'shot175_631',
# 'shot175_641',
# 'shot175_642',
# 'shot175_669',
# 'shot175_763',
# 'shot175_766',
# 'shot175_784',
# 'shot175_800',
# 'shot175_808',
# 'shot175_860',
# 'shot175_872',
# 'shot175_873',
# 'shot175_895',
# 'shot175_903',
# 'shot175_940',
# 'shot175_972',
# 'shot175_986',
# 'shot175_1092',
# 'shot175_1097',
# 'shot175_1100',
# 'shot175_1135',
# 'shot175_1143',
# 'shot175_1186',
# 'shot175_1188',
# 'shot175_1258',
# 'shot175_1273',
# 'shot175_1293',
# 'shot175_1353',
# 'shot175_1359',
# 'shot175_1438',
# 'shot175_1440',
# 'shot175_1468',
# 'shot175_1766',
# 'shot175_1778',
# 'shot175_1825',
# 'shot175_1879',
# 'shot175_1935',
# 'shot175_1942',
# 'shot175_1972',
# 'shot175_2218',
# 'shot175_2254',
# 'shot175_2307',
# 'shot175_2334',
#     ]
#
#     secs = get_shot_lenght(gt_shot)
#     with open("./secs.txt",'w') as f:
#         for s in secs:
#             f.write("{}\n".format(round(s,3)))



    # gen_video_sum('GT_VSUM.mp4',shot_list,cfg.PATH_SHOT_BBC,cfg.PATH_RESULT_VSUM_BBC)
