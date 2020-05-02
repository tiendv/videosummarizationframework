# Create docker images base on Dockerfile: Accessing the working directory :
https://github.com/tiendv/videosummarizationframework/tree/master/source/src/baseline/deep_semantic_feature
Build images: docker build -t Name_image:Tag_image -f Dockerfile .
Ex: docker build -t deep_semantic_feature:v1 -f Dockerfile .
Ex: docker run --name videosum_test2 --runtime=nvidia -v /mmlabstorage:/mmlabstorage -it deep_semantic_feature:v1 bash

# Input:
- Path directory .npy extract feature from video with vgg or resnet:
/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/frames_feature/VGG16

- Path directory .csv feature:
/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/input_data/SumMe.csv

- Path save output time:
/mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/SumMe_processed_data/time_segment/vsum_dsf

# Accessing the working directory :
https://github.com/tiendv/videosummarizationframework/tree/master/source/src/baseline/deep_semantic_feature
# Run: 
-   BBC dataset: 0: video_id starting || 244: video_id ending || 4: length uniform segment || 'smt_feat': using pretrained model or 'vgg': not using pretrained model || 'bbc': set output fit with dataset.
Ex: python dsf.py 0 244 4 smt_feat bbc

-   TVSum dataset: no need video_id starting and ending.
Ex: python dsf.py 0 244 2 vgg tvsum

-   SumMe dataset: no need video_id starting and ending.
Ví dụ: python dsf.py 0 244 5 smt_feat summe

