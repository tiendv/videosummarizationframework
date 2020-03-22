import os,glob
import argparse

def get_all_shots_detected(path_data):
    files = glob.glob(os.path.join(path_data,"*.txt"))
    data = set()
    for p in files:
        with open(p,'r+') as f:
            for l in f:
                data.add(l)
    data = list(data)
    data.sort(key=lambda x: int(x.split('_')[1]))
    return data


def concat_video_bbc(id_st,id_ed,path_save_result="/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/mergedshots"):
    path_data = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/person_shots"
    path_video = "/mmlabstorage/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots/"
    with open('temp.txt','w') as f:
        for id in range(id_st,id_ed+1):
            data = get_all_shots_detected(os.path.join(path_data,'video{}'.format(id)))
            for d in data:
                path_save = os.path.join(path_video,'video{}'.format(id))
                f.write('file {}.mp4\n'.format(os.path.join(path_save,d.rstrip())))
    # os.system("ffmpeg -f concat -safe 0 -i temp.txt -c copy {}/video{}_{}.mp4".format(path_save_result,id_st,id_ed))
    # os.system("rm temp.txt")
    # print("the result video be saved at {}/videp{}_{}.mp4".format(path_save_result,id_st,id_ed))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('st', type=int,
                    help='ID of the start of video')
    parser.add_argument('en', type=int,
                    help='ID of the end of video')
    args = parser.parse_args()
    concat_video_bbc(args.st,args.en)
