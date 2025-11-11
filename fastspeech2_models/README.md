## Fastspeech2 TTS Models
This folder consists of TTS models for dysarthric speakers in `exp/` directory.

### Setup instructions
- Download the files from [GDrive link](https://drive.google.com/drive/folders/15jOT5cz6AqzzK-TAm0mzDgyqfo0XbqUX?usp=sharing)
- Unzip the contents and `exp.zip`
```
Expected directory setup...

fastspeech2_models/
                espnet/
                espnet2/
                dump/
                exp/
                requirements.txt
                synthesize.py
                speaker_list.txt
            
```
- Install the requirements
```
pip install -r requirements.txt
```
- Run the model
```
python3 synthesize.py "arg1" arg2
```
- **arg1** - Tamil text 
- **arg2** - Speaker ID

Example:
```
python3 synthesize.py "சென்னையில் தங்கம் விலை என்ன" fga
```
> Kindly refer `speaker_list.txt` for the available speakers.

