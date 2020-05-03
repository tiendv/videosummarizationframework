# Deep semantic feature and K-medoids
[Original code](https://github.com/mayu-ot/vsum_dsf) - "Video Summarization using Deep Semantic Features" in ACCV'16-[[arXiv](https://arxiv.org/abs/1609.08758)]
### Create docker images base on Dockerfile
Accessing the working directory: 
[deep_semantic_feature](https://github.com/tiendv/videosummarizationframework/tree/master/source/src/baseline/deep_semantic_feature)

Build images: `docker build -t Name_image:Tag_image -f Dockerfile .`

- Ex: `docker build -t deep_semantic_feature:v1 -f Dockerfile .`

Create container:

- Ex: `docker run --name dsf_kemdoids --runtime=nvidia -v /mmlabstorage:/mmlabstorage -it deep_semantic_feature:v1 bash`
# Deep semantic feature
### Input
- Path of folder extract feature from video with vgg or resnet (' .npy'):

`/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/frames_feature/VGG16`

- Path of folder information of dataset (' .csv'):

`/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/input_data/SumMe.csv`

- Path save output:

`/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_segment/vsum_dsf`

### Output
```
<time_start>        <time_end>
<HH:MM:SS:FFFF>     <HH:MM:SS:FFFF>
00:00:04.0000       00:00:08.0000
00:00:35.0000       00:00:39.0000
00:00:52.0000       00:00:56.0000
00:01:31.0000       00:01:35.0000
```
### Run code: 
Accessing the working directory :
[deep_semantic_feature](https://github.com/tiendv/videosummarizationframework/tree/master/source/src/baseline/deep_semantic_feature)

-   BBC dataset: `0: video_id starting || 244: video_id ending || 4: length uniform segment || 'smt_feat': using pretrained model or 'vgg': not using pretrained model || 'bbc': set output fit with dataset.`

Ex: `python dsf.py 0 244 4 smt_feat bbc`

-   TVSum dataset: `no need video_id starting and ending.`

Ex: `python dsf.py 0 244 2 vgg tvsum`

-   SumMe dataset: `no need video_id starting and ending.`

Ex: `python dsf.py 0 244 5 smt_feat summe`

# K-medoids

### Input
- Path of folder emotion or event ('.csv'):

`/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/shot_event`

- Path of save output:

`/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/time_shots_bbc/dsf_seg_rgb`

### Run code:
Accessing the working directory:
[deep_semantic_feature](https://github.com/tiendv/videosummarizationframework/tree/master/source/src/baseline/deep_semantic_feature)

Ex: `python bbc_kmedoids.py 0 243 1000` : `0: video_id starting || 243: video_id ending || 1000: Value K of K-medoids.`

### Output
```
<time_start>      <time_end>
<HH:MM:SS:FFFF>   <HH:MM:SS:FFFF>
00:00:30.4668     00:00:33.6703
00:00:52.8580     00:00:55.1271
00:00:58.3974     00:01:03.1359
00:01:07.9078     00:01:11.1447
```
