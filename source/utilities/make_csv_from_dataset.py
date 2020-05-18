"""This script use to create file csv store dataset infomation 
    Field: Name-video, Path-to-video, Fps, Total-frames, Duration
Author: Thinhplg 07/05/2020
"""
import csv
import os 
import cv2 as cv
import sys

sys.path.append('../config')
from config import cfg
from check_permission import check_permission_to_write
import argparse

def make_args():
    """Fuction to define arguments
    """    
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()


    new_dataset = subparsers.add_parser(
        '+newdataset', help='To create csv file for new dataset')
    new_dataset.add_argument(
        'datasetname', action='store',type=str, help='Name of dataset')
    new_dataset.add_argument(
        'datapath', action='store',type=str, help='The directory to folder store all videos')
    new_dataset.add_argument(
        'output', action='store',type=str, help='The directory to save result file')

    parser.add_argument('-bbc', action='store_true',
                        default=False,
                        dest='bbc',
                        help='Flat to run for BBC EastEnders dataset')

    parser.add_argument('-tvsum', action='store_true',
                        default=False,
                        dest='tvsum',
                        help='Flat to run for TVSum dataset')
    parser.add_argument('-summe', action='store_true',
                        default=False,
                        dest='summe',
                        help='Flat to run for SumMe dataset')
    args = parser.parse_args()
    return args

def make_csv_from_data(dataset_name,path_data,output):
    """This function to make file csv store dataset metadata

    Arguments:
        dataset_name {[string]} -- [The name of dataset]
        path_data {[string]} -- [Path to folder storage video]
        output {[string]} -- [Path to save result file]
    """
    with open(output+'/'+dataset_name+'.csv', 'w', newline='') as file:
        print(output+'/'+dataset_name+'.csv')
        fieldnames = ['name_vid','path','fps','nFrames','duration']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        filenames = [f for f in os.listdir(path_data) if f.endswith('.mp4')]
        filenames.sort(key = lambda f: os.path.splitext(os.path.basename(f))[0])
        for name in filenames:
            path = path_data+'/'+name
            cap = cv.VideoCapture(path)
            length = (cap.get(cv.CAP_PROP_FRAME_COUNT))
            fps = (cap.get(cv.CAP_PROP_FPS))
            duration = float(length)/float(fps)
            writer.writerow({'name_vid':name,'path':path,'fps':fps,'nFrames':length,'duration':duration})
    file.close()

def main():
    args = make_args()
    #check if have new dataset
    if len(vars(args))>3:
        make_csv_from_data(args.datasetname,args.datapath,args.output)
    else:
        if args.bbc is True:
            dn = 'BBC'
            dp = cfg.PATH_VIDEO_BBC
            out = cfg.VIDEO_CSV_PATH
        elif args.tvsum is True:
            dn = 'TVSum'
            dp = cfg.PATH_VIDEO_TVSUM
            out = cfg.VIDEO_CSV_PATH
        elif args.summe is True:
            dn = 'SumMe'
            dp = cfg.PATH_VIDEO_SUMME
            out = cfg.VIDEO_CSV_PATH
        else:
            print("Error: Unable to identify the arguments, Check input arguments again!!!!")
            sys.exit()
        if check_permission_to_write(out) is False:
            sys.exit()
        print('Make file csv for dataset: ',dn)
        make_csv_from_data(dn,dp,out)

if __name__ == "__main__":
    main()
