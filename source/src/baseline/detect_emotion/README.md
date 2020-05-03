# Detect emotion
More information original paper and github: https://talhassner.github.io/home/publication/2015_ICMI 
### Create docker images base on Dockerfile
Accessing the working directory: 
[detect_emotion](https://github.com/tiendv/videosummarizationframework/blob/master/source/src/baseline/detect_emotion)

Build images: `docker build -t Name_image:Tag_image -f Dockerfile .`

Ex: `docker build -t emotion:v1 -f Dockerfile .`

Create container:

Ex: `docker run --name emotion --runtime=nvidia -v /mmlabstorage:/mmlabstorage -it emotion:v1 bash`
### Input:
- Path of folder keyframes:

`/mmlabstorage/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Keyframes_5fps`

- Path of folder face coordinates (' .csv'):

`/mmlabstorage/workingspace/InstaceSearch/hungvq/data/TRECVID_processed_data/TRECVID_BBC_EastEnders_Faces`

- Path save output emotion:

`/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/BBC_processed_data/events_emotion`
### Run code:
Accessing the working directory :
[detect_emotion](https://github.com/tiendv/videosummarizationframework/blob/master/source/src/baseline/detect_emotion)

Ex: `CUDA_VISIBLE_DEVICES=1 python3 detect_emotion.py 0 243` : `0: video_id starting || 243: video_id ending`

### Output
```
Sad,1
Angry,6
Disgust,0
Fear,0
Happy,0
Neutral,2
Surprise,0
```
