# SISOCA Speech-Input Speech-Output Communication Aid

This project integrates a **DNN-HMM based ASR** (Automatic Speech Recognition) system and a **FastSpeech2-based TTS** (Text-to-Speech) system. It is designed for **dysarthria speech conversion**, specifically targeting **mild and moderate dysarthric speakers**, as well as **individual speaker adaptation** for dysarthria. The ASR transcribes the input speech, and the TTS generates clear, natural-sounding speech from the recognized text.

---


## 📦 Prerequisites

- [Kaldi](https://github.com/kaldi-asr/kaldi)
- [ESPnet](https://github.com/espnet/espnet)

---

## 📁 ASR Models (only tamil)

The **DNN-HMM** model files are stored in the `exp/` directory, with separate subfolders for each model:

- **Mild**
- **Moderate**
- **Punitha**


---

## 🚀 Setup & Run Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/JustinBenito/ssn_speech_sisoca.git
cd ssn_speech_sisoca/
```
### 2️⃣ Setup ESPnet & Kaldi
Ensure you have Kaldi and ESPnet installed.

Activate the ESPnet virtual environment:

```bash
source activate_python.sh    # Activates ESPnet virtual environment (optional)
source path_try.sh           # Sets Kaldi + ESPnet paths
```
👉 Make sure both ESPnet and Kaldi paths are correctly set in `activate_python.sh` and `path_try.sh` respectively.

### 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```
### 4️⃣ Download & Setup TTS Model
Run the model download script:

```bash
python download.py
```
Copy the models into the exp/ directory:

```bash
mv fastspeech2_aarthi/* exp/tts_train_fastspeech2_raw_phn_espeak_ng_tamil/
```
### 5️⃣ Run Model Decoding

- **Moderate model decoding**
```bash
./main_run.sh <audio.wav>
```
- **Mild model decoding**
```bash
./main_run_mild.sh <audio.wav>
```
- **Punitha model decoding**
```bash
./main_run_punitha.sh <audio.wav>

```
> Note: The above script consists of ASR and TTS pipline. Hence the output is saved as `test.wav`

### 6️⃣ Try our Web App
👉 [sisoca.ssn.lat](sisoca.ssn.lat)

---


## 🔄 Pipeline

```text
Speech Input
      ↓
ASR Model (Kaldi)
      ↓
Recognised Text
      ↓
TTS Model (ESPnet)
      ↓
Speech Output
```

---

## 📌 Notes

- Ensure all required Kaldi and ESPnet paths are correctly set in the `.sh` scripts.
- The TTS models are located in:
  ```
  /exp/tts_train_fastspeech2_raw_phn_espeak_ng_tamil/
  ```
- Audio output will be saved as `test.wav` unless specified otherwise.
