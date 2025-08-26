# #step 1 is installing espnet
# FROM espnet/espnet:cpu-latest

# # Environment
# ENV LC_ALL=C.UTF-8
# ENV LANG=C.UTF-8

# # Copy repo
# WORKDIR /workspace
# COPY . /workspace


# # Update and install dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     automake \
#     autoconf \
#     libtool \
#     subversion \
#     wget \
#     python3 \
#     python3-pip \
#     libatlas3-base \
#     alsa-utils \
#     sox \
#     && rm -rf /var/lib/apt/lists/*

# # Build tools: sph2pipe and openfst
# WORKDIR /opt/kaldi/tools
# RUN make sph2pipe openfst -j$(nproc)

# # Build src
# WORKDIR /opt/kaldi/src
# RUN ./configure --mathlib=ATLAS
# RUN make -j$(nproc) clean depend
# RUN make -j$(nproc)

# WORKDIR /opt/kaldi/egs
# RUN git clone https://github.com/JustinBenito/ssn_speech_sisoca.git

# WORKDIR /opt/kaldi/egs/ssn_speech_sisoca
# RUN python3 -m venv .venv 
# RUN source .venv/bin/activate
# RUN pip install -r requirements.txt
# RUN fastapi run

# new docker file it is :)

# FROM speechlabssn/sisoca:v1.0

# # Set working directory
# WORKDIR /opt/kaldi/egs/ssn_speech_sisoca

# # Activate the virtual environment by adjusting PATH
# ENV PATH="/opt/kaldi/egs/ssn_speech_sisoca/.venv/bin:$PATH"

# # Expose FastAPI port inside container
# EXPOSE 8000

# # Run FastAPI app
# # Assuming your app is started by "fastapi run" or maybe "uvicorn main:app --host 0.0.0.0 --port 8000"
# CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]

# ++++++++++++++++++
FROM speechlabssn/sisoca:v1.0

WORKDIR /opt/kaldi/egs/ssn_speech_sisoca
RUN git stash
RUN git pull

# Use existing venv from base image
ENV PATH="/opt/kaldi/egs/ssn_speech_sisoca/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y sox ffmpeg

ENV KALDI_ROOT=/opt/kaldi
ENV PATH=$KALDI_ROOT/src/latbin:$KALDI_ROOT/src/bin:$KALDI_ROOT/src/fstbin:$KALDI_ROOT/src/gmmbin:$KALDI_ROOT/src/featbin:$KALDI_ROOT/src/lmbin:$KALDI_ROOT/src/nnet2bin:$KALDI_ROOT/src/nnet3bin:$KALDI_ROOT/src/online2bin:$KALDI_ROOT/src/ivectorbin:$KALDI_ROOT/src/rnnlmbin:$KALDI_ROOT/tools/openfst/bin:$PATH


# Install Python deps
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install pydub

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
