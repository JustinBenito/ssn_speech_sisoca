#!/usr/bin/python3
import sys
sys.path.append('/home/sltlab/espnet/')


import sys
import time
import soundfile
from espnet2.bin.tts_inference import Text2Speech

def synthesize_tamil(text, dictionary_path='pronuncing_dictionary',
                     model_path="exp/tts_train_fastspeech2_raw_phn_espeak_ng_tamil/1000epoch.pth", 
                     vocoder_tag="parallel_wavegan/vctk_style_melgan.v1", output_path="test.wav"):
    """
    Synthesizes speech from text using a pronouncing dictionary and a pre-trained TTS model.
    
    Args:
        text (str): The English text to be synthesized.
        dictionary_path (str): Path to the pronouncing dictionary.
        model_path (str): Path to the pre-trained TTS model.
        vocoder_tag (str): Vocoder tag to use for synthesis.
        output_path (str): Output path for the synthesized WAV file.
    
    Returns:
        str: Path to the output WAV file.
    """
    # Load the pronouncing dictionary
    with open(dictionary_path) as f:
        lines = f.readlines()

    d = {}
    for line in lines:
        tam, eng, lex = line.strip().split('\t')
        d[eng] = tam

    # Prepare the Tamil text using the dictionary
    words = text.split()
    new_text = ' '.join(d.get(word, word) for word in words)  # Use word itself if not found in dictionary

    # Start TTS inference
    text2speech = Text2Speech.from_pretrained(
        model_file=model_path, 
        vocoder_tag=vocoder_tag
    )
    start = time.time()
    speech = text2speech(new_text)["wav"]
    end = time.time()

    # Write the output to a WAV file
    soundfile.write(output_path, speech.numpy(), text2speech.fs, "PCM_16")
    
    print(f"Synthesis completed in {end - start} seconds.")
    return output_path
