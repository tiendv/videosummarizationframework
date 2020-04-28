from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
cfg = __C

BASIC_DIR = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/"

__C.SAMPLING_RATE = 5
__C.FRAMES_DIR_PATH = BASIC_DIR + "data/BBC_processed_data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Keyframes_5fps"
__C.INPUT_BBC_SHOT_PATH = BASIC_DIR + "data/input_data/BBC_EastEnder/input_shot"
__C.LOG_DIR_PATH = BASIC_DIR + "source/log"
__C.EXAMPLE_VIDEO = "test_data/input/video1/shot1_18.mp4"
__C.EXAMPLE_FRAME_PATH = "test_data/keyframes"
