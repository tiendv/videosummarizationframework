import glob,os


data = glob.glob("/mmlabstorage/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Keyframes_5fps/*")

data.sort(key=lambda x: int(x.split("/")[-1][5:]))
cnt =0
for v in data:
    file_name = v.split("/")[-1]
    with open("frame_input/{}.txt".format(file_name), 'w') as f:
        shots = glob.glob(v+"/*/*.jpg")
        shots.sort(key=lambda x: int(x.split("/")[-1].split("_")[1]))
        for s in shots:
            f.write(s+"\n")
            cnt = cnt + 1
print("Total frames: {}".format(cnt))
