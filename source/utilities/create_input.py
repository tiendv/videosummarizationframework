import glob

def create_input(path,name_file):
    vid_list = glob.glob(path+"/*.mp4")
    vid_list.sort()
    with open("../data/input_list/{}.txt".format(name_file),'w') as f:
        for p in vid_list:
            f.write(p+'\n')
