import time
import os
import sys

sys.path.append('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/')

from videoSumSIFT import runSIFT
from config.config import cfg
from utilities.convert_time import sec2time

path_out = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data'

bbc =['/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/videos',path_out+'/BBC_processed_data/time_shots_bbc/SIFT']
tvsum = ['/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video',path_out+'/TVSum_processed_data/time_shots_tvsum50/SIFT']
path_out = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data'

dic = {'bbc':bbc,'tvsum':tvsum,'summe':summe}
_input = sys.argv[1]



data_path = dic[_input][0]
output_path = dic[_input][1]
print(data_path,output_path)

listnames =[f for f in os.listdir(data_path) if f.endswith(".mp4")]

def write_to_file(file_name,out_dir,list_begin,list_end,score,fps):
    #file name without extension
    fName_no_ex=os.path.splitext(file_name)[0]

    #path output folder
    path = os.path.join(out_dir,fName_no_ex)
    if os.path.exists(path) is False:
        os.mkdir(path)
    list_begin = [sec2time(i/fps) for i in list_begin]
    list_end = [sec2time(i/fps) for i in list_end]
    with open(os.path.join(path,fName_no_ex+'.txt'), 'a') as the_file:
        for i in range(0,len(list_begin)):
            the_file.write(str(list_begin[i])+' '+str(list_end[i])+' '+str(score[i])+'\n')


if __name__ == "__main__":
    for idx,name in enumerate(listnames):
        print("++++++++++++++++++++++++++++++++")
        print( "%s/%s: %s" % (idx+1,len(listnames),name))
        start_time = time.time()
        path = os.path.join(data_path,name)
        list_begin,list_end,score,fps,nFrames = runSIFT(path)
        write_to_file(name,output_path,list_begin,list_end,score,fps)
        print("--- %s seconds ---" % (time.time() - start_time))
