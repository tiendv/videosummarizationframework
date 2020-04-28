#!/bin/bash
. ../../config/config_extractshot.cfg

video_list="../../../test_data/input/video_list/${1}"

SECONDS=0
while IFS= read -r video_name
do
  file= "../../../test_data/input/shot_reference.txt"
    found=false
    echo "Searching $video_name in master_shot_reference.txt ..."

    while IFS= read -r line
    do
	IFS="    "
	set -- $line

	if [ $video_name != $1 ]
	then
	    continue
	fi

	if [ "$found" = false ]
	then
	    echo "File $video_name has been found."
	    found=true
	fi

	name= $example_video_path/$1
	start_time="$3"
	end_time="$4"
	output= $example_shots_path/$2.mp4

	if [ ! -f $output ]
	then
        echo "Do ffmpeg"
		    #$ffmpeg -ss ${start_time} -i $name -to ${end_time} -an -copyts  $output
    fi

	# echo "!Warning: Path $output is already existed"
	# echo $name
    done <"$file"

done <"$video_list"
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
