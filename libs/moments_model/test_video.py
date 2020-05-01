"""Test pre-trained RGB model on a single video.

Date: 01/15/18
Authors: Bolei Zhou and Alex Andonian

This script accepts an mp4 video as the command line argument --video_file
and averages ResNet50 (trained on Moments) predictions on num_segment equally
spaced frames (extracted using ffmpeg).

Alternatively, one may instead provide the path to a directory containing
video frames saved as jpgs, which are sorted and forwarded through the model.

ResNet50 trained on Moments is used to predict the action for each frame,
and these class probabilities are average to produce a video-level predction.

Optionally, one can generate a new video --rendered_output from the frames
used to make the prediction with the predicted category in the top-left corner.

"""

import os,glob
import argparse
import moviepy.editor as mpy

import torch.optim
import torch.nn.parallel
from torch.nn import functional as F

import models
from utils import extract_frames, load_frames, render_frames
from multiprocessing import Process
import pickle


def test_model(video_file, save_path,arch="resnet3d50",num_segments=16):
    shot_name = os.path.basename(video_file).split(".")[0]
    vid_name = shot_name.split("_")[0].replace("shot","video")
    path_save = os.path.join(save_path,vid_name,shot_name+".csv")
    print(path_save)
    if os.path.isfile(path_save):
        return

    device = torch.device("cuda")

    # Load model
    model = models.load_model(arch)
    model = model.to(device)

    # Get dataset categories
    categories = models.load_categories()

    # Load the video frame transform
    transform = models.load_transform()

    # Obtain video frames


    # frames = extract_frames(video_file, num_segments)
    try:
        frames = extract_frames(video_file, num_segments)
    except Exception as e:
        os.system("echo {} >> /mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/logs_error_detect.txt".format(video_file))
        return

    # Prepare input tensor
    if arch == 'resnet3d50':
        # [1, num_frames, 3, 224, 224]
        input = torch.stack([transform(frame) for frame in frames], 1).unsqueeze(0)
    else:
        # [num_frames, 3, 224, 224]
        input = torch.stack([transform(frame) for frame in frames])

    input = input.to(device)

    # Make video prediction
    with torch.no_grad():
        logits = model(input)
        h_x = F.softmax(logits, 1).mean(dim=0)
        probs, idx = h_x.sort(0, True)


    if not os.path.isdir(os.path.dirname(path_save)):
        os.makedirs(os.path.dirname(path_save))

    # Output the prediction.
    with open(path_save,'w+') as f:
        for i in range(0, len(probs)):
            f.write('{},{:.3f}\n'.format(categories[idx[i]],probs[i]))

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Optional description')
    # parser.add_argument('st', type=int,
    #                 help='ID of the start of video')
    # parser.add_argument('en', type=int,
    #                 help='ID of the end of video')
    # args = parser.parse_args()
    #
    # main(args.st,args.en)

    # with open("logs_error_detect.txt",'r') as f:
    #     data = f.readlines()
    # # for id,p in enumerate(data[args.st:args.en+1]):
    # #     print(id)
    # #     test_model(p.rstrip())

    test_model("../../data/TRECVID_BBC_EastEnders_Shots/video21/shot21_1575.mp4")
