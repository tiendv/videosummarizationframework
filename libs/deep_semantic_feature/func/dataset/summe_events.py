import simplejson
import numpy as np
import sys,os,glob
import csv
import pandas
from os import listdir
from os.path import isfile, join
import datetime
import time



class SUMME():

    def __init__(self, video_id,fps,feature,fnum,feat_type='vgg'):
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
        dictionary['fps'] = fps
        dictionary['fnum'] = fnum
        dataset = file_json
        data = filter(lambda x: x['videoID'] == video_id, dataset)
        self.data = data[0]
        self.feat = np.array(feature)


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
