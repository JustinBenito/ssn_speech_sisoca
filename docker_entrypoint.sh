#!/bin/bash
# Activate ESPnet venv
source /opt/espnet/tools/venv/bin/activate
# Set Kaldi root
export KALDI_ROOT=/opt/kaldi
# Set PATH as in path_try.sh
export PATH=$PWD/utils/:$KALDI_ROOT/src/bin:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/../tools/srilm-1.6.0/bin/i686-m64/:$KALDI_ROOT/src/fstbin/:$KALDI_ROOT/src/gmmbin/:$KALDI_ROOT/src/featbin/:$KALDI_ROOT/src/lm/:$KALDI_ROOT/src/sgmmbin/:$KALDI_ROOT/src/sgmm2bin/:$KALDI_ROOT/src/fgmmbin/:$KALDI_ROOT/src/latbin/:$KALDI_ROOT/src/nnetbin:$KALDI_ROOT/src/nnet2bin/:$KALDI_ROOT/src/kwsbin:$KALDI_ROOT/src/lmbin:$PWD:$PATH
export LC_ALL=C
exec "$@" 