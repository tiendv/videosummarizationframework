FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ENV PATH="/root/miniconda2/bin:${PATH}"
ARG PATH="/root/miniconda2/bin:${PATH}"

RUN apt-get update && apt-get install -y
RUN apt-get install -y python2.7
RUN apt install -y python-pip
RUN apt-get install -y wget

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda2-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda2-latest-Linux-x86_64.sh

RUN pip install numpy
RUN conda install -c conda-forge opencv -y
RUN conda install -c anaconda chainer
RUN pip install scipy
COPY . /home/code
RUN cd /home/code/gm_submodular && python setup.py install --user
RUN pip install ipython
RUN pip install simplejson
RUN pip install pandas
RUN apt install -y libsm6



