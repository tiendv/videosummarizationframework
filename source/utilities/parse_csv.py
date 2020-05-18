import os
import sys
import pandas as pd

VIDEOSUM_FW_PATH ="/mmlabstorage/workingspace/VideoSum/videosummarizationframework/"
sys.path.append(os.path.join(VIDEOSUM_FW_PATH,'source/config')) #config path append
from config import cfg


def get_metadata(namevid):
    """[Fuction to get metadata of each dataset]

    Args:
        namevid ({string}): [Name of dataset ]

    Returns:
    name_video [string]: [Array of name video]
    path       [string]: [Array of path video data]
    fps        [float64]: [Array of fps]
    nf         [float64]]: [Array of total number frame video]
    duration   [float64]: [Array of duration video]

    Author: thinhplg - 28/04/2020

    """
    namevid = namevid.lower()
    if namevid == 'bbc':
        csvpath = cfg.VIDEO_CSV_BBC_PATH
    elif namevid == 'tvsum':
        csvpath = cfg.VIDEO_CSV_TVSUM_PATH
    elif namevid == 'summe':
        csvpath = cfg.VIDEO_CSV_SUMME_PATH
    else:
        print('Error (parse_csv.py): Check name dataset again')
        sys.exit()
    data = pd.read_csv(csvpath)

    name_video = data.get('name_vid')
    path = data.get('path')
    fps = data.get('fps')
    nf = data.get('nFrames')
    duration = data.get('duration')
    return name_video, path, fps, nf, duration

def main():
    example_datasetname = 'SUmMe'
    name,path,fps,nf,d= get_metadata(example_datasetname)
    #print(name)
    a = name[4:9]
    x = 4
    for idx,video in enumerate(a):
        print(a[idx+x])

if __name__ == '__main__':
    main()
    