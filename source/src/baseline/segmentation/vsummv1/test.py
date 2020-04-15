import sys
import os

Datapath = '/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video'
Framepath = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/tvsum50_frames'
outpath = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/time_shots_tvsum50/VSUMM'


if __name__ == "__main__":
    sam = [1, 2, 5, 10, 25, 30]
    for i in sam:
        #print('Sampling rate: ',i)
        cmd ='python Vsumm_test.py '+Datapath+' '+Framepath+' '+outpath+' '+str(i)
        print(cmd)
        os.system(cmd)
