#!/usr/bin/env python
# coding: utf-8

import os,sys,glob
import argparse
sys.path.append("../../../config")
sys.path.append("../../../../libs/deep_semantic_feature/")
from bbc_kmedoids_lib import run_kmedoids
import datetime
import time
import numpy as np
import pandas

def time2sec(times):
    x = time.strptime(times.split('.')[0],'%H:%M:%S')
    range_mili = 1
    mili = 0
    if len(times.split(".")) == 2 :
        if times.split(".")[1] != '':
            for i in range(len(times.split(".")[1])):
                range_mili = 10*range_mili
            mili = float(times.split(".")[1])/range_mili
        else:
            mili =0
    else:
        mili = 0
    return float(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds() + mili)


def create_feature(path_feature,path_selected,video_name):
    feature = np.load(path_feature+'/'+video_name+'_inceptionv1_1.npy')
    
if __name__ == "__main__":
    list_video_name_bbc= ['5531550228324592939', '5534228999422914578', '5539381671692122744', '5542003749222140011', '5544574287152993687', '5544620672795594434', '5547193787702629969', '5549784941472309008', '5552368364300855101', '5555325449284154780', '5555360238519252381']
    list_events = ['playing+videogames','fighting','attacking','laughing','hitting','crying','shaking','camping','baptizing','barbecuing']
#    f=  pandas.read_csv('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/events_emotion/video175/shot175_5.csv',header=None)
#    for event in f[0]:
#        list_events.append(event)

#    list_video_name_bbc= ['175','176','177','178','179','180','181','182','183','184','185']
    for person in ['janine','ryan','stacey']:
        feature  = []
        name_shot_selec = []
        time_start = []
        time_end = []
        print(person)
        for video_name in list_video_name_bbc:
#            feature_video = np.squeeze(np.load('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/shot_event/'+video_name+'/'))
            print (video_name)
            if os.path.exists('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/VSUM_TRECVID/bbc_person_segment/'+video_name+'/'+person+'.txt') :
                with open('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/VSUM_TRECVID/bbc_person_segment/'+video_name+'/'+person+'.txt','r') as person_shot:
                    Lines = person_shot.readlines() 
                    for line in Lines:
                        name_shot_selec.append(line.split(' ')[0])
                        start = int(time2sec((line.split(' ')[1]).replace('\n',''))*25)
                        time_start.append((line.split(' ')[1]).replace('\n',''))
                        end = int(time2sec((line.split(' ')[2]).replace('\n',''))*25)
                        time_end.append((line.split(' ')[2]).replace('\n',''))
                        temp = [0] * len(list_events)
                        if os.path.exists('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/shot_event/video'+((line.split(' ')[0]).split('_')[0]).replace('shot','')+'/'+line.split(' ')[0]+'.csv') :
                            f=  pandas.read_csv('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/shot_event/video'+((line.split(' ')[0]).split('_')[0]).replace('shot','')+'/'+line.split(' ')[0]+'.csv',header=None)
                            for j in range(len(list_events)):
                                id = 0
                                for event  in f[0]:
                                    if event == list_events[j]:
                                        temp[j] = f[1][id]
                                        #print event
                                        #print temp[i]
                                    id+=1
                        feature.append(np.array(temp))
        feature = np.array(feature)
        print(feature.shape)
        for k in [5,10,15,20]:
            selected = run_kmedoids(feature,k,person)
            print (selected)
            with open('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/VSUM_TRECVID/bbc_segment_time/bbc_major_life_event_kmedoids/'+str(k)+'/'+person+'.txt','w') as file_save:
                for i in selected:
                    file_save.write(name_shot_selec[i-1]+' '+time_start[i-1] + ' ' +time_end[i-1]+'\n')
                    print(name_shot_selec[i-1]+' '+time_start[i-1] + ' ' +time_end[i-1])

