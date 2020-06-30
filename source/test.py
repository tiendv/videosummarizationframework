import glob,os
from config.config import cfg
from uit.mmlab.vsum.visualization import create_json
from utilities.convert_time import time2sec

if __name__ == '__main__':
    path = glob.glob("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/VSUM_TRECVID/bbc_segment_time/twopeak_vasnet_knapsack_150s/*/*.txt")
    total = []
    for p in path:
        with open(p,'r') as f:
            for l in f:
                d = l.split()
                total.append(time2sec(d[2])-time2sec(d[1]))
    print(sum(total)/len(total))
