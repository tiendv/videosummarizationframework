import glob,os
from config.config import cfg
from uit.mmlab.vsum.visualization import create_json
from utilities.convert_time import time2sec
import numpy as np
if __name__ == '__main__':
    shot_data = [(2,2),(4,0),(1,11),(6,777),(9,9),(7,75)]

    sorted_idx = [i[0] for i in sorted(enumerate(shot_data), key=lambda x: x[1][0])]

    print(sorted_idx)
