import sys

import argparse
import cv2
import os
import errno
import glob

import time

def KeyframeExtraction(input_path, output_path, sampling_rate=None, max_frame_per_shot=None):
    #************************************************************************
    # Purpose: Extract keyframes from a video file
    # Inputs:
    # - input_path: path to video file
    # - output_path: directory path to store keyframes
    # - sampling_rate: the number of frames per second
    # - max_frame_per_shot: if this is set, the numbers of keyframes extracted must satisfied this value
    # Returns: None
    # Author: Hung Vo
    # Modified: Dugmn
    #************************************************************************

    cap = cv2.VideoCapture(input_path)
    origin_fps = cap.get(cv2.CAP_PROP_FPS)
    if max_frame_per_shot is not None:
        sampling_rate = max_frame_per_shot * cap.get(cv2.CAP_PROP_FPS) / cap.get(cv2.CAP_PROP_FRAME_COUNT)

    if sampling_rate is not None:
        # coef = round(fps / sampling_rate)
        coef = round(25 / sampling_rate)


    shotname = input_path.split('/')[-1].split('.')[0]
    videoname = shotname.split('_')[0].replace("shot","video")

    directory_path = os.path.join(output_path,videoname, shotname)

    try:
        os.makedirs(directory_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            if (sampling_rate is None) or (index % coef == 0):
                # cv2.imwrite(os.path.join(directory_path, str(
                #     label).zfill(5) + '.jpg'), frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                cv2.imwrite(os.path.join(directory_path,"{}_frame_{}_.jpg".format(shotname,round(index/origin_fps,2))), frame)
        else:
            break
        index += 1
    cap.release()
    cv2.destroyAllWindows()

def run_extract(id):
    frames_folder = "/mmlabstorage/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Keyframes_5fps/"
    total_time = 0
    extracted_shot = 0
    with open("shot_input/video{}.txt".format(id)) as f:
        data = f.readlines()

    for shot in data:
        shot = shot.rstrip()
        video_id = os.path.basename(shot).split('_')[0][4:]

        # Check if there is no free space on hard disk
        statvfs = os.statvfs('/')
        if statvfs.f_frsize * statvfs.f_bavail / (10**6 * 1024) < 5:
            print(
                '\033[93mWarning: Stop process. There is no free space left!\033[0m')
            break

        begin = time.time()
        KeyframeExtraction(shot, frames_folder, 5)
        end = time.time()

        total_time += (end - begin)

        extracted_shot += 1
        # print('[+] Number of extracted shots: %d' % (extracted_shot))

        os.system("echo {} >> ../../logs/extract_frame_log.txt".format(shot))
        # print('Total Elapsed Time: %f minutes and %d seconds' % (
        # total_time/60, total_time % 60))

def main():
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('id', type=int,
                    help='ID of input video')
    args = parser.parse_args()

    run_extract(args.id)

if __name__ == '__main__':
    # main()
    KeyframeExtraction("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/test_data/input/video1/shot1_18.mp4","/mmlabstorage/workingspace/VideoSum/videosummarizationframework/test_data/keyframes",sampling_rate=5)
