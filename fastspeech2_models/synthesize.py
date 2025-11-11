#!/usr/bin/python3

import sys
import soundfile
from espnet2.bin.tts_inference import Text2Speech

import os
import kaldiio

if len(sys.argv) != 3:
  print("Argument1 - text to be synthesized")
  print("Argument2 - name of the speaker")
  exit()

text = sys.argv[1]

new_text=text

xvec_file = 'dump/xvector/train/spk_xvector_'+sys.argv[2].upper()+'.ark'
xvectors = {k: v for k, v in kaldiio.load_ark(xvec_file)}
spembs = xvectors[sys.argv[2].upper()]

model_file = 'exp/tts_finetune_fast2_'+sys.argv[2].lower()+'/train.loss.ave_5best.pth'
print(model_file, xvec_file)
text2speech = Text2Speech.from_pretrained(model_file=model_file, vocoder_tag="parallel_wavegan/vctk_style_melgan.v1")
speech = text2speech(new_text, spembs=spembs)["wav"]
soundfile.write("test.wav", speech.numpy(), text2speech.fs, "PCM_16")
os.system("play test.wav")
