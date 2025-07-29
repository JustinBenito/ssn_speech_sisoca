# Use Ubuntu 22.04 as base
FROM ubuntu:22.04

# 1. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential git wget sox python3 python3-pip python3-venv \
    libatlas-base-dev libboost-all-dev zlib1g-dev automake autoconf \
    libtool subversion gfortran cmake libopenblas-dev liblapack-dev \
    libsndfile1-dev sox ffmpeg curl ca-certificates unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Install Kaldi
WORKDIR /opt
RUN git clone --depth 1 https://github.com/kaldi-asr/kaldi.git
WORKDIR /opt/kaldi/tools
RUN mkdir -p python
RUN sed -i 's/OPENFST_VERSION = .*/OPENFST_VERSION = 1.8.2/' Makefile
RUN make -j 4
WORKDIR /opt/kaldi/src
RUN ./configure --shared && make depend -j 4 && make -j 4

# 3. Install ESPnet
WORKDIR /opt
RUN git clone --depth 1 https://github.com/espnet/espnet.git
WORKDIR /opt/espnet/tools
RUN python3 -m venv venv
ENV PATH="/opt/espnet/tools/venv/bin:$PATH"
RUN /bin/bash -c ". venv/bin/activate && pip install --upgrade pip && pip install wheel && pip install espnet"

# 4. Copy your repo
WORKDIR /workspace
COPY . /workspace

# 5. Install your repo's Python dependencies in ESPnet venv
RUN /bin/bash -c ". /opt/espnet/tools/venv/bin/activate && pip install -r /workspace/requirements.txt"

# 6. Update path_try.sh to point to /opt/kaldi
RUN sed -i 's|export KALDI_ROOT=.*|export KALDI_ROOT=/opt/kaldi|' /workspace/path_try.sh

# 7. Copy entrypoint script
COPY docker_entrypoint.sh /docker_entrypoint.sh
RUN chmod +x /docker_entrypoint.sh

# 8. Set entrypoint
WORKDIR /workspace
ENTRYPOINT ["/docker_entrypoint.sh"] 