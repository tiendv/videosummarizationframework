FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update 
RUN apt update -y
RUN apt-get install -y wget

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN pip install numpy
RUN pip install hdf5storage
RUN pip install tables
RUN pip install scipy
RUN pip install pandas
RUN pip install scikit-learn
RUN pip install easydict
