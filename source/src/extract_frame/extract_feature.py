"""
Code Feature Extract VGG-ResNet-Inception-FisherVector
Version: 0.2
Author: ThinhPLG - 29/04/2020
++++++++++++++++++++++++++++++
Log update:
    +Add class extract feature video: use for input is a video
    +Modify old class ExtractFeature to ExtractFeatureDataSet
"""

import sys
import tensorflow as tf
import os
import numpy as np
import cv2 
from PIL import Image
from tqdm import tqdm
import logging

from keras.preprocessing import image
from keras.applications import vgg16,vgg19,resnet,inception_v3,resnet_v2
from keras.models import Model
from keras.layers import Layer

VIDEOSUM_FW_PATH ="/mmlabstorage/workingspace/VideoSum/videosummarizationframework/"
sys.path.append(os.path.join(VIDEOSUM_FW_PATH,'source/config')) #config path append
sys.path.append(os.path.join(VIDEOSUM_FW_PATH,'source/utilities'))
from config import cfg
from check_permission import check_permission_to_write
from parse_csv import get_metadata

#ExtractFeatureDataSet
#make log file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=os.path.join(VIDEOSUM_FW_PATH,'source/log','feature-extract-log.txt'),
                    filemode='a')

class Feature:
    def __init__(self,feat,name,method,sampling_rate):
        self.feature = feat
        self._sampling_rate=sampling_rate
        self._method = method
        self._namefile=name
        
    def save(self,output_path):
        #Write feature data to file
        if check_permission_to_write(output_path) is False:
            return
        try:
            self.__write_to_file_npy(output_path,self._namefile,self.feature)
        except:
            print("Error try to extract feature before save")

    def __write_to_file_npy(self,output_path,name,data):
        path = os.path.join(output_path,self._method+'_'+
                            name+'_'+str(self._sampling_rate)+'.npy')
        np.save(path,data)
        print("Video: %s with sampling rate %d is save at %s"%(name,self._sampling_rate,path))

class ExtractFeatureVideo(Feature):
    def __init__(self,path_video,sampling_rate=1,device_name='GPU:0'): 
        """[init fuction]

        Arguments:
            Feature {class}
            path_video {string} -- [path to video]

        Keyword Arguments:
            sampling_rate {int} -- [Sampling rate] (default: {1})
            device_name {str} -- [Device name to use]] (default: {'GPU:0'})
        """        
        self._path = path_video
        self._namevideo = os.path.basename(path_video)
        self._namefile = os.path.splitext(self._namevideo)[0]
        self._device = '/device:'+device_name
        self._sampling_rate = sampling_rate

    def VGG19(self,output_layer='fc2'):
        """VGG1() - fc2 - output_shape = 4096
        """
        self.method = 'vgg19'
        base_model = vgg19.VGG19(weights='imagenet')
        _model = Model(input=base_model.input, output=base_model.get_layer(output_layer).output)
        _model.summary()
        self.imageSize = (224,224)
        self.model = _model
        self.preinput = vgg19.preprocess_input
        return self._process()

    def VGG16(self,output_layer='fc2'):
        """VGG16 - fc2 - output_shape = 4096
        """
        self.method = 'vgg16'
        base_model = vgg16.VGG16(weights='imagenet')
        _model = Model(input=base_model.input, output=base_model.get_layer(output_layer).output)
        _model.summary()
        self.imageSize = (224,224)
        self.model = _model
        self.preinput = vgg16.preprocess_input
        return self._process()

    def ResNet50(self,output_layer='avg_pool'):
        """ResNet50 - avg_pool - output_shape = 2048
        """
        self.method = 'resnet50'
        base_model = resnet.ResNet50(weights='imagenet')
        _model = Model(input=base_model.input, output=base_model.get_layer(output_layer).output)
        _model.summary()
        self.imageSize = (224,224)
        self.model = _model
        self.preinput = resnet.preprocess_input
        return self._process()

    def ResNet152(self,output_layer='avg_pool'):
        """ResNet152 - avg_pool - output_shape = 2048
        """
        self.method = 'resnet152'
        base_model = resnet.ResNet152(weights='imagenet')
        _model = Model(input=base_model.input, output=base_model.get_layer(output_layer).output)
        _model.summary()
        self.imageSize = (224,224)
        self.model = _model
        self.preinput = resnet.preprocess_input
        return self._process()

    def InceptionV3(self,output_layer='avg_pool'):
        """ResNet50 - avg_pool - output_shape = 1024
        """
        self.method = 'inceptionv3'
        base_model = inception_v3.InceptionV3(weights='imagenet')
        _model = Model(input=base_model.input, output=base_model.get_layer(output_layer).output)
        _model.summary()
        self.imageSize = (299,299)
        self.model = _model
        self.preinput = inception_v3.preprocess_input
        return self._process()
    
    def InceptionV1(self,output_layer = 'pool5'):
        self.method = 'inceptionv3'
        pass

    def _process(self):
        """Fuction for run process
        Check input is video folder or frame folder
        """
        try:
            with tf.device(self._device):
                feat = self.__process_video()
        except RuntimeError as e:
            logging.error(e)
        return Feature(feat,self._namefile,self.method,self._sampling_rate)

    def __process_video(self):
        print("%s with sampling rate is %d"%(self._namevideo,self._sampling_rate))
        vidcap = cv2.VideoCapture(self._path)
        if (vidcap.isOpened()== False):
            #check opened?
            logging.error("Fail to open video %s"%(video))
        sam = self._sampling_rate
        nFrame = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        pbar = tqdm(total = nFrame)
        it = 0
        feat = []
        while(vidcap.isOpened()):
            pbar.update(1)
            suc, img = vidcap.read()
            it+=1
            if(suc == False):
                break
            if ((it-1)%sam) != 0:
                continue
            _feature = self.__extract(img)
            feat.append(_feature)
        res = np.asarray(feat)
        #self.feature = np.squeeze(res)
        res = np.squeeze(res)
        return res# self.feature

    def __extract(self,input_image):
        #Extract feature from image                    
        img = Image.fromarray(input_image)
        img = img.resize(self.imageSize)
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = self.preinput(img_data)
        _feature = self.model.predict(img_data)
        return _feature


class ExtractFeatureDataSet(ExtractFeatureVideo):
    def __init__(self,dataset_name,output_path,sampling_rate=1,device_name='GPU:0'): 
        """[Init fuction]]

        Arguments:
            ExtractFeatureVideo {class}
            dataset_name {sting} -- [Name dataset to extract] (BBC,TVSUM,SUMME)
            output_path {string} -- [Path for save extracted file]

        Keyword Arguments:
            sampling_rate {int} -- [Sampling rate] (default: {1})
            device_name {str} -- [Device to run] (default: {'GPU:0'})
        """        
        #super().__init__(sampling_rate=sampling_rate,device_name=device_name)
        self.dataset = dataset_name
        self.output = output_path
        self.device = '/device:'+device_name
        self.samplingRate = sampling_rate
        if check_permission_to_write(self.output) is False:
            sys.exit()

    def _process(self):
        """Fuction for run process
        Check input is video folder or frame folder
        """
        try:
            with tf.device(self.device):
                self.__process_video()
        except RuntimeError as e:
            logging.error(e)

    def __process_video(self):
        videoName,videoPathLists,_,nFrame,_ = self._read_meta_data()
        for idx,video in enumerate(videoName):
            feat = []
            print("%s/%s : %s with sampling rate is %d"%(idx+1,len(videoName),video,self.samplingRate))
            path = videoPathLists[idx]
            vidcap = cv2.VideoCapture(path)
            if (vidcap.isOpened()== False):
                #check opened?
                logging.error("Fail to open video %s"%(video))
            sam = self.samplingRate
            pbar = tqdm(total = nFrame[idx])
            it = 0
            while(vidcap.isOpened()):
                pbar.update(1)
                suc, img = vidcap.read()
                it+=1
                if(suc == False):
                    break
                if ((it-1)%sam) != 0:
                    continue
                _feature = self.__extract(img)
                feat.append(_feature)
            result = np.asarray(feat)
            result = np.squeeze(result)
            namefile = os.path.splitext(os.path.basename(video))[0]
            self._write_to_file(namefile,result)

    def _read_meta_data(self):
        #read data from file csv
        dn = self.dataset   #dataset name
        if dn == 'bbc' or dn =='BBC' or dn == 'BBC EastEnders':
            namevid,path,fps,nFrame,duration = get_metadata('bbc')
        elif dn == 'summe' or dn =='SumMe' or dn == 'SUMME':
            namevid,path,fps,nFrame,duration = get_metadata('summe')
        else:
            namevid,path,fps,nFrame,duration = get_metadata(dn)

        return namevid,path,fps,nFrame,duration

    def _write_to_file(self,name,data):
        #Write feature data to file
        self.__write_to_file_npy(name,data)

    def __write_to_file_npy(self,name,data):
        path = os.path.join(self.output,self.method+'_'+
                            name+'_'+str(self.samplingRate)+'.npy')
        np.save(path,data)
        logging.info("Dataset: %s Video: %s with sampling rate %d is save at %s"%(self.dataset,name,self.samplingRate,path))

    def __extract(self,input_image):
            #Extract feature from image                    
        img = Image.fromarray(input_image)
        img = img.resize(self.imageSize)
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = self.preinput(img_data)
        _feature = self.model.predict(img_data)
        return _feature
def main():
    #Example for runing
    feat = ExtractFeatureVideo('./test.mp4',20).VGG16()
    feat.save('./')
    #data = ExtractFeatureDataSet('tvsum','./',sampling_rate=50).VGG16()


if __name__ == '__main__':
    main()
    