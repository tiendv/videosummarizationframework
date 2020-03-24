import glob,os
path = "/mmlabstorage/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots"

vid = glob.glob(path+"/*")
vid.sort(key=lambda x: int(os.path.basename(x).replace("video","")))
for v in vid:
    shot =  glob.glob(v+"/*")
    print("{},{}".format(os.path.basename(v),len(shot)))
