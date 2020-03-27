from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
cfg = __C

#prams for visualization TVSum50
__C.PATH_VIDEOS = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video"
__C.PATH_KF = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/keyframes/TVSum"
__C.PATH_JSON_KF = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/kf"
__C.PATH_JSON_SHOT_GT = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/shots/GT"
__C.PATH_JSON_SELECT_GT = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/selected/GT"
__C.PATH_JSON_SHOT_BL = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/shots/BL"
__C.PATH_JSON_SELECT_BL = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/selected/BL"

__C.PATH_TIME_SHOTS_GT= "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/time_shots_tvsum50/GT"
__C.PATH_GT_TVSUM50 = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/visualization/static/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat"

#prams for visualization BBC
__C.PATH_TIME_SHOTS_BBC= "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/time_shots_bbc/GT"
__C.PATH_JSON_SELECT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected"
__C.PATH_JSON_EVENT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TRECVID_BBC_EastEnders/events"
__C.PATH_DATA_REF_BBC_FILE = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/reference_bbc/master_shot_reference.txt"
__C.PATH_EVENT_SHOT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/events_shot"
__C.PATH_FACES_SHOT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Faces"
