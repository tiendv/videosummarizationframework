import hdf5storage
import numpy as np
from config.config import cfg
from uit.mmlab.vsum.visualization import create_json

def preprocess():
    with open("dppLSTM",'r') as f:
        data = f.readlines()
    data = list(map(lambda x: list(map(float,x.split()))[:-1],data))
    data = np.array(data)
    f1s = data[:,0]
    rcs = data[:,1]
    pres = data[:,2]

    f = hdf5storage.loadmat(cfg.PATH_GT_TVSUM50, variable_names=['tvsum50'])
    tvsum_data = f['tvsum50'].ravel()
    vid_names = []
    for item in tvsum_data:
        video,_,_,_,_,_,_ = item
        vid_names.append(video[0,0])
    return vid_names,pres,rcs,f1s

def main():
    vid_names,precisions,recalls,fscores = preprocess()
    create_json.write_eval_result(cfg.PATH_EVALUATE_TVSUM,'KTS_dppLSTM_Knapsack',vid_names,precisions,recalls,fscores)

main()
