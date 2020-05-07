"""Calcutate execution time
Author: ThinhplgThinhplg
"""
import time
import cv2

def exec_time_func(func,*args):
    """This function use to calculate execution time for input fuction

    Arguments:
        func {Python Fuction Name} -- The name of the input fuction
        *args -- All parameter for func
    Returns:
        total_time - {float} -- Total execution time
    """
    start_time = time.time()
    func(*args)
    total_time = time.time() - start_time
    return total_time

def exec_time_func_video(videopath,func,*args):
    """This function use to calculate execution time for input function and that function work on a video

    Arguments:
        videopath {[string} -- Path to video. Remind: this video must on the input of `func`
        func {Python Fuction Name} -- The name of the input fuction

    Returns:
        total_time - {float} -- Total execution time
        t1fps - {float} -- Time the input func use to do on 1 frame
    """
    start_time = time.time()
    func(*args)
    total_time = time.time() - start_time
    #read video to get total frame
    nFps = cv2.VideoCapture(videopath).get(cv2.CAP_PROP_FRAME_COUNT)
    #calculate time for exctute 1 frame
    t1fps = total_time/nFps
    return total_time,t1fps

def exec_time_func_videotest(func,*args):
    """This function use to calculate execution time for input function with input is test video

    Arguments:
        func {Python Fuction Name} -- The name of the input fuction

    Returns:
        total_time - {float} -- Total execution time
        t1fps - {float} -- Time the input func use to do on 1 frame
    """
    start_time = time.time()
    func(*args)
    total_time = time.time() - start_time
    #Total frame of video test is 1440. Check it on config file or ../test_data/video4test/video.mp4
    #calculate time for exctute 1 frame
    t1fps = total_time/144
    return total_time,t1fps