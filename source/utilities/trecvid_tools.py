import os
import pandas as pd
import numpy as np
from itertools import groupby
from config.config import cfg
from utilities.get_data_ref_bbc import get_data_ref_bbc
from utilities.convert_time import time2sec, sec2time
from uit.mmlab.vsum.visualization.create_json import create_json4shots


def get_shot_id(path,vid_id=0):
    '''
        vid_id=0 : get all of video
        vid_id=x : get all shot_id of videox
    '''
    with open(path,'r') as f:
        shots = f.read().splitlines()

    if vid_id:
        shots = [list(i) for j,i in groupby(shots,lambda x: x.partition('_')[0])]
        return shots[vid_id-175]
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

def write_trecvid_score(values,save_path):
    shots = get_shot_id(cfg.TRECVID_SHOT_ID_PATH)
    with open(os.path.join(save_path,"bbc_janine.csv"),'w') as f:
        for s,v in zip(shots,values):
            f.write("{},{}\n".format(s,v))

def write_selected_shot(selected_shot,selected_score,save_path,file_name):
    gName,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)

    selected_shot = [list(i) for j,i in groupby(selected_shot,lambda x: x.partition('_')[0])]

    for item in selected_shot:
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        with open(os.path.join(save_path,'{n}.txt'.format(n=file_name)),'w') as f:
            for ind,s in enumerate(item):
                shot = time_shot[s]
                st = shot[0]
                en = shot[1]
                sc = round(selected_score[ind][0],8)

                f.write('{} {} {} {}\n'.format(s,st,en,sc))
    print("the result is saved at " + os.path.join(save_path,'{n}.txt'.format(n=file_name)))

def create_json_from_result_VSUM(path_data,path_json,name_vid,id_json="shot_gt"):
    '''
        This function uses to create a json file from text file for shots
        input: path_data - path of txt file including time of shot
               path_json - path of json being saved
               name_vid - name of video
               id(optional) = id of the json file (default="shot_gt")
        output: none
    '''
    dicts_data = []
    list_begin = []
    list_score = []
    list_sec = []
    with open(path_data,'r') as f:
        for line in f:
            dict_data = {}
            line = line.split()
            gName,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)

            list_sec.append(round(time2sec(time_shot[line[0]][1])-time2sec(time_shot[line[0]][0]),2))
            list_score.append("1")

    t = 0
    for s in list_sec:
        list_begin.append(sec2time(t))
        t = t + s;

    create_json4shots(path_json, name_vid,list_begin,list_score,id_json)

def get_bbc_shot_event(shot_id):
    n_vid = shot_id.split("_")[0].replace("shot","video")
    event_csv = os.path.join(cfg.TRECVID_EVENT_SHOT_PATH,"{}/{}.csv".format(n_vid,shot_id))
    if not os.path.exists(event_csv):
        df = pd.DataFrame()
        return df

    df = pd.read_csv(event_csv,header=None)

    return df

def create_json_from_result_event(path_data,path_json,name_vid,id_json="shot_gt"):
    '''
        This function uses to create a json file from text file for shots
        input: path_data - path of txt file including time of shot
               path_json - path of json being saved
               name_vid - name of video
               id(optional) = id of the json file (default="shot_gt")
        output: none
    '''
    dicts_data = []
    list_begin = []
    list_score = []
    list_sec = []
    with open(path_data,'r') as f:
        for line in f:
            dict_data = {}
            line = line.split()
            gName,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)

            list_sec.append(round(time2sec(time_shot[line[0]][1])-time2sec(time_shot[line[0]][0]),2))
            df = get_bbc_shot_event(line[0])

            if df.empty:
                label = "None"
            else:
                label=""
                for i in range(5):
                    label = label + "{}({:0.3f})\n".format(df.loc[i][0],df.loc[i][1])
            list_score.append(label)

    t = 0
    for s in list_sec:
        list_begin.append(sec2time(t))
        t = t + s;


    create_json4shots(path_json, name_vid,list_begin,list_score,id_json)


def get_shot_lenght(shot_list):
    gName,time_shot = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    sec = []
    for s in shot_list:
        sec.append(time2sec(time_shot[s][1]) - time2sec(time_shot[s][0]))
    return sec
