# Zero ASR 🎙️

> **Fully offline, custom-built Automatic Speech Recognition system.**
> No cloud. No APIs. No subscriptions. Your voice, your hardware, your model.

Built from scratch using a **Compact Conformer-CTC** acoustic model trained on LibriSpeech.
Supports **English** and **Romanized Tamil** transcription with a FastAPI backend and React frontend.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quick Start (Running Locally)](#quick-start-running-locally)
- [Training — Resume on Any Machine](#training--resume-on-any-machine)
  - [Option 2 — Quick Fine-Tune (Recommended First)](#option-2--quick-fine-tune-recommended-first)
  - [Option 1 — Full Long Run](#option-1--full-long-run)
- [CPU Incremental Training](#cpu-incremental-training)
- [Google Drive Storage](DRIVE_SETUP.md)
- [Setup on Colab / Kaggle / Company PC](#setup-on-colab--kaggle--company-pc)
- [API Endpoints](#api-endpoints)
- [Current Model Status](#current-model-status)
- [Roadmap](#roadmap)

---

## Overview

Zero ASR is a custom speech recognition system that runs **100% offline** on your own GPU.
It uses a Conformer-CTC model trained on LibriSpeech `train-clean-100` (~100 hours of speech).

| Feature | Details |
|---|---|
| **Languages** | English, Tamil (Romanized Latin) |
| **Architecture** | Conformer-CTC (non-autoregressive) |
| **Model size** | ~3.4M parameters (compact, edge-ready) |
| **Training data** | LibriSpeech train-clean-100 (28,539 utterances) |
| **Inference** | Real-time streaming via browser mic |
| **Backend** | FastAPI + PyTorch |
| **Frontend** | React + Vite |

---

## Architecture

```
Microphone / Audio File
        │
        ▼
┌──────────────────┐
│  AudioFrontend   │  16kHz mono → 80-channel Log-Mel Spectrogram + CMVN
└──────────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│  Conv2dSubsampler  (4× time reduce)  │
└──────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│  6 × Conformer Blocks                │
│  (Self-Attn + Conv + FFN, d=144)     │
└──────────────────────────────────────┘
        │
        ▼
┌──────────────────┐
│  CTC Head        │  Linear projection → 32-token vocab
└──────────────────┘
        │
        ▼
┌──────────────────┐
│  CTC Greedy      │  Decode characters → words
│  Decoder         │
└──────────────────┘
        │
        ▼
┌──────────────────┐
│  TextNormalizer  │  Remove fillers, fix casing
└──────────────────┘
        │
        ▼
     Transcript
```

---

## Project Structure

```
Zero_ASR/
├── backend/
│   ├── asr_engine/
│   │   ├── audio/
│   │   │   ├── frontend.py        # Mel-spectrogram extraction + CMVN
│   │   │   ├── io.py              # Universal audio loader (soundfile + PyAV)
│   │   │   ├── augment.py         # SpecAugment
│   │   │   └── vad.py             # Energy-based VAD
│   │   ├── model/
│   │   │   ├── ctc_model.py       # ConformerCTC main model
│   │   │   └── conformer.py       # Conformer blocks + subsampler
│   │   ├── tokenizer/
│   │   │   ├── char_tokenizer.py  # 32-token character tokenizer
│   │   │   └── romanizer.py       # Tamil → Romanized Latin
│   │   ├── decoding/
│   │   │   └── ctc_decoder.py     # Greedy + streaming CTC decoder
│   │   ├── postprocess/
│   │   │   └── normalizer.py      # Text normalization & disfluency removal
│   │   ├── evaluation/
│   │   │   └── metrics.py         # WER, CER, RTF calculation
│   │   ├── data/
│   │   │   └── dataset.py         # ASR dataset + collate fn
│   │   └── pipeline.py            # End-to-end ASRPipeline class
│   ├── checkpoints/
│   │   └── compact_conformer/
│   │       ├── best_model.pt      # Best checkpoint (epoch 47, loss 0.83)
│   │       ├── latest_model.pt    # Latest checkpoint (epoch 50, loss 0.83)
│   │       └── vocab.json         # Tokenizer vocabulary
│   ├── data/
│   │   └── manifests/             # JSON manifest files for training
│   ├── server.py                  # FastAPI REST server
│   ├── train.py                   # Main training script
│   ├── prepare_data.py            # LibriSpeech → manifest builder
│   └── live_transcribe.py         # CLI live mic transcription
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main React app
│   │   ├── index.css              # Global styles
│   │   └── utils/wavEncoder.js    # Browser mic → WAV encoder
│   ├── package.json
│   └── vite.config.js
├── start_backend.bat              # Windows: start FastAPI server
├── start_frontend.bat             # Windows: start React dev server
├── start_training.bat             # Windows: run training / fine-tune
├── TRAINING_PROMPT.md             # Agent prompt for Colab / Kaggle
├── CPU_TRAINING.md                # CPU five-epoch training handoff
├── requirements.txt               # Python dependencies
└── README.md
```

---

## Quick Start (Running Locally)

### Prerequisites
- Python 3.10+
- Node.js 18+
- NVIDIA GPU (recommended) or CPU

### 1. Clone

```bash
git clone https://github.com/Hariesh-Kai/Zero_ASR.git
cd Zero_ASR
```

### 2. Create Python environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install fastapi uvicorn soundfile av numpy
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

## CPU Incremental Training

For machines without CUDA, use the isolated CPU workflow documented in
[CPU_TRAINING.md](CPU_TRAINING.md). It runs exactly five additional epochs per
command and resumes from `backend/checkpoints/cpu_finetune/` on the next run.

It starts from the existing epoch-50 model but never overwrites
`backend/checkpoints/compact_conformer/`, which preserves the original GPU
training result. The complete handoff instructions, data prerequisites,
settings, checkpoint behavior, and deployment notes are in that document.

```bash
source venv/bin/activate
python backend/prepare_data.py
python backend/train_cpu_increment.py
```

When local disk space is limited, place the dataset, manifests, source
checkpoint, and `cpu_finetune` directory on a mounted Google Drive and pass
their paths with `--train_manifest`, `--val_manifest`, `--source_model_dir`,
and `--checkpoint_dir`. See [CPU_TRAINING.md](CPU_TRAINING.md) for the Google
Colab mount and repeatable command.

### 5. Start the backend

```bash
# Windows
start_backend.bat

# Linux / Mac
cd backend
python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
```

### 6. Start the frontend

```bash
# Windows
start_frontend.bat

# Linux / Mac
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser. The app connects to the backend at `http://localhost:8000`.

---

## Training — Resume on Any Machine

The pre-trained checkpoint (epoch 50, CTC loss 0.83) is included in the repo.
You can **resume training directly** without starting from scratch. Before a
corrective fine-tune, rebuild the manifests so duration metadata is accurate.
The training pipeline now ignores padded audio during loudness and CMVN,
does not add unused language tags to English targets, and restores the
learning-rate scheduler when resuming.

### Data Setup (required before training)

Download LibriSpeech `train-clean-100` (~6.3 GB):

```bash
# Linux / Mac / Colab
wget https://www.openslr.org/resources/12/train-clean-100.tar.gz -P backend/data/
tar -xzf backend/data/train-clean-100.tar.gz -C backend/data/

# Also download validation set
wget https://www.openslr.org/resources/12/dev-clean.tar.gz -P backend/data/
tar -xzf backend/data/dev-clean.tar.gz -C backend/data/
```

Build the manifest JSONs:

```bash
python backend/prepare_data.py \
    --librispeech_dir backend/data/LibriSpeech \
    --output_dir backend/data/manifests
```

The current data preparation script uses audio metadata to keep utterances
between 0.5 and 15 seconds. Re-run it when using older manifests.

---

### Option 2 — Quick Fine-Tune *(Recommended First)*

> ⏱️ **~2–4 hours on GPU** | Resumes from epoch 50 | Lower learning rate for stability

Reduces CTC loss from **0.83 → ~0.5** and improves WER from **~50% → ~25–35%**.

```bash
python backend/train.py \
    --train_manifest backend/data/manifests/librispeech_train100.json \
    --val_manifest backend/data/manifests/librispeech_val.json \
    --checkpoint_dir backend/checkpoints/compact_conformer \
    --resume \
    --epochs 20 \
    --batch_size 32 \
    --d_model 144 \
    --layers 6 \
    --heads 4 \
    --grad_accum 2 \
    --lr 0.0001
```

**Windows**: Just double-click `start_training.bat` — Option 2 is pre-configured and ready to run.

---

### Option 1 — Full Long Run

> ⏱️ **~8–20 hours on GPU** | 100 epochs | Bigger model for best accuracy

Trains a larger model (~10–12M params) for significantly better transcription.

> ⚠️ **Note**: Uses `d_model=256, layers=8, heads=8` — this is a **different architecture**
> from the current 3.4M checkpoint. Do **NOT** use `--resume` with this config unless you
> keep `d_model=144 --layers 6 --heads 4` to match the existing checkpoint.

```bash
python backend/train.py \
    --train_manifest backend/data/manifests/librispeech_train100.json \
    --val_manifest backend/data/manifests/librispeech_val.json \
    --checkpoint_dir backend/checkpoints/compact_conformer \
    --epochs 100 \
    --batch_size 32 \
    --d_model 256 \
    --layers 8 \
    --heads 8 \
    --grad_accum 2 \
    --lr 0.0004
```

**Windows**: Edit `start_training.bat` — comment out Option 2, uncomment Option 1 at the bottom.

---

### After Training — Deploy the New Model

1. The best checkpoint is automatically saved to `backend/checkpoints/compact_conformer/best_model.pt`
2. Restart the backend server — it auto-loads `best_model.pt` on startup
3. No code changes needed

```bash
# Linux / Mac
cd backend
python -m uvicorn server:app --host 127.0.0.1 --port 8000

# Windows
start_backend.bat
```

---

## Setup on Colab / Kaggle / Company PC

See **[TRAINING_PROMPT.md](./TRAINING_PROMPT.md)** for the full step-by-step agent prompt.

**TL;DR:**

```bash
# 1. Clone (includes pre-trained epoch-50 checkpoint)
git clone https://github.com/Hariesh-Kai/Zero_ASR.git
cd Zero_ASR

# 2. Install
pip install torch torchaudio fastapi uvicorn soundfile av numpy

# 3. Download + extract LibriSpeech data (see TRAINING_PROMPT.md)

# 4. Run Option 2 fine-tune
python backend/train.py --resume --epochs 20 --lr 0.0001 \
    --train_manifest backend/data/manifests/librispeech_train100.json \
    --val_manifest backend/data/manifests/librispeech_val.json \
    --checkpoint_dir backend/checkpoints/compact_conformer \
    --batch_size 32 --d_model 144 --layers 6 --heads 4 --grad_accum 2
```

---

## API Endpoints

The backend runs at `http://localhost:8000`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/info` | Model info, device, vocab size, param count |
| `POST` | `/api/transcribe` | Upload audio file → get transcript |
| `POST` | `/api/reload` | Hot-reload latest checkpoint (no restart needed) |
| `GET` | `/api/training/status` | Check current checkpoint epoch & loss |
| `POST` | `/api/romanize` | Convert Tamil Unicode → Romanized Latin |
| `GET` | `/api/samples` | Demo phrases for testing |
| `GET` | `/api/temp` | List temp audio files |
| `POST` | `/api/clear_temp` | Delete all temp audio files |

### Example — Transcribe

```bash
curl -X POST http://localhost:8000/api/transcribe \
  -F "file=@audio.wav" \
  -F "mode=transcription"
```

Response:
```json
{
  "text": "hi hello how are you",
  "raw_text": "hi hello how are you",
  "language": "English",
  "duration_sec": 2.1,
  "latency_ms": 38.4,
  "rtf": 0.018,
  "speedup": 54.7
}
```

---

## Current Model Status

| Metric | Value |
|---|---|
| Architecture | Conformer-CTC |
| Parameters | ~3.4M |
| Epochs trained | 50 / 50 |
| Best CTC loss | 0.8296 |
| Estimated WER | ~40–50% |
| Training data | LibriSpeech train-clean-100 |
| Checkpoint saved | `best_model.pt` (epoch 47) |

> The model is functional but needs further fine-tuning (Option 2) for production-quality transcription.
> Run Option 2 to reduce WER to ~25–35%, or Option 1 for a larger, more accurate model.

---

## Roadmap

- [x] Compact Conformer-CTC model (3.4M params)
- [x] Character-level CTC tokenizer (English + Romanized Tamil)
- [x] FastAPI backend with streaming support
- [x] React frontend with live mic recording
- [x] SpecAugment + AMP training
- [x] WER/CER evaluation during training
- [ ] **Fine-tune corrected pipeline** — rebuild manifests, then reduce WER
- [ ] **Scale up Option 1** — 10–12M param model
- [x] Prefix beam-search CTC decoding (language-model free)
- [ ] Noise augmentation (RIR + MUSAN) for mic robustness
- [ ] ONNX export for edge deployment
- [ ] Tamil audio training data

---

## License

MIT License — free to use, modify, and distribute.

---

*Built by [Hariesh Kai](https://github.com/Hariesh-Kai)*
