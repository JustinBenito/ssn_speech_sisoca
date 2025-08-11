# SISOCA Demo

This project integrates a **DNN-HMM based ASR** (Automatic Speech Recognition) system and a **FastSpeech2-based TTS** (Text-to-Speech) system. It is designed for **dysarthria speech conversion**, specifically targeting **mild and moderate dysarthric speakers**, as well as **individual speaker adaptation** for dysarthria. The ASR transcribes the input speech, and the TTS generates clear, natural-sounding speech from the recognized text.

---


## 📦 Prerequisites

- [Kaldi](https://github.com/kaldi-asr/kaldi)
- [ESPnet](https://github.com/espnet/espnet)

---

## 📁 Models for Demo

The **DNN-HMM** model files are stored in the `exp/` directory, with separate subfolders for each model:

- **mild**
- **moderate**
- **punitha**

**Example `exp/` directory structure:**
```
exp/
├── mild/
│   ├── model files...
├── moderate/
│   ├── model files...
└── punitha/
    ├── model files...
```

---

## 🚀 Steps to Execute

### 1️⃣ Activate Environment
```bash
source activate_python.sh   # Activates ESPnet virtual environment
source path_try.sh          # Sets up Kaldi paths
```

### 2️⃣ Run Model Decoding
- **Moderate model decoding**  
  ```bash
  ./main_run.sh
  ```

- **Mild model decoding**  
  ```bash
  ./main_run_mild.sh
  ```

- **Punitha model decoding**  
  ```bash
  ./main_run_punitha.sh
  ```

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
  /workspace/exp/tts_train_fastspeech2_raw_phn_espeak_ng_tamil/
  ```
- Audio output will be saved as `test.wav` unless specified otherwise.
