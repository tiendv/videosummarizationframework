 
import time
import os
import sys
sys.path.append('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/')

#from ShotBoundaryDetection import ShotBoundaryDetection
#from config.config import cfg
#from utilities.convert_time import sec2time

##Path of data-set and output
path_out = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data'
bbc =['/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/videos',path_out+'/BBC_processed_data/time_shots_bbc/VSUMMv2']
tvsum = ['/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video',path_out+'/TVSum_processed_data/time_shots_tvsum50/VSUMMv2']
summe = ['/mmlabstorage/datasets/SumMe/videos',path_out+'/SumMe_processed_data/time_shots_summe/VSUMMv2']

dic = {'bbc':bbc,'tvsum':tvsum,'summe':summe}

#input name of dataset
_input = sys.argv[1]

data_path = dic[_input][0]
output_path = dic[_input][1]
print(data_path,output_path)

listnames =[f for f in os.listdir(data_path) if f.endswith(".mp4")]

if __name__ == "__main__":
    #percent defaults to 1/100 of video length
    percent = str(15)
    sampling_rate =[5,30,15,2,1]
    for sam in sampling_rate:
        #make folder name sampling rate
        p = os.path.join(output_path,str(sam))
        if os.path.exists(p) is False:
            os.mkdir(p)
        #run 
        for idx,name in enumerate(listnames):
            path = os.path.join(data_path,name)
            print( "%s: %s   %s/%s: %s" % ('Sampling-rate',sam,idx+1,len(listnames),name))
            cmd = 'python vsumm_feat.py '+path+' '+str(sam)+' '+percent+' 0 0 1 '+p+' '+'cnn_reduced'
            try:
                os.system(cmd)
            except:
                pass
