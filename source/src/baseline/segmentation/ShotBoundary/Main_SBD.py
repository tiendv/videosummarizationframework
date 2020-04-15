import time
import os
import sys
sys.path.append('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/')

from ShotBoundaryDetection import ShotBoundaryDetection
from config.config import cfg
from utilities.convert_time import sec2time

##Path of data-set and output
path_out = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data'
bbc =['/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/videos',path_out+'/BBC_processed_data/time_shots_bbc/SBD']
tvsum = ['/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video',path_out+'/TVSum_processed_data/time_shots_tvsum50/SBD']
summe = ['/mmlabstorage/datasets/SumMe/videos',path_out+'/SumMe_processed_data/time_shots_summe/SBD']

dic = {'bbc':bbc,'tvsum':tvsum,'summe':summe}

#input name of dataset
_input = sys.argv[1]

data_path = dic[_input][0]
output_path = dic[_input][1]
print(data_path,output_path)

listnames =[f for f in os.listdir(data_path) if f.endswith(".mp4")]

def write_to_file(file_name,out_dir,nFrame,fps,list_begin,list_end):
    #check folder output is exist
    fName_no_ex=os.path.splitext(file_name)[0]
    path = os.path.join(out_dir,fName_no_ex)
    if os.path.exists(path) is False:
        os.mkdir(path)
    
    if(list_end[len(list_end)-1]==-1):
        list_end[len(list_end)-1]=nFrame
    
    for i in range(0,len(list_end)):
        #check if list_end==-1 mean list_begin have infomation of frame of SHOT CUT
        if list_end[i]==-1:
            list_end[i]=list_begin[i+1]-1
        list_begin[i]=sec2time(list_begin[i]/fps)
        list_end[i]=sec2time(list_end[i]/fps)
    with open(os.path.join(path,fName_no_ex+'.txt'), 'a') as the_file:
        for i in range(0,len(list_begin)):
            the_file.write(str(list_begin[i])+' '+str(list_end[i])+' '+str(1)+'\n')

if __name__ == "__main__":
    for idx,name in enumerate(listnames):
        print( "%s/%s: %s" % (idx+1,len(listnames),name))
        start_time = time.time()
        sbd = ShotBoundaryDetection()
        path = os.path.join(data_path,name)
        sbd.open_video(path)
        nF,fps=sbd.get_total_frame_and_fps()
        list_begin,list_end = sbd.detect()
        write_to_file(name,output_path,nF,fps,list_begin,list_end)
        print("--- %s seconds ---" % (time.time() - start_time))
