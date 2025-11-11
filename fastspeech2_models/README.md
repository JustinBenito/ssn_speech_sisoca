## Fastspeech2 TTS Models
This folder consists of TTS models for dysarthric speakers in `exp/` directory.

### Setup instructions
```
pip install -r requirements.txt
```
```
python3 synthesize.py "arg1" arg2
```
arg1 - Tamil text 
arg2 - Speaker ID

Kindly refer `speaker_list.txt` for the available speakers.
Example:

```
python3 synthesize.py "சென்னையில் தங்கம் விலை என்ன" fga
```

