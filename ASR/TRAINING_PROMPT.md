# 🤖 Zero ASR — Training Agent Prompt

> **READ THIS FIRST.** This file is written for an AI coding agent (e.g. Gemini, GPT, Claude)
> running in Google Colab, Kaggle, or a company PC. It explains the full context of this
> project and exactly what training work needs to be done.

---

## 📌 Project Overview

**Zero ASR** is a custom, fully offline Automatic Speech Recognition (ASR) system built from scratch.
It uses a **Compact Conformer-CTC** acoustic model trained on **LibriSpeech train-clean-100**
to transcribe English (and optionally Romanized Tamil) speech without any cloud dependency.

- **Architecture**: Conformer-CTC (Character-level CTC decoding)
- **Current Model Size**: ~3.4M parameters (`d_model=144`, 6 layers, 4 heads)
- **Tokenizer**: Character-level (32 tokens: a-z + special tokens)
- **Training Data**: LibriSpeech `train-clean-100` (~28,539 utterances, ~100 hours)
- **Backend**: FastAPI server (`backend/server.py`)
- **Frontend**: React/Vite app (`frontend/`)

---

## ⚠️ Current Problem (Why Training is Needed)

The model was trained for **50 epochs** (CTC loss = 0.83), but transcription quality is poor.

**Example:**
- User said: `"hi hello how are you"`
- Model output: `"An ie I lo oa hi"` ← completely wrong

### Root Causes:
1. **CTC loss 0.83 is too high** — needs to drop below 0.4 for acceptable WER
2. **Model is too small** (3.4M params) — ideally needs 8–12M for better accuracy
3. **Only 50 epochs** — needs more training
4. **Trained on clean studio audio** — real mic audio is noisier (mismatch)

---

## ✅ What You Need to Do — Two Options

### 🟡 OPTION 2 — Quick Fine-Tune (Do This First, ~2–4 hours on GPU)

**Goal**: Resume from the existing epoch-50 checkpoint and fine-tune with a lower learning rate.
This should meaningfully reduce CTC loss and improve transcription quality.

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

**What `--resume` does**: Automatically loads `backend/checkpoints/compact_conformer/latest_model.pt`
and continues training from epoch 50 onward.

**Expected outcome**: CTC loss should drop from ~0.83 → ~0.5–0.6, WER from ~50% → ~25–35%.

---

### 🔴 OPTION 1 — Long Full Run (Do This When You Have Time, ~8–20 hours on GPU)

**Goal**: Run a full 100-epoch training pass with a bigger model config for best accuracy.
This replaces the current small model with a significantly better one (~10–12M params).

```bash
python backend/train.py \
    --train_manifest backend/data/manifests/librispeech_train100.json \
    --val_manifest backend/data/manifests/librispeech_val.json \
    --checkpoint_dir backend/checkpoints/compact_conformer \
    --resume \
    --epochs 100 \
    --batch_size 32 \
    --d_model 256 \
    --layers 8 \
    --heads 8 \
    --grad_accum 2 \
    --lr 0.0004
```

> ⚠️ **Note on `--d_model 256 --layers 8 --heads 8`**: This is a bigger model (~10–12M params).
> If you're resuming from the existing 3.4M checkpoint, you CANNOT resume (architecture mismatch).
> In that case, remove `--resume` to start fresh. If you want to keep the same architecture
> (144/6/4), add `--resume` and keep `--d_model 144 --layers 6 --heads 4`.

---

## 🛠️ Environment Setup (Colab / Kaggle / Company PC)

### Step 1 — Clone the repo
```bash
git clone https://github.com/Hariesh-Kai/Zero_ASR.git
cd Zero_ASR
```

### Step 2 — Install dependencies
```bash
pip install torch torchaudio fastapi uvicorn soundfile pyav numpy
```

### Step 3 — Download LibriSpeech data
The training data is NOT in the repo (too large). Download it:

```bash
# Download train-clean-100 (~6.3 GB)
wget https://www.openslr.org/resources/12/train-clean-100.tar.gz -P backend/data/
tar -xzf backend/data/train-clean-100.tar.gz -C backend/data/

# Then generate the manifest JSON
python backend/prepare_data.py \
    --librispeech_dir backend/data/LibriSpeech \
    --output_dir backend/data/manifests
```

### Step 4 — Download dev-clean for validation
```bash
wget https://www.openslr.org/resources/12/dev-clean.tar.gz -P backend/data/
tar -xzf backend/data/dev-clean.tar.gz -C backend/data/
```

### Step 5 — Download existing checkpoint (Option 2 only)
If you want to resume from the pre-trained epoch-50 checkpoint, download it from
the project owner (Hariesh) separately — checkpoint `.pt` files are not in the repo
(they are in `.gitignore`). The owner will share via Google Drive or similar.

If starting fresh (Option 1 with new architecture), skip this step.

### Step 6 — Run training
See **Option 2** or **Option 1** commands above.

---

## 📂 Key File Locations

| File | Purpose |
|------|---------|
| `backend/train.py` | Main training script |
| `backend/prepare_data.py` | Builds manifest JSONs from LibriSpeech |
| `backend/asr_engine/model/ctc_model.py` | Conformer-CTC architecture |
| `backend/asr_engine/audio/frontend.py` | Mel-spectrogram feature extraction |
| `backend/asr_engine/tokenizer/char_tokenizer.py` | Character tokenizer (32 vocab) |
| `backend/checkpoints/compact_conformer/vocab.json` | Vocabulary file (must be present) |
| `backend/checkpoints/compact_conformer/best_model.pt` | Best model (not in repo) |
| `backend/checkpoints/compact_conformer/latest_model.pt` | Latest epoch checkpoint (not in repo) |

---

## 📊 Training Progress Monitoring

The training script prints a table every epoch:

```
Epoch   Train Loss    Val Loss    Val WER     Val CER   Time (s)
======================================================================
51/70   0.7123        0.6891      38.2%       22.1%     312.4
52/70   0.6844        0.6612      35.7%       20.8%     309.8
...
```

Every 3 epochs it also prints a sample reference vs hypothesis:
```
  [Ref]: 'the quick brown fox'
  [Hyp]: 'the kuick brwn fox'
```

**Target**: Get Val WER below 25% and CTC loss below 0.5.

---

## 🎯 After Training

1. The best checkpoint is saved to `backend/checkpoints/compact_conformer/best_model.pt`
2. Download this `.pt` file and copy it to the same path on the home/company PC
3. Restart the backend server:
   ```bash
   python backend/server.py
   # or use start_backend.bat on Windows
   ```
4. The server auto-loads `best_model.pt` on startup — no code changes needed.

---

## 📞 Owner Contact

**Project**: Zero ASR
**Owner**: Hariesh Kai
**GitHub**: https://github.com/Hariesh-Kai/Zero_ASR
