import glob,os
from config.config import cfg
from uit.mmlab.vsum.visualization import create_json
from utilities.convert_time import time2sec
import numpy as np
if __name__ == '__main__':
    score = np.load("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/VSUM_TRECVID/vsum_scores/janine/video175.npy")
    with open("./175_janine_score.txt",'w') as f:
        for s in score:
            f.write("{}\n".format(s))
