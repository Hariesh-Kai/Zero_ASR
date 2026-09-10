@echo off
title Antigravity ASR — Model Fine-Tuning
color 0A
echo.
echo ============================================================
echo  Antigravity ASR — Fine-Tuning Compact Conformer-CTC
echo  Mode    : OPTION 2 — Low-LR Fine-tune (resume from ep 50)
echo  Dataset : LibriSpeech train-clean-100 (28,539 utterances)
echo  GPU     : NVIDIA GeForce RTX 5050 Laptop GPU
echo ============================================================
echo.
echo  Resuming from existing checkpoint (epoch 50).
echo  Fine-tuning with reduced LR=0.0001 for 20 more epochs.
echo  Checkpoints saved to: backend\checkpoints\compact_conformer\
echo  Press Ctrl+C to stop at any time.
echo.
cd /d "%~dp0"

:: ---------------------------------------------------------------
:: OPTION 2 (ACTIVE): Low-LR fine-tune — resumes from epoch 50
:: ~2-4 hours on RTX 5050. Run this first for quick improvement.
:: ---------------------------------------------------------------
".venv\Scripts\python.exe" backend\train.py ^
    --train_manifest backend\data\manifests\librispeech_train100.json ^
    --val_manifest backend\data\manifests\librispeech_val.json ^
    --checkpoint_dir backend\checkpoints\compact_conformer ^
    --resume ^
    --epochs 20 ^
    --batch_size 32 ^
    --d_model 144 ^
    --layers 6 ^
    --heads 4 ^
    --grad_accum 2 ^
    --lr 0.0001

:: ---------------------------------------------------------------
:: OPTION 1 (when ready): Long run — 100 epochs from scratch
:: Comment out Option 2 above and uncomment Option 1 below.
:: ~8-20 hours on RTX 5050.
:: ---------------------------------------------------------------
:: ".venv\Scripts\python.exe" backend\train.py ^
::     --train_manifest backend\data\manifests\librispeech_train100.json ^
::     --val_manifest backend\data\manifests\librispeech_val.json ^
::     --checkpoint_dir backend\checkpoints\compact_conformer ^
::     --resume ^
::     --epochs 100 ^
::     --batch_size 32 ^
::     --d_model 144 ^
::     --layers 6 ^
::     --heads 4 ^
::     --grad_accum 2 ^
::     --lr 0.0004

echo.
echo ============================================================
echo  Fine-tuning complete! Best checkpoint saved.
echo  Restart your backend to load the improved model.
echo ============================================================
pause
