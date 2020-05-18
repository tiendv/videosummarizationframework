FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install  -y -q caffe-cuda
RUN apt install python3-pip -y
RUN pip3 install opencv-python
RUN apt install -y libsm6
RUN pip3 install easydict

