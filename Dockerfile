#step 1 is installing espnet
FROM espnet/espnet:cpu-latest

# Environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Copy repo
WORKDIR /workspace
COPY . /workspace


# Update and install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    automake \
    autoconf \
    libtool \
    subversion \
    wget \
    python3 \
    python3-pip \
    libatlas3-base \
    alsa-utils \
    sox \
    && rm -rf /var/lib/apt/lists/*

# Build tools: sph2pipe and openfst
WORKDIR /opt/kaldi/tools
RUN make sph2pipe openfst -j$(nproc)

# Build src
WORKDIR /opt/kaldi/src
RUN ./configure --mathlib=ATLAS
RUN make -j$(nproc) clean depend
RUN make -j$(nproc)

WORKDIR /opt/kaldi/egs
RUN git clone https://github.com/JustinBenito/ssn_speech_sisoca.git

WORKDIR /opt/kaldi/egs/ssn_speech_sisoca
RUN python3 -m venv .venv 
RUN source .venv/bin/activate
RUN pip install -r requirements.txt
RUN fastapi run


