"""
Minimal Viable Prototype Training Script (Phase 1 & 2).
Validates end-to-end tensor pipeline:
Waveform -> Mel-spectrogram -> Conv2D Subsampling -> Causal Conformer -> CTC Loss -> CTC Decoding.
Trains a compact 3.2M parameter prototype to verify convergence and alignment.
"""

import os
import sys
import time
import math
import random
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

from asr_engine.audio.frontend import AudioFrontend
from asr_engine.audio.augment import SpecAugment
from asr_engine.model.ctc_model import ConformerCTC
from asr_engine.tokenizer.char_tokenizer import CharTokenizer
from asr_engine.decoding.ctc_decoder import CTCDecoder
from asr_engine.evaluation.metrics import compute_wer, compute_cer
from asr_engine.data.dataset import asr_collate_fn


class ControlledPrototypeDataset(Dataset):
    """
    Controlled audio dataset for validating gradient descent and CTC alignment.
    Generates harmonic and acoustic speech-like formant sweeps mapped to distinct phrases.
    """

    SAMPLE_PHRASES = [
        ("i went to college yesterday and met my friend", "en"),
        ("naan innaikku veettukku poren", "ta"),
        ("enakku adhu theriyadhu", "ta"),
        ("the weather is very good today", "en"),
        ("speech recognition from scratch", "en"),
        ("vanakkam nanba eppadi irukkeenga", "ta"),
        ("acoustic conformer streaming test", "en"),
        ("indha model nalla velai seiyudhu", "ta"),
    ]

    def __init__(self, num_samples: int = 120, sample_rate: int = 16000, tokenizer: CharTokenizer = None):
        self.sample_rate = sample_rate
        self.tokenizer = tokenizer or CharTokenizer()
        self.items = []

        # Deterministic seed for reproducible evaluation
        rng = random.Random(42)
        for i in range(num_samples):
            phrase, lang = self.SAMPLE_PHRASES[i % len(self.SAMPLE_PHRASES)]
            # Audio duration: 2.0 to 4.5 seconds
            duration = 2.5 + (i % 4) * 0.5
            self.items.append((phrase, lang, duration))

    def __len__(self):
        return len(self.items)

    def _synthesize_speech_like_waveform(self, phrase: str, duration: float) -> torch.Tensor:
        """
        Synthesizes structured harmonic formant sweeps correlated with phrase characters.
        This provides real acoustic structure (varying pitches, pauses, formants) for CTC to align.
        """
        n_samples = int(duration * self.sample_rate)
        t = torch.linspace(0, duration, n_samples)
        waveform = torch.zeros(n_samples)

        # Base formant frequencies based on character sequence
        char_vals = [ord(c) for c in phrase]
        n_chars = len(char_vals)
        samples_per_char = max(1, n_samples // n_chars)

        for ci, val in enumerate(char_vals):
            start = ci * samples_per_char
            end = min(n_samples, (ci + 1) * samples_per_char)
            if start >= end:
                continue

            # F0 fundamental + F1 & F2 formants
            f0 = 120.0 + (val % 30) * 4.0
            f1 = 500.0 + (val % 50) * 15.0
            f2 = 1500.0 + (val % 70) * 20.0

            sub_t = t[start:end]
            segment = (
                0.5 * torch.sin(2 * math.pi * f0 * sub_t)
                + 0.3 * torch.sin(2 * math.pi * f1 * sub_t)
                + 0.2 * torch.sin(2 * math.pi * f2 * sub_t)
            )

            # Smooth segment transitions (Hann envelope)
            seg_len = end - start
            hann = torch.hann_window(seg_len)
            segment = segment * hann

            waveform[start:end] = segment

        # Add slight background pink noise (-20dB)
        noise = torch.randn(n_samples) * 0.02
        waveform = waveform + noise

        # Normalize to [-0.9, 0.9]
        max_val = torch.max(torch.abs(waveform))
        if max_val > 0:
            waveform = waveform / max_val * 0.9

        return waveform

    def __getitem__(self, idx: int):
        phrase, lang, duration = self.items[idx]
        waveform = self._synthesize_speech_like_waveform(phrase, duration)

        lang_tag = f"<{lang}>"
        token_ids = self.tokenizer.encode(phrase, add_lang_tag=lang_tag)

        return {
            "waveform": waveform,
            "waveform_len": waveform.shape[0],
            "token_ids": torch.tensor(token_ids, dtype=torch.long),
            "token_len": len(token_ids),
            "raw_transcript": phrase,
            "language": lang,
        }


def train_prototype(
    num_epochs: int = 15,
    batch_size: int = 8,
    lr: float = 1e-3,
    checkpoint_dir: str = "checkpoints/prototype",
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== Starting Prototype Training on device: {device} ===")

    # 1. Initialize Tokenizer
    tokenizer = CharTokenizer()
    checkpoint_path = Path(checkpoint_dir)
    checkpoint_path.mkdir(parents=True, exist_ok=True)
    tokenizer.save(checkpoint_path / "vocab.json")
    print(f"Tokenizer initialized: vocab size = {tokenizer.vocab_size} tokens")

    # 2. Dataset & DataLoader
    train_dataset = ControlledPrototypeDataset(num_samples=160, tokenizer=tokenizer)
    val_dataset = ControlledPrototypeDataset(num_samples=24, tokenizer=tokenizer)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=asr_collate_fn,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=asr_collate_fn,
    )

    # 3. Model & Frontend
    frontend = AudioFrontend().to(device)
    spec_augment = SpecAugment().to(device)

    model = ConformerCTC(
        in_channels=80,
        vocab_size=tokenizer.vocab_size,
        d_model=128,
        n_layers=4,
        n_heads=4,
        conv_kernel_size=15,
        ffn_expansion=4,
        dropout=0.1,
    ).to(device)

    print(f"Conformer-CTC Model initialized with {model.parameter_count:,} trainable parameters.")
    estimated_mb = (model.parameter_count * 4) / (1024 * 1024)
    print(f"Estimated FP32 footprint: {estimated_mb:.2f} MB")

    # 4. Optimizer & Scheduler
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs, eta_min=1e-5)
    decoder = CTCDecoder(tokenizer)

    start_time = time.time()

    for epoch in range(1, num_epochs + 1):
        model.train()
        total_loss = 0.0
        batch_count = 0

        for batch in train_loader:
            waveforms = batch["waveforms"].to(device)
            waveform_lengths = batch["waveform_lengths"].to(device)
            targets = batch["tokens"].to(device)
            target_lengths = batch["token_lengths"].to(device)

            optimizer.zero_grad()

            # Feature extraction
            # Shape: (batch, time, 80)
            mel = frontend(waveforms)
            mel = spec_augment(mel)

            # Approximate mel frames from raw waveform lengths
            mel_lengths = torch.div(waveform_lengths, frontend.hop_length, rounding_mode="floor")

            # Acoustic model forward pass
            log_probs, out_lens = model(mel, input_lengths=mel_lengths)

            # CTC Loss
            loss = model.compute_loss(log_probs, targets, out_lens, target_lengths)

            if torch.isfinite(loss):
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
                optimizer.step()
                total_loss += loss.item()
                batch_count += 1

        scheduler.step()
        avg_loss = total_loss / max(1, batch_count)

        # Validation & Sample Decoding
        model.eval()
        val_wers = []
        val_cers = []
        sample_ref = ""
        sample_hyp = ""

        with torch.no_grad():
            for v_idx, batch in enumerate(val_loader):
                waveforms = batch["waveforms"].to(device)
                waveform_lengths = batch["waveform_lengths"].to(device)
                mel = frontend(waveforms)
                mel_lengths = torch.div(waveform_lengths, frontend.hop_length, rounding_mode="floor")
                log_probs, out_lens = model(mel, input_lengths=mel_lengths)

                for b in range(waveforms.shape[0]):
                    hyp = decoder.decode_logits(log_probs[b, : out_lens[b]])
                    ref = batch["transcripts"][b]

                    wer_res = compute_wer(ref, hyp)
                    cer_res = compute_cer(ref, hyp)
                    val_wers.append(wer_res["wer"])
                    val_cers.append(cer_res["cer"])

                    if not sample_ref:
                        sample_ref = ref
                        sample_hyp = hyp

        mean_wer = sum(val_wers) / max(1, len(val_wers))
        mean_cer = sum(val_cers) / max(1, len(val_cers))

        print(
            f"Epoch {epoch:02d}/{num_epochs:02d} | "
            f"Train Loss: {avg_loss:.4f} | "
            f"Val WER: {mean_wer * 100:.1f}% | "
            f"Val CER: {mean_cer * 100:.1f}%"
        )
        if epoch % 3 == 0 or epoch == num_epochs:
            print(f"  [Sample Ref]: '{sample_ref}'")
            print(f"  [Sample Hyp]: '{sample_hyp}'")

    elapsed = time.time() - start_time
    print(f"\n=== Training Complete in {elapsed:.1f} seconds! ===")

    # Save final model
    model_save_path = checkpoint_path / "model.pt"
    model.save_checkpoint(model_save_path, optimizer=optimizer, epoch=num_epochs, loss=avg_loss)
    print(f"Saved prototype model checkpoint to: {model_save_path}")


if __name__ == "__main__":
    train_prototype(num_epochs=12, batch_size=8, lr=1e-3)
