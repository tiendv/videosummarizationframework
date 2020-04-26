import datetime
import time

def time2sec(times):
    x = time.strptime(times.split('.')[0],'%H:%M:%S')
    return float(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds() +float(times.split(".")[1])/10000)

path_data = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/time_shots_bbc/dsf_seg_rgb_vgg16/5136783892766027774/5136783892766027774.txt"
total = 0

with open(path_data,"r") as f:
    Lines = f.readlines() 
    for line in Lines:
        total += (time2sec(line.split(" ")[1])-time2sec(line.split(" ")[0]))
print (total)
