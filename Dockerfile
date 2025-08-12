FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# 1. System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential g++ gfortran make automake autoconf libtool \
        bzip2 unzip wget sox git python3 python3-pip python3-venv \
        zlib1g-dev ca-certificates patch libatlas-base-dev libboost-all-dev \
        libsndfile1-dev ffmpeg curl subversion cmake libopenblas-dev liblapack-dev \
        python-is-python3 && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Kaldi (CPU) - use system OpenBLAS instead of install_openblas.sh
WORKDIR /opt
RUN git clone --depth 1 https://github.com/kaldi-asr/kaldi.git
WORKDIR /opt/kaldi/tools
RUN touch openblas.done  # trick Kaldi into thinking OpenBLAS is installed
RUN make -j $(nproc)
WORKDIR /opt/kaldi/src
RUN ./configure --shared --mathlib=OPENBLAS && \
    make depend -j $(nproc) && \
    make -j $(nproc)


# 3. Install ESPnet (CPU, no CUDA)
WORKDIR /opt
RUN git clone --depth 1 https://github.com/espnet/espnet.git
WORKDIR /opt/espnet/tools
RUN python3 -m venv venv
ENV PATH="/opt/espnet/tools/venv/bin:$PATH"
RUN . venv/bin/activate && \
    pip install --upgrade pip wheel && \
    make KALDI=/opt/kaldi CPU_ONLY=1 && \
    pip cache purge

# 4. Copy your repo
WORKDIR /workspace
COPY . /workspace

# 5. Install your repo's dependencies in ESPnet venv
RUN . /opt/espnet/tools/venv/bin/activate && \
    pip install --no-cache-dir -r /workspace/requirements.txt

# 6. Point your scripts to Kaldi
RUN sed -i 's|export KALDI_ROOT=.*|export KALDI_ROOT=/opt/kaldi|' /workspace/path_try.sh

# 7. Entrypoint
COPY docker_entrypoint.sh /docker_entrypoint.sh
RUN chmod +x /docker_entrypoint.sh
ENTRYPOINT ["/docker_entrypoint.sh"]
