from easydict import EasyDict as edict

__C = edict()
# Consumers can get config by:
cfg_ef = __C

BASIC_DIR = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/"

#Params for video test
__C.VIDEO_TEST_PATH = BASIC_DIR + 'test_data/video4test/video.mp4'
#Params for dataset metadata
__C.VIDEO_CSV_PATH = BASIC_DIR + "data/input_data"
__C.VIDEO_CSV_TVSUM_PATH = BASIC_DIR + "data/input_data/TVSum.csv"
__C.VIDEO_CSV_SUMME_PATH = BASIC_DIR + "data/input_data/SumMe.csv"
__C.VIDEO_CSV_BBC_PATH = BASIC_DIR + "data/input_data/BBC_EastEnder/BBC_video.csv"
__C.BBC_SHOT_PATH = BASIC_DIR + "/data/input_data/BBC_EastEnder/input_shot"
__C.OUTPUT_PATH = BASIC_DIR + "/data/BBC_processed_data/shot_event"
__C.LOG_DIR_PATH = BASIC_DIR + "source/log"


#Params for disable tensorflow debugging information
__C.TENSORFLOW_DEBUGGING_CODE = '3'
	
"""	0 = all messages are logged (default behavior)
	1 = INFO messages are not printed
	2 = INFO and WARNING messages are not printed
	3 = INFO, WARNING, and ERROR messages are not printed
"""
#Params for choose CNN
__C.NAME_CNN = 'inceptionv1'
__C.LAYER_CNN = None

#Params for ExtractFeartureDataSet
__C.DATASET_NAME = 'tvsum'     #bbc or summe or tvsum
__C.DATASET_OUTPUT_PATH= '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/frames_feature/inceptionv1'
__C.DATASET_FROM_VIDEO = None
__C.DATASET_TO_VIDEO = None
__C.DATASET_SAMPLING_RATE = 1
__C.DATASET_DEVICE_NAME = '0'

#Params for ExtractFeartureVideo
__C.VIDEO_PATH = '/mmlabstorage/datasets/SumMe/videos/Air_Force_One.mp4'
__C.VIDEO_SAMPLING_RATE = 1
__C.VIDEO_DEVICE_NAME = '0'
__C.VIDEO_OUTPUT_PATH = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/test_data'

#Params for ExtractFeartureImages
__C.IMAGES_FOLDER = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/test_data/keyframes/video1/shot1_18'
__C.IMAGES_OUTPUT_PATH = '/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/test_data'
__C.IMAGES_SAMPLING_RATE = 1
__C.IMAGES_DEVICE_NAME = '0'