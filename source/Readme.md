# How to run a baseline for summarizing a video

### Segmenting video into shots
Import module: *from uit.mmlab.vsum.segment import segment_shot*
* Sampling method:

  Call the function: *segment_shot.sampling_shot(vid_path,shot_len=2)*, where vid_path is a input video path and shot_len is the length of each shot
* Superframe method:

  Call the function: *segment_shot.do_superframe(vid_path)*, where vid_path is a input video path 
* Transnet method

  Call the function: *segment_shot.do_transnet(vid_path)*, where vid_path is a input video path
