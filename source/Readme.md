# How to run a baseline for summarizing a video

### Segmenting video into shots
Output: - video_name -- the name of the input video
        - begin_list --  a begin time list of each shot
        - endn_list --  a end time list of each shot
        
Import module: *from uit.mmlab.vsum.segment import segment_shot*
* **Sampling method:**
  
  Call the function: *segment_shot.sampling_shot(vid_path,shot_len=2)*, where vid_path is a input video path and shot_len is the length of each shot
* **Superframe method:**

  Call the function: *segment_shot.do_superframe(vid_path)*, where vid_path is a input video path 
* **Transnet method**

  Call the function: *segment_shot.do_transnet(vid_path)*, where vid_path is a input video path

### Scoring for each shot
 Import module: *from uit.mmlab.vsum.segment import score_shot*
 
* **Random method:**
  output: A score list of each shot
  Call the function: * segment_shot.random_score(begin_list)*, where begin_list is a begin time list of each shot
