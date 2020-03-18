# How to run a baseline for summarizing a video

### Summarize a input video
To summarize a input video using the following command
```python
python main_baseline.py <path_input_video> --jshot <path_json_shot> --jseg <path_json_segment>
```
* <path_input_video> (required) : the path of a video you want to summarize
* <path_json_shot> (optional) : the path that the json for visualizing the shots will be saved at (default "./")
* <path_json_segment> (optional) : the path that the json for visualizing the shots will be saved at (default "./")

### Change the method segmenting to shots
Replace the **spli_shot** function in *main_baseline* function with your segment function

### Change the method calculating the score for shots
Replace the **calc_score** function in *main_baseline* function with your score function

### Create json for visualizing shots from file
#### File format
The information of each shot is written in a file with the following format
```
<start time of shot> <end time of shot> <score of shot>
HH:MM:SS.FFFF HH:MM:SS.FFFF float (1st shot)
HH:MM:SS.FFFF HH:MM:SS.FFFF float (2nd shot)
...
HH:MM:SS.FFFF HH:MM:SS.FFFF float (nth shot)
```

example:
```
00:00:00.0000 00:00:02.0402 1.15
00:00:02.0402 00:00:04.0404 1.7
00:00:04.0404 00:00:06.0406 1.45
00:00:06.0406 00:00:08.0407 1.55
00:00:08.0407 00:00:10.0409 1.35
00:00:10.0409 00:00:12.0411 1.45
00:00:12.0411 00:00:14.0413 1.5
00:00:14.0413 00:00:18.0417 1.55
00:00:18.0417 00:00:20.0418 1.65
```
#### Using the **create_json4shots** function to create json from the above file
```python
from src.baseline.segmentation.create_json_from_time_shots import create_json4shots
```
