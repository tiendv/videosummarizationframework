import glob, os
import json
import urllib.request
import cv2
import random



path_json = "visualization/static/TRECVID_BBC_EastEnders/videos"

list_json = glob.glob(path_json+"/*.mp4")
for p in list_json:
    file_name = os.path.basename(p).split(".")[0]
    print(file_name)
    vidcap = cv2.VideoCapture(p)
    success,image = vidcap.read()
    count = 0
    k = random.randint(50,500)
    while success:
        if count == k:
            cv2.imwrite("visualization/static/thumbnails_BBC/{}.jpg".format(file_name),image)
            break   # save frame as JPEG file
        success,image = vidcap.read()
        count += 1
