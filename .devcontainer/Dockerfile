# FROM mcr.microsoft.com/devcontainers/anaconda:0-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
# COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/

# RUN python3 -m pip install -U pyOpenSSL cryptography \
#  && if [ -f "/tmp/conda-tmpython3 -m pip install -U pyOpenSSL cryptographyp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
#     && rm -rf /tmp/conda-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

FROM nvidia/cuda:10.2-devel-ubuntu18.04

ENV COLMAP_VERSION=3.7
ENV CMAKE_VERSION=3.21.0
ENV PYTHON_VERSION=3.8.0
ENV OPENCV_VERSION=4.5.5.62
ENV CERES_SOLVER_VERSION=2.0.0

RUN echo "Installing apt packages..." \
	&& export DEBIAN_FRONTEND=noninteractive \
	&& apt -y update --no-install-recommends \
	&& apt -y install --no-install-recommends \
	git \
	wget \
	ffmpeg \
	tk-dev \
	libxi-dev \
	libc6-dev \
	libbz2-dev \
	libffi-dev \
	libomp-dev \
	libssl-dev \
	zlib1g-dev \
	libcgal-dev \
	libgdbm-dev \
	libglew-dev \
	python3-dev \
	python3-pip \
	qtbase5-dev \
	checkinstall \
	libglfw3-dev \
	libeigen3-dev \
	libgflags-dev \
	libxrandr-dev \
	libopenexr-dev \
	libsqlite3-dev \
	libxcursor-dev \
	build-essential \
	libcgal-qt5-dev \
	libxinerama-dev \
	libboost-all-dev \
	libfreeimage-dev \
	libncursesw5-dev \
	libatlas-base-dev \
	libqt5opengl5-dev \
	libgoogle-glog-dev \
	libsuitesparse-dev \
	python3-setuptools \
	libreadline-gplv2-dev \
	&& apt autoremove -y \
	&& apt clean -y \
	&& export DEBIAN_FRONTEND=dialog

RUN apt install python2.7
ENV NODE_VERSION=18.13.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

RUN echo "Installing Python ver. ${PYTHON_VERSION}..." \
	&& cd /opt \
	&& wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
	&& tar xzf Python-${PYTHON_VERSION}.tgz \
	&& cd ./Python-${PYTHON_VERSION} \
	&& ./configure --enable-optimizations \
	&& make \
	&& checkinstall

COPY ./requirements.txt ./

RUN echo "Installing pip packages..." \
	&& python3 -m pip install -U pip \
	&& pip3 --no-cache-dir install -r ./requirements.txt \
	&& pip3 --no-cache-dir install cmake==${CMAKE_VERSION} opencv-python==${OPENCV_VERSION} \
	&& rm ./requirements.txt

RUN echo "Installing Ceres Solver ver. ${CERES_SOLVER_VERSION}..." \
	&& cd /opt \
	&& git clone https://github.com/ceres-solver/ceres-solver \
	&& cd ./ceres-solver \
	&& git checkout ${CERES_SOLVER_VERSION} \
	&& mkdir ./build \
	&& cd ./build \
	&& cmake ../ -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF \
	&& make -j3 \
	&& make install

RUN echo "Installing COLMAP ver. ${COLMAP_VERSION}..." \
	&& cd /opt \
	&& git clone https://github.com/colmap/colmap \
	&& cd ./colmap \
	&& git checkout ${COLMAP_VERSION} \
	&& mkdir ./build \
	&& cd ./build \
	&& cmake ../ \
	&& make -j3 \
	&& make install \
	&& colmap -h
	

RUN npm install -g prisma
COPY ./prisma/schema.prisma ./prisma/
RUN prisma db push