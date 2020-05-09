# How to run a baseline for summarizing a video

### Step 1: Segmenting video into shots
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

### Step 2: Scoring for each shot
 Import module: *from uit.mmlab.vsum.segment import score_shot*
  output: A score list of each shot
* **Random method:**
  Call the function: *segment_shot.random_score(begin_list)*, where begin_list is a begin time list of each shot
### Step3: Selecting shot for summarization using Knapsack0/1
 Import module:  *from uit.mmlab.vsum.selection import select_shot*
 Call the function: *select_shot.do_knapsack(vid_name,begin_list,end_list,score_list,selected_shot_file_path)* 
 where:
       - vid_name -- the name of the input video
       - begin_list -- a begin time list of each shot
       - end_list -- a end time list of each shot
       - score_list -- a score  list of each shot
       - selected_shot_file_path -- the place to save result json
