import simplejson
import numpy as np
import sys,os,glob
import csv
import pandas
from os import listdir
from os.path import isfile, join
import datetime
import time

def time2sec(times):
    mili = 0
    if len((times.split(".")[1]).replace("\n","")) == 1:
        mili =float(float(times.split(".")[1])/10)
    else:
        mili =float(float(times.split(".")[1])/100)
    x = time.strptime(times.split('.')[0],'%H:%M:%S')
    return float(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds() + mili)




class SUMME():

    def __init__(self, video_id,fps,datatype, duration,path_npy,fnum,path_reference,feat_type='vgg'):
        print "***OK***",video_id
        file_json= []
        dictionary = {}
        dictionary['image']= []
        dictionary['score']= []
        dictionary['imgID']= []
        for i in range(fnum):
            dictionary['image'].append(str(i).zfill(6) + '.jpg')
            dictionary['score'].append(0)
            dictionary['imgID'].append(i)
        file_json.append(dictionary)
        dictionary['videoID'] = video_id
        dictionary['length'] = duration
        dictionary['fps'] = fps
        dictionary['fnum'] = fnum
        dataset = file_json
        data = filter(lambda x: x['videoID'] == video_id, dataset)
        self.data = data[0]
        first = True
        list_events = []
        onlyfiles = []
        if os.path.isdir(os.path.join(path_npy,video_id)):
            onlyfiles = [f for f in listdir(os.path.join(path_npy,video_id)) if isfile(join(os.path.join(path_npy,video_id), f))]
        path = os.path.join(path_npy,video_id)
        vector = []

        dict_refer = {}
        with open(path_reference,"r") as f:
            Lines = f.readlines() 
            time_filter = 0
            start = 0
            end = 0
            total = 0
            total_shot = 0
            for line in Lines:    
                if int(((line.split("    ")[1]).split("_")[0]).replace("shot","")) != int(video_id.replace("video","")) :
                    continue
                start = end
                end = float(time2sec(line.split("    ")[3]))
                if time_filter + ((end-start)-int(end-start)) >= 1 :
                    time_filter  =  ((end-start)-int(end-start)) + time_filter -1
                    dict_refer[str("video"+((line.split("    ")[1]).split("_")[0]).replace("shot",""))+str(line.split("    ")[1])] = (int(end-start)+1)
                    total += (int(end-start)+1)
                else:
                    time_filter += ((end-start)-int(end-start))
                    dict_refer[str("video"+((line.split("    ")[1]).split("_")[0]).replace("shot",""))+str(line.split("    ")[1])] = (int(end-start))
                    total +=int(end-start)
                if int(((line.split("    ")[1]).split("_")[0]).replace("shot","")) == int(video_id.replace("video","")) :
                    total_shot = int((line.split("    ")[1]).split("_")[1])
        list_events = []
        for paths, subdirs, files in os.walk(path_npy):
            for name in files:
                f=  pandas.read_csv(os.path.join(paths,name),header=None)
                list_event= []
                for event in f[0]:
                    list_events.append(event)
                break
            if len(list_events) != 0 :
                break
        totals = 0
        for i in range (1,total_shot+1):
            name_shot = str("shot"+video_id.replace("video","")+"_"+str(i))
            key_frames = dict_refer[str(video_id)+str(name_shot)]
            temp = [0] * len(list_events)
            try:
                f=  pandas.read_csv(os.path.join(path,name_shot+".csv"),header=None)             
                for j in range(len(list_events)):
                    id = 0
                    for event  in f[0]:
                        if event == list_events[j]:
                            temp[j] = f[1][id]
                        id+=1
            except:
                a = 0
            for k in range(key_frames):
                totals+=1
                vector.append(temp)
        self.feat = np.array(vector)


    def sampleFrame(self):
        fps = self.data['fps']
        fnum = self.data['fnum']

        idx = np.arange(fps, fnum, fps) 
        idx = np.floor(idx)
        idx = idx.tolist()
        idx = map(int, idx)

        img = [self.data['image'][i] for i in idx]
        img_id = [self.data['imgID'][i] for i in idx]
        score = [self.data['score'][i] for i in idx]

        return img, img_id, score
