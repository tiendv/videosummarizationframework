import functools
import os
import re
import subprocess

import numpy as np
from PIL import Image
import time
import cv2


def extract_frames(video_file, num_frames=8):
    """Return a list of PIL image frames uniformly sampled from an mp4 video."""
    id = time.time()
    try:
        os.makedirs(os.path.join(os.getcwd(), 'frames_{}'.format(id)))
    except OSError:
        pass
    output = subprocess.Popen(['ffmpeg', '-i', video_file],
                              stderr=subprocess.PIPE).communicate()
    # Search and parse 'Duration: 00:05:24.13,' from ffmpeg stderr.
    re_duration = re.compile(r'Duration: (.*?)\.')
    duration = re_duration.search(str(output[1])).groups()[0]

    seconds = functools.reduce(lambda x, y: x * 60 + y,
                               map(int, duration.split(':')))
    rate = num_frames / float(seconds)

    output = subprocess.Popen(['ffmpeg', '-i', video_file,
                               '-vf', 'fps={}'.format(rate),
                               '-vframes', str(num_frames),
                               '-loglevel', 'panic',
                               'frames_{}'.format(id)+'/%d.jpg']).communicate()
    frame_paths = sorted([os.path.join('frames_{}'.format(id), frame)
                          for frame in os.listdir('frames_{}'.format(id))])
    frames = load_frames(frame_paths, num_frames=num_frames)
    subprocess.call(['rm', '-rf', 'frames_{}'.format(id)])
    return frames


def load_frames(frame_paths, num_frames=8):
    """Load PIL images from a list of file paths."""
    frames = [Image.open(frame).convert('RGB') for frame in frame_paths]
    if len(frames) >= num_frames:
        return frames[::int(np.ceil(len(frames) / float(num_frames)))]
    else:
        raise ValueError('Video must have at least {} frames'.format(num_frames))


def render_frames(frames, prediction):
    """Write the predicted category in the top-left corner of each frame."""
    rendered_frames = []
    for frame in frames:
        img = np.array(frame)
        height, width, _ = img.shape
        cv2.putText(img, prediction,
                    (1, int(height / 8)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2)
        rendered_frames.append(img)
    return rendered_frames
