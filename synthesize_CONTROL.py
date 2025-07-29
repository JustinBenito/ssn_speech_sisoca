#!/usr/bin/python3



with open('pronuncing_dictionary') as f:
     lines = f.readlines()
     
d ={}

for line in lines:
    tam, eng, lex = line.split('\t')
    d[eng] = tam
   

import sys
sys.path.append('/home/ssn/espnet/')
#sys.path.append('/home/sltlab/espnet/tools/venv/lib64/python3.10/site-packages')

import time
import soundfile
from espnet2.bin.tts_inference import Text2Speech

import os

if len(sys.argv) != 2:
    print("Argument - text to be synthesized")

text = sys.argv[1]

words = text.split()
new_text=''

for word in words:
    new_text+=d[word]+' ' 

#start = time.time()
text2speech = Text2Speech.from_pretrained(model_file="exp/tts_train_fastspeech2_raw_phn_espeak_ng_tamil/1000epoch.pth", vocoder_tag="parallel_wavegan/vctk_style_melgan.v1")
speech = text2speech(new_text)["wav"]
speech_keys = text2speech(new_text)
print(speech)
end = time.time()
soundfile.write("test.wav", speech.numpy(), text2speech.fs, "PCM_16")
#os.system("play test.wav")
#print(end-start)
