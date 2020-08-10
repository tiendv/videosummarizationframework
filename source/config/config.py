from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
cfg = __C

BASIC_DIR = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/"

#Params for video test
__C.VIDEO_TEST_PATH = BASIC_DIR + 'test_data/video4test/video.mp4'

#Params for dataset metadata
__C.VIDEO_CSV_PATH = BASIC_DIR + "data/input_data"
__C.VIDEO_CSV_TVSUM_PATH = BASIC_DIR + "data/input_data/TVSum.csv"
__C.VIDEO_CSV_TVSUM_RAW_PATH = BASIC_DIR + "data/input_data/TVSum_RAW.csv"
__C.VIDEO_CSV_SUMME_PATH = BASIC_DIR + "data/input_data/SumMe.csv"
__C.VIDEO_CSV_BBC_PATH = BASIC_DIR + "data/input_data/BBC_EastEnder/BBC_video.csv"
__C.BBC_SHOT_PATH = BASIC_DIR + "/data/input_data/BBC_EastEnder/input_shot"
__C.OUTPUT_PATH = BASIC_DIR + "/data/BBC_processed_data/shot_event"
__C.LOG_DIR_PATH = BASIC_DIR + "source/log"

#params for visualization TVSum50
__C.PATH_VIDEO_TVSUM = "/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video"
__C.PATH_FEATURE_RESNET50_TVSUM= BASIC_DIR + "/data/TVSum_processed_data/frames_feature/resnet50"
__C.PATH_DSF_RESNET50_TVSUM = BASIC_DIR + "/data/TVSum_processed_data/time_segment/res_net50"
__C.PATH_TIME_SHOTS_GT= BASIC_DIR + "data/TVSum_processed_data/time_shots_tvsum50/GT"
__C.PATH_TIME_SHOTS_BL= BASIC_DIR + "data/TVSum_processed_data/time_shots_tvsum50/SuperF"
__C.PATH_TIME_SHOTS_VSUM_DSF_TVSUM = BASIC_DIR + "data/TVSum_processed_data/time_shots_tvsum50/vsum_dsf"
__C.PATH_VIDEOS = BASIC_DIR + "source/src/visualization/static/TVSum50/ydata-tvsum50-v1_1/video"
__C.PATH_KF = BASIC_DIR + "source/src/visualization/static/keyframes/TVSum"
__C.PATH_JSON_KF = BASIC_DIR + "source/src/visualization/static/json/TVSum/kf"
__C.PATH_JSON_SHOT_GT = BASIC_DIR + "source/src/visualization/static/json/TVSum/shots/GT"
__C.PATH_JSON_SHOT_BL = BASIC_DIR + "source/src/visualization/static/json/TVSum/shots/TransNet"
__C.PATH_JSON_SHOT_SUM_DSF_TVSUM = BASIC_DIR + "source/src/visualization/static/json/TVSum/selected/vsum_dsf"
__C.PATH_JSON_SELECT_GT = BASIC_DIR + "source/src/visualization/static/json/TVSum/selected/GT"
__C.PATH_JSON_SELECT_BL = BASIC_DIR + "source/src/visualization/static/json/TVSum/selected/dsf_vgg16_m"
__C.PATH_JSON_EVALUATE = BASIC_DIR + "source/src/visualization/static/evaluation/SuperF"
__C.PATH_EVALUATE_TVSUM = BASIC_DIR + "source/src/visualization/static/evaluation/TVSum"
__C.PATH_GT_TVSUM50 = BASIC_DIR + "source/src/visualization/static/TVSum50/ydata-tvsum50-v1_1/ydata-tvsum50-matlab/matlab/ydata-tvsum50.mat"

#params for visualization BBC
__C.EXAMPLE_BBC_SHOT_PATH = "../../../../test_data/shots/shot1_18.mp4"
__C.EXAMPLE_OUTPUT_PATH = "../../../../test_data/events"

#####----config for segment and score----#####
__C.TRECVID_SHOT_ID_PATH = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/trecvid_shot_id.txt"
__C.SKIPPED_TRECVID_SHOT_PATH = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/skipped_trecvid_shot.txt"
__C.GT_TRECVID_PATH = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/bbc_gt.txt"
__C.VIDEO175_GT = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/video175_vsum_result/video175_GT.txt"


####----VSUM----####
#---------config to run a baseline-----------#
__C.TRECVID_SEGMENT_PATH = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/segment/bbc_seg"
__C.TRECVID_SCORE_PATH = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/score/VASNet_scores"
__C.PATH_TIME_SELECTION_BBC = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/video175_vsum_result"
####
__C.TRECVID_BBC_SEGMENT_PATH = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/segment/bbc_seg/trecvid_bbc_shot.npy"
__C.TRECVID_SEGMENT_JSON_PATH = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC/selected"
__C.PATH_RESULT_VSUM_BBC = BASIC_DIR + "source/src/visualization/static/result/TRECVID_BBC_EastEnders"
#####----config for shot and selection time----#####
__C.PATH_PERSON_SHOTS_BBC = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/bbc_person_segment"
__C.PERSON_SCORE_PATH = BASIC_DIR + "data/BBC_processed_data/VSUM_TRECVID/vsum_scores"
#config for visualization
__C.PATH_TIME_SHOTS_BBC = BASIC_DIR + "data/BBC_processed_data/c3d_scores_first500"
__C.TRECVID_SHOT_JSON_PATH = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC/shots/scores"
__C.TRECVID_EVENT_SHOT_PATH = BASIC_DIR + "/data/BBC_processed_data/shot_event"




__C.PATH_VIDEO_BBC = "/mmlabstorage/datasets/TRECVID/TRECVID_BBC_EastEnders/videos"
__C.PATH_EMOTION_KMEDOIDS_BBC =  BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/emotion_seg_vsum_dsf_fix"
__C.PATH_EVENT_KMEDOIDS_BBC =  BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/event_seg_vsum_dsf_fix"
__C.PATH_DSF_BBC =  BASIC_DIR + "/data/BBC_processed_data/time_shots_bbc/dsf_seg_rgb"
__C.PATH_FEATURE_VGG19_BBC =  BASIC_DIR + "/data/BBC_processed_data/time_shots_bbc/feature/VGG19"
__C.PATH_TIME_SHOTS_BBC_GT= BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/GT"
__C.PATH_TIME_SHOTS_BBC_BL= BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/SBD"
__C.PATH_DATA_REF_BBC_FILE = BASIC_DIR + "data/BBC_processed_data/reference_bbc/master_shot_reference.txt"
__C.PATH_EVENT_SHOT_BBC = BASIC_DIR + "data/BBC_processed_data/events_shot"
__C.PATH_EVENT_EMOTION_BBC = BASIC_DIR + "data/BBC_processed_data/events_emotion"
__C.PATH_EVENT_AUDIO_BBC = BASIC_DIR + "data/BBC_processed_data/audio_event"
__C.PATH_FACES_SHOT_BBC = BASIC_DIR + "data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Faces"
__C.PATH_AUDIO_SHOT_BBC = BASIC_DIR + "data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots_Audios"
__C.PATH_SHOT_BBC = BASIC_DIR + "data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots_VSUM"
__C.PATH_SHOT_BBC_TRECVID = BASIC_DIR + "data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Shots_VSUM"

__C.PATH_TIME_SHOTS_EVENTS_VSUM_DSF_BBC = BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/event_seg_vsum_dsf"
__C.PATH_TIME_SHOTS_RGB_VSUM_DSF_BBC = BASIC_DIR + "data/BBC_processed_data/time_shots_bbc/event_seg_rgb"
__C.PATH_JSON_SELECT_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected"
__C.PATH_JSON_EVENT_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/events"
__C.PATH_JSON_EVENT_EMOTION_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/events_emotion"
__C.PATH_JSON_SHOT_EVENTS_SUM_DSF_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected/event_seg_vsum_dsf"
__C.PATH_JSON_SHOT_RGB_SUM_DSF_BBC = BASIC_DIR + "source/src/visualization/static/json/TRECVID_BBC_EastEnders/selected/dsf_seg_vsum_rgb"

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
__C.PATH_GT_SUMME = BASIC_DIR + "source/src/visualization/static/SumMe/GT"
