#======152=====#
CUDA_VISIBLE_DEVICES=0 python detect_sound.py 1 50 &
CUDA_VISIBLE_DEVICES=1 python detect_sound.py 50 100 &
