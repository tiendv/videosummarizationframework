rethinking-evs
==============================

[Original code](https://github.com/mayu-ot/rethinking-evs) - Scripts of CVPR'19 paper "Rethinking the Evaluation of Video Summaries" [[arXiv](https://arxiv.org/abs/1903.11328)]

### Create docker images base on Dockerfile
Accessing the working directory: 
[rethinking-evs](https://github.com/tiendv/videosummarizationframework/tree/master/source/src/baseline/rethinking-evs)

Download Dockerfile : "Dockerfile_random_method" [[Dockerfile](https://drive.google.com/drive/u/1/folders/1xSGkUZpzZ8TjCthL-kgvtj77WIY_FOhc)]

Build images: `docker build -t Name_image:Tag_image -f Dockerfile .`

- Ex: `docker build -t rethinking-evs:v1 -f Dockerfile_random_method .`

Create container:

- Ex: `docker run --name rethinking --runtime=nvidia -v /mmlabstorage:/mmlabstorage -it rethinking-evs:v1 bash`

# Data
Optional: For KTS segmentation results provided [here](https://github.com/kezhang-cs/Video-Summarization-with-LSTM).

Convet boundaries of video to name_video.npy
### Input
    
- Path of folder information of dataset (' .csv')

- Path of folder boundaries (' .npy')

- Path save output

### Run code
Accessing the working directory: 
[rethinking-evs](https://github.com/tiendv/videosummarizationframework/tree/master/source/src/baseline/rethinking-evs)

-   BBC dataset: `0: video_id starting || 244: video_id ending || uniform: method(one-peak or two-peak or KTS or randomized-KTS or uniform) || 'bbc': set dataset to get real_name video.`

Ex: `python random_method.py 0 244 uniform bbc`

-   TVSum dataset: `no need video_id starting and ending.`

Ex: `python random_method.py 0 244 KTS tvsum`

-   SumMe dataset: `no need video_id starting and ending.`

Ex: `python random_method.py 0 244 randomized-KTS summe`
### Output
```
<time_start>        <time_end>
<HH:MM:SS:FFFF>     <HH:MM:SS:FFFF>
00:00:14.0144       00:00:16.0164
00:00:28.0288       00:00:30.0308
00:00:38.0390       00:00:40.0411
00:00:58.0596       00:01:02.0637
```
