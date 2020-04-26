import sys
import ffmpeg
import numpy as np
import tensorflow as tf
sys.path.append("/mmlabstorage/workingspace/VideoSum/videosummarizationframework/libs/TransNet")
from transnet import TransNetParams, TransNet
from transnet_utils import draw_video_with_predictions, scenes_from_predictions

# initialize the network
params = TransNetParams()
params.CHECKPOINT_PATH = "/mmlabstorage/workingspace/VideoSum/videosummarizationframework/libs/TransNet/model/transnet_model-F16_L3_S2_D256"

net = TransNet(params)

def run_trainsnet(vid_path):
    global net
    video_stream, err = (
        ffmpeg
        .input(vid_path)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(params.INPUT_WIDTH, params.INPUT_HEIGHT))
        .run(capture_stdout=True)
    )
    video = np.frombuffer(video_stream, np.uint8).reshape([-1, params.INPUT_HEIGHT, params.INPUT_WIDTH, 3])
    # predict transitions using the neural network
    predictions = net.predict_video(video)

    scenes = scenes_from_predictions(predictions, threshold=0.1)
    return scenes,scenes[-1][-1]

if __name__ == '__main__':
    shots,total_frame = run_trainsnet('/mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video/-esJrBWj2d8.mp4')
