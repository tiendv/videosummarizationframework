from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
cfg = __C

BASIC_DIR = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/"

#params for visualization TVSum50
__C.PATH_VIDEO_TVSUM = "/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video"
__C.PATH_TIME_SHOTS_GT= BASIC_DIR + "data/TVSum_processed_data/time_shots_tvsum50/GT"
__C.PATH_TIME_SHOTS_BL= BASIC_DIR + "data/TVSum_processed_data/time_shots_tvsum50/SuperF"
__C.PATH_TIME_SHOTS_VSUM_DSF_TVSUM = BASIC_DIR + "data/TVSum_processed_data/time_shots_tvsum50/vsum_dsf"
__C.PATH_VIDEOS = BASIC_DIR + "source/src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video"
__C.PATH_KF = BASIC_DIR + "source/src/visualization/static/keyframes/TVSum"
__C.PATH_JSON_KF = BASIC_DIR + "source/src/visualization/static/json/TVSum/kf"
__C.PATH_JSON_SHOT_GT = BASIC_DIR + "source/src/visualization/static/json/TVSum/shots/GT"
__C.PATH_JSON_SHOT_BL = BASIC_DIR + "source/src/visualization/static/json/TVSum/shots/Random"
__C.PATH_JSON_SHOT_SUM_DSF_TVSUM = BASIC_DIR + "source/src/visualization/static/json/TVSum/selected/vsum_dsf"
__C.PATH_JSON_SELECT_GT = BASIC_DIR + "source/src/visualization/static/json/TVSum/selected/GT"
__C.PATH_JSON_SELECT_BL = BASIC_DIR + "source/src/visualization/static/json/TVSum/selected/dsf_vgg16_m"
__C.PATH_JSON_EVALUATE = BASIC_DIR + "source/src/visualization/static/evaluation/SuperF"
__C.PATH_EVALUATE_TVSUM = BASIC_DIR + "source/src/visualization/static/evaluation/TVSum"
__C.PATH_GT_TVSUM50 = BASIC_DIR + "source/src/visualization/static/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat"

#params for visualization BBC
__C.PATH_VIDEO_BBC = "/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/videos"
__C.PATH_TIME_SHOTS_BBC_GT= BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/GT"
__C.PATH_TIME_SHOTS_BBC_BL= BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/SBD"
__C.PATH_DATA_REF_BBC_FILE = BASIC_DIR + "data/BBC_processed_data/reference_bbc/master_shot_reference.txt"
__C.PATH_EVENT_SHOT_BBC = BASIC_DIR + "data/BBC_processed_data/events_shot"
__C.PATH_EVENT_EMOTION_BBC = BASIC_DIR + "data/BBC_processed_data/events_emotion"
__C.PATH_EVENT_AUDIO_BBC = BASIC_DIR + "data/BBC_processed_data/audio_event"
__C.PATH_FACES_SHOT_BBC = BASIC_DIR + "data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Faces"
__C.PATH_AUDIO_SHOT_BBC = BASIC_DIR + "data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots_Audios"
__C.PATH_SHOT_BBC = BASIC_DIR + "data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots"
__C.PATH_TIME_SHOTS_EVENTS_VSUM_DSF_BBC = BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/event_seg_vsum_dsf"
__C.PATH_TIME_SHOTS_RGB_VSUM_DSF_BBC = BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/event_seg_rgb"
__C.PATH_JSON_SELECT_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected"
__C.PATH_JSON_EVENT_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/events"
__C.PATH_JSON_EVENT_EMOTION_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/events_emotion"
__C.PATH_JSON_SHOT_EVENTS_SUM_DSF_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected/event_seg_vsum_dsf"
__C.PATH_JSON_SHOT_RGB_SUM_DSF_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected/dsf_seg_vsum_rgb"
__C.PATH_RESULT_VSUM_BBC = BASIC_DIR + "source/src/visualization/static/result/TRECVID_BBC_EastEnders"

#params for SumMe
__C.PATH_SUMME_VIDEOS = BASIC_DIR + "source/src/visualization/static/SumMe/videos"
__C.PATH_TIME_SHOTS_GT_SUMME = BASIC_DIR + "data/SumMe_processed_data/time_shots_summe/GT"
__C.PATH_TIME_SEG_RANDOM_SUMME = BASIC_DIR + "data/SumMe_processed_data/time_segment/Random"
__C.PATH_TIME_SHOTS_VSUM_DSF_SUMME = BASIC_DIR + "data/SumMe_processed_data/time_shots_summe/vsum_dsf"
__C.PATH_JSON_SHOT_GT_SUMME = BASIC_DIR + "source/src/visualization/static/json/SumMe/shots/GT"
__C.PATH_JSON_SHOT_RANDOM_SUMME = BASIC_DIR + "source/src/visualization/static/json/SumMe/shots/Random"
__C.PATH_JSON_SHOT_SUM_DSF_SUMME = BASIC_DIR + "source/src/visualization/static/json/SumMe/shots/vsum_dsf"
__C.PATH_JSON_SELECT_GT_SUMME = BASIC_DIR + "source/src/visualization/static/json/SumMe/selected/GT"
__C.PATH_JSON_SELECT_RANDOM_SUMME = BASIC_DIR + "source/src/visualization/static/json/SumMe/selected/Random"
__C.PATH_JSON_SELECT_DSF_VGG16_SUMME = BASIC_DIR + "source/src/visualization/static/json/SumMe/selected/dsf_vgg16"
__C.PATH_EVALUATE_SUMME = BASIC_DIR + "source/src/visualization/static/evaluation/SumMe"
