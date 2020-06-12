import glob, os, h5py
import numpy as np
import pandas as pd

static_folder = "static"
def create_dictionary_tvsum50(path_thumbnails,link_path,matlab_gt):
    f = h5py.File(matlab_gt,'r')
    title_gt = f.get('tvsum50/title')
    data_name = f.get('tvsum50/video')
    list_name = []
    for i in range(data_name.shape[0]):
        name= ''.join(map(chr,f[data_name[i][0]]))
        list_name.append(name)
    list_title = {}
    for i in range(title_gt.shape[0]):
        title= ''.join(map(chr,f[title_gt[i][0]]))
        list_title[list_name[i]]=title
    path_thumbnails = glob.glob(static_folder+"/"+path_thumbnails+"/*")
    path_thumbnails = [file[(len(static_folder)+1):] for file in path_thumbnails]
    data_list = []
    link_video = []
    for i in path_thumbnails :
        link = link_path + i.split("/")[len(i.split("/"))-1].replace('jpg','mp4') + "&para_title=Title:" + ((((list_title[i.split("/")[len(i.split("/"))-1].replace('.jpg','')]).replace(" ","_")).replace("&","and")).replace("+","")).replace("#","")
        link_video.append(link)
    for i in range(len(path_thumbnails)):
        dict_temp = {}
        dict_temp['video'] = link_video[i]
        dict_temp['thumbnail'] = path_thumbnails[i]
        data_list.append(dict_temp)
    return data_list

def create_dictionary_summe(path_videos,path_thumbnails,link_path):
    path_videos = glob.glob(static_folder+"/"+path_videos+"/*.mp4")
    path_videos.sort(key=lambda x: os.path.basename(x).split(".")[0])

    path_thumbnails = glob.glob(static_folder+"/"+path_thumbnails+"*.jpg")
    path_thumbnails.sort(key=lambda x: os.path.basename(x).split(".")[0])

    data_list = []
    link_video = []
    for i in path_videos :
        link = link_path + i.split("/")[len(i.split("/"))-1]
        link_video.append(link)
        for i in range(len(path_thumbnails)):
            dict_temp = {}
            dict_temp['video'] = (link_video[i].replace("static/","")).replace(" ","@")
            dict_temp['thumbnail'] = path_thumbnails[i].replace("static/","")
            data_list.append(dict_temp)
            return data_list

def create_dictionary_bbc(path_videos,path_thumbnails,link_path):
    path_videos = glob.glob(static_folder+"/"+path_videos+"/*.mp4")
    path_videos.sort(key=lambda x: os.path.basename(x).split(".")[0])

    path_thumbnails = glob.glob(static_folder+"/"+path_thumbnails+"*.jpg")
    path_thumbnails.sort(key=lambda x: os.path.basename(x).split(".")[0])

    data_list = []
    link_video = []
    for i in path_videos :
        link = link_path + i.split("/")[len(i.split("/"))-1]
        link_video.append(link)
    for i in range(len(path_thumbnails)):
        dict_temp = {}
        dict_temp['video'] = link_video[i].replace("static/","")
        dict_temp['thumbnail'] = path_thumbnails[i].replace("static/","")
        data_list.append(dict_temp)
    return data_list

def create_bbc_trecvid_dict(path_thumbnails,link_path):
    df = pd.read_csv("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/input_data/BBC_EastEnder/BBC_video.csv")
    data_list = []
    for i in range(175,186) :
        dict_temp = {}
        dict_temp['video'] = link_path+ df.loc[i]['name_vid']
        dict_temp['thumbnail'] = path_thumbnails + df.loc[i]['name_vid'].replace('mp4','jpg')
        data_list.append(dict_temp)
    return data_list

if __name__ == '__main__':
    create_bbc_trecvid_dict("thumbnails_BBC/","/visualTRECVID_BBC_EastEnders?file_id=")
