from __future__ import print_function
import os
import os.path as osp
import argparse
import sys
import h5py
import datetime
import numpy as np
from tabulate import tabulate

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.optim import lr_scheduler
from torch.distributions import Bernoulli

from models import *

gpu = str(0)
use_cpu = 0
torch.manual_seed(1) # seed
os.environ['CUDA_VISIBLE_DEVICES'] = gpu
use_gpu = torch.cuda.is_available()
if use_cpu: use_gpu = False

def get_DR_DSN_frame_scoring(feature,path_pretrained_model=''):
    if use_gpu:
        print("Currently using GPU {}".format(gpu))
        cudnn.benchmark = True
        torch.cuda.manual_seed_all(1) # seed
    else:
        print("Currently using CPU")

    print("Initialize model")
    model = DSN(in_dim=1024, hid_dim=256, num_layers=1, cell="lstm")
    print("Model size: {:.5f}M".format(sum(p.numel() for p in model.parameters())/1000000.0))
    resume = path_pretrained_model
    print("Loading checkpoint from '{}'".format(resume))
    checkpoint = torch.load(resume)
    model.load_state_dict(checkpoint)


    if use_gpu:
        model = nn.DataParallel(model).cuda()

    with torch.no_grad():
        model.eval()
        seq = feature
        seq = torch.from_numpy(seq).unsqueeze(0)
        if use_gpu: seq = seq.cuda()
        probs = model(seq)
        probs = probs.data.cpu().squeeze().numpy()
        return probs
    
