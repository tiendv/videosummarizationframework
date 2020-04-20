import os
import argparse

parser = argparse.ArgumentParser(description='Optional description')
parser.add_argument('id_gpu', type=int,help='ID of gpu')
parser.add_argument('id_st', type=int,help='ID of starting video')
parser.add_argument('id_ed', type=int,help='ID of ending video')

args = parser.parse_args()
st = int(args.id_st)
ed = int(args.id_ed)

for i in range(st,ed+1):
    os.system("CUDA_VISIBLE_DEVICES={} python detect_sound.py {}".format(args.id_gpu,i))
