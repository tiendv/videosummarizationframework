from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
cfg = __C

#params for visualization TVSum50
__C.PATH_VIDEOS = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video"
__C.PATH_KF = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/keyframes/TVSum"
__C.PATH_JSON_KF = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/kf"
__C.PATH_JSON_SHOT_GT = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/shots/GT"
__C.PATH_JSON_SHOT_BL = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/shots/Random"
__C.PATH_JSON_SHOT_SUM_DSF_TVSUM = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/selected/vsum_dsf"
__C.PATH_JSON_SELECT_GT = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/selected/GT"
__C.PATH_JSON_SELECT_BL = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TVSum/selected/dsf_vgg16_m"
__C.PATH_JSON_EVALUATE = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/evaluation/SuperF"
__C.PATH_EVALUATE_TVSUM = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/evaluation/TVSum"
__C.PATH_TIME_SHOTS_GT= "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/time_shots_tvsum50/GT"
__C.PATH_TIME_SHOTS_BL= "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/time_shots_tvsum50/SuperF"
__C.PATH_TIME_SHOTS_VSUM_DSF_TVSUM = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/time_shots_tvsum50/vsum_dsf"
__C.PATH_GT_TVSUM50 = "/mmlabstorage//workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat"

#params for visualization BBC
__C.PATH_TIME_SHOTS_BBC_GT= "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/time_shots_bbc/GT"
__C.PATH_TIME_SHOTS_BBC_BL= "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/time_shots_bbc/SBD"
__C.PATH_JSON_SELECT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected"
__C.PATH_JSON_EVENT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TRECVID_BBC_EastEnders/events"
__C.PATH_JSON_EVENT_EMOTION_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TRECVID_BBC_EastEnders/events_emotion"
__C.PATH_DATA_REF_BBC_FILE = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/reference_bbc/master_shot_reference.txt"
__C.PATH_EVENT_SHOT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/events_shot"
__C.PATH_EVENT_EMOTION_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/events_emotion"
__C.PATH_EVENT_AUDIO_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/audio_event"
__C.PATH_FACES_SHOT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Faces"
__C.PATH_AUDIO_SHOT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots_Audios"
__C.PATH_SHOT_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots"
__C.PATH_TIME_SHOTS_EVENTS_VSUM_DSF_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/time_shots_bbc/event_seg_vsum_dsf"
__C.PATH_TIME_SHOTS_RGB_VSUM_DSF_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/time_shots_bbc/event_seg_rgb"
__C.PATH_JSON_SHOT_EVENTS_SUM_DSF_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected/event_seg_vsum_dsf"
__C.PATH_JSON_SHOT_RGB_SUM_DSF_BBC = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected/event_seg_vsum_rgb"

#params for SumMe
__C.PATH_TIME_SHOTS_GT_SUMME = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_shots_summe/GT"
__C.PATH_JSON_SELECT_GT_SUMME = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/SumMe/selected/GT"
__C.PATH_JSON_SELECT_BL_SUMME = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/SumMe/selected/dsf_vgg16"

__C.PATH_JSON_SHOT_GT_SUMME = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/SumMe/shots/GT"
__C.PATH_JSON_SHOT_SUM_DSF_SUMME = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/json/SumMe/shots/vsum_dsf"
__C.PATH_TIME_SHOTS_GT_SUMME = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_shots_summe/GT"
__C.PATH_TIME_SHOTS_VSUM_DSF_SUMME = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_shots_summe/vsum_dsf"
__C.PATH_EVALUATE_SUMME = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/source/src/visualization/static/evaluation/SumMe"
