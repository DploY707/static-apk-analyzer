FROM ubuntu:18.04
MAINTAINER DploY707 <starj1024@gmail.com>

# Install basic packages
RUN \
    apt-get update -y &&\
    apt-get install git zip curl unzip vim python3 python3-pip -y &&\
    apt-get update -y

# Install androguard
WORKDIR /root
RUN \
    mkdir workDir &&\
    cd workDir &&\
    git clone https://github.com/androguard/androguard.git &&\
    cd androguard &&\
    pip3 install setuptools &&\
    python3 ./setup.py install

# Set projects directories
WORKDIR /root
RUN \
    mkdir results &&\
    cd results &&\
    mkdir methodLists

# Set project core
COPY core /root/workDir/core/

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /root/workDir/core
# CMD ["python3","main.py"]
