from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
cfg = __C

#prams for visualization TVSum50
__C.PATH_VIDEOS = "src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video"
__C.PATH_KF = "src/visualization/static/keyframes/TVSum"
__C.PATH_JSON_KF = "src/visualization/static/json/TVSum/kf"
__C.PATH_JSON_SHOT_GT = "src/visualization/static/json/TVSum/shots/GT"
__C.PATH_JSON_SELECT_GT = "src/visualization/static/json/TVSum/selected/GT"
__C.PATH_JSON_SHOT_BL = "src/visualization/static/json/TVSum/shots/BL"
__C.PATH_JSON_SELECT_BL = "src/visualization/static/json/TVSum/selected/BL"

__C.PATH_TIME_SHOTS_GT= "../data/time_shots_tvsum50/GT"
__C.PATH_GT_TVSUM50 = "src/visualization/static/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat"
#prams for visualization BBC
__C.PATH_TIME_SHOTS_BBC= "../../../../data/time_shots_bbc/GT"
__C.PATH_JSON_SELECT_BBC = "../../../src/visualization/static/json/TRECVID_BBC_EastEnders/selected"
