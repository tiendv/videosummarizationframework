# videosummarizationframework
This source is a framework using to summarize video and show the result visually on the website

![](https://github.com/tiendv/videosummarizationframework/blob/master/demo.png?raw=true)

## Requirement
* python 3.6

## Installing the evironment
Download the environment at  https://drive.google.com/open?id=1xSGkUZpzZ8TjCthL-kgvtj77WIY_FOhc
Environment list:
* videosum -- main environment to run the baseline
* freesound -- environment to run event detection from audios
* transnet -- environment to run transnet method to segment video
* event -- environment to run event detection from shots
### Intall a environment
* Dowdload a suitable environment having name_env.tar.gz format from above link.
* Unpack environment into directory
e.g
```
$ mkdir -p videosum
$ tar -xzf videosum.tar.gz -C videosum
```
* Activate the environment
```
$ source videosum/bin/activate
```

## How to run a baseline for video summary
Reading the instructions in the *source* directory

## How to run a visual tool for video summary
Reading the instructions in the *source/src/visualization* directory
