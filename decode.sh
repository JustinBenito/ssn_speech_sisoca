#!/bin/bash


input_wav_path="/home/sltlab/kaldi/egs/SISOCADEMO/test_new/MPK293.wav"


rm -rf ./mfcc
rm -rf ./wav_test
rm -rf ./output_MONO.txt

mkdir -p test_one
mkdir -p wav_test



last_part=$(echo "$input_wav_path" | rev | cut -d'/' -f1 | rev)
base_name=$(basename "$last_part" .wav)
spk=$(echo "$input_wav_path" | cut -d'/' -f2)

sox "$input_wav_path" "wav_test/$base_name.wav"          # This is done becuase the .wav file was actually in sphere (.sph) format. 
echo "$base_name wav_test/$base_name.wav" > test_one/wav.scp
echo "$base_name" > test_one/utt
echo "$spk" > test_one/spk
paste test_one/utt test_one/spk > test_one/utt2spk
paste test_one/spk test_one/utt > test_one/spk2utt


#feature extraction for test cases

steps/make_mfcc.sh --cmd "run.pl" --nj 1 test_one exp/make_mfcc/test mfcc
echo ""
echo ""

steps/compute_cmvn_stats.sh test_one exp/make_mfcc/test mfcc
echo ""
echo ""

#decode using monophone GMM-HMM

#steps/decode.sh --nj "1" --cmd "run.pl" --model exp/DNN_tri_8_2000_aligned_layer3_nodes256_mild/final.mdl exp/tri_8_2000_mild/graph test_one exp/DNN_tri_8_2000_aligned_layer3_nodes256_mild/decode

steps/nnet2/decode.sh --cmd "run.pl" --nj "1" \
 exp/tri_8_2000_mild/graph test_one \
  exp/DNN_tri_8_2000_aligned_layer3_nodes256_mild/decode | tee exp/DNN_tri_8_2000_aligned_layer3_nodes256_mild/decode/decode.log

#Store the decoded result

grep -h -Ev '^(#|nnet|LOG|apply|gmm|add|latgen-faster-mapped|copy|WARNING)' exp/DNN_tri_8_2000_aligned_layer3_nodes256_mild/decode/log/decode.1.log > output.txt


echo ""
echo ""
echo ""
cat output.txt


