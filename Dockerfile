FROM ubuntu:18.04
MAINTAINER DploY707 <starj1024@gmail.com>
MAINTAINER kordood <gigacms@gmail.com>

# Update apt source list mirror site
RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

# Install basic packages
RUN \
    apt-get update -y &&\
    apt-get install git zip curl unzip vim python3.8 python3-pip -y &&\
    apt-get update -y &&\
#	update-alternatives --config python3
	update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Install androguard
WORKDIR /root
RUN \
    mkdir workDir &&\
    cd workDir &&\
    git clone https://github.com/androguard/androguard.git &&\
    cd androguard &&\
    pip3 install setuptools &&\
    python3 ./setup.py install

# Install RetDec
RUN useradd -m retdec
WORKDIR /home/retdec
ENV HOME /home/retdec

RUN apt-get install -y		\
	build-essential			\
	cmake					\
	git						\
	python3					\
	doxygen					\
	graphviz				\
	upx						\
	openssl				    \
	libssl-dev				\
	zlib1g-dev				\
	autoconf				\
	automake				\
	pkg-config				\
	m4						\
	libtool

USER retdec
RUN git clone https://github.com/avast/retdec && \
	cd retdec &&		\
	mkdir build &&		\
	cd build &&			\
	cmake .. -DCMAKE_INSTALL_PREFIX=/home/retdec/retdec-install -DCMAKE_LIBRARY_PATH=/usr/lib/gcc/x86_64-linux-gnu/7/ && \
	make -j$(nproc) &&	\
	make install

ENV PATH /home/retdec/retdec-install/bin:$PATH
RUN mkdir /home/retdec/input /home/retdec/output

# Set projects directories
USER root
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
