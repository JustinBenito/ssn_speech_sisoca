#!/bin/bash

source cmd.sh
source path_try.sh

input_wav_path=$1

# Convert the audio to the same name with different settings (16 kHz, mono)
temp_output="${input_wav_path%.wav}_temp.wav"
ffmpeg -y -i "$input_wav_path" -ar 16000 -ac 1 "$temp_output"
# If conversion is successful, move the temporary file to overwrite the original
if [ $? -eq 0 ]; then
    mv "$temp_output" "$input_wav_path"
else
    echo "Conversion failed"
fi

aplay "$input_wav_path"

echo "$input_wav_path"

rm -rf ./mfcc
rm -rf ./wav_test
rm -rf ./output_MONO.txt
rm -rf ./test_one

mkdir -p test_one
mkdir -p wav_test

last_part=$(echo "$input_wav_path" | rev | cut -d'/' -f1 | rev)
base_name=$(basename "$last_part" .wav)
spk=$(echo "$input_wav_path" | cut -d '/' -f 7)

echo $last_part
echo $base_name
echo $spk

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

steps/nnet2/decode.sh --cmd "run.pl" --nj "1" \
 exp/tri_8_2000_moderate/graph test_one \
  exp/DNN_tri_8_2000_aligned_layer3_nodes256_moderate/decode | tee exp/DNN_tri_8_2000_aligned_layer3_nodes256_moderate/decode/decode.log

#Store the decoded result

grep -h -Ev '^(#|nnet|LOG|apply|gmm|add|latgen-faster-mapped|copy|WARNING)' exp/DNN_tri_8_2000_aligned_layer3_nodes256_moderate/decode/log/decode.1.log > output.txt
#cat output.txt

log_filter=$(grep -h -Ev '^(#|nnet|LOG|apply|gmm|add|latgen-faster-mapped|copy|WARNING)' exp/DNN_tri_8_2000_aligned_layer3_nodes256_moderate/decode/log/decode.1.log)

var2=$(echo "$log_filter" | cut -d ' ' -f 2-)
echo "$var2"  

#python synthesize.py "$var2" $spk

python3 synthesize_CONTROL.py "$var2"

#aplay test.wav 
