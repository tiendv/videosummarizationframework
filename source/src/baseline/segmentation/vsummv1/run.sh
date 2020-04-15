#!/bin/bash
Datapath = /mmlabstorage/datasets/TVSum50/ydata-tvsum50-v1_1/video;
Framepath = /mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/tvsum50_frames;
outpath = /mmlabstorage/workingspace/VideoSum/videosummarizationframework/data/TVSum_processed_data/time_shots_tvsum50/VSUMM;

# sampling rates for future use
# "1" "2" "5" "10" "25" "30"
$echo Datapath
$echo Framepath
$echo outpath

for sampling_rate in 1 2 5 10 25 30; do
	echo $sampling_rate

	python Vsumm_test.py $Datapath $Framepath $outpath $sampling_rate
done