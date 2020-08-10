import glob, os
import numpy as np
from config.config import cfg

def evalBBC(pd,gt):
    with open(gt,'r') as f:
        gt_shot = f.read().splitlines()
    with open(pd,'r') as f:
        pd_shot = f.read().splitlines()

    cnt = 0
    ans = []
    for s in pd_shot:
        if s.split()[0] in gt_shot:
            cnt = cnt + 1
            ans.append(s.split()[0])
    print("true:",cnt,ans)
    print("Lenght of pd",len(pd_shot))
    print("Lenght of gt", len(gt_shot))

if __name__ == '__main__':
    evalBBC(os.path.join(cfg.PATH_TIME_SELECTION_BBC,"bbc0.76_vasnetjanine_knapsack80.txt"),cfg.VIDEO175_GT)
