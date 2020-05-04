# How to run detect event from a video shot

### Installing environment
* Download event.tar.gz file from  https://drive.google.com/open?id=1xSGkUZpzZ8TjCthL-kgvtj77WIY_FOhc
* Unpack environment into directory "event_env"
```
$ mkdir -p event_env
$ tar -xzf event.tar.gz -C event_env
```
* Activate the environment.
```
$ source event_env/bin/activate
```
### Run event detection
In https://github.com/tiendv/videosummarizationframework/blob/master/source/config/config.py
* Change the path of video input at cfg.EXAMPLE_BBC_SHOT_PATH
* Change the path of detection result at cfg.EXAMPLE_OUTPUT_PATH
Run the following conmand:
 ```
 python detect_event.py
```
The output is a csv file having format:
```
event_name1,score1
event_name2,score2
...
event_name339,score339
```
 
