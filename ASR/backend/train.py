"""
Complete ASR Acoustic Model Training Script.
Supports training compact Conformer-CTC models (6M - 12M parameters) on English and Romanized Tamil manifests.
Features:
- PyTorch AMP (Automatic Mixed Precision, bf16/fp16)
- SpecAugment time/frequency masking
- Dynamic batch collation with audio length sorting
- Warmup + Cosine Annealing learning rate schedule
- Periodic evaluation on validation manifest (WER & CER calculation)
- Best checkpoint tracking
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, Any

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from asr_engine.audio.frontend import AudioFrontend
from asr_engine.audio.augment import SpecAugment
from asr_engine.model.ctc_model import ConformerCTC
from asr_engine.tokenizer.char_tokenizer import CharTokenizer
from asr_engine.decoding.ctc_decoder import CTCDecoder
from asr_engine.data.dataset import ASRDataset, asr_collate_fn
from asr_engine.evaluation.metrics import compute_wer, compute_cer


def train_epoch(
    model: ConformerCTC,
    dataloader: DataLoader,
    frontend: AudioFrontend,
    spec_augment: SpecAugment,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    use_amp: bool = True,
    scaler: Optional[torch.amp.GradScaler] = None,
    grad_accum_steps: int = 1,
    scheduler: Optional[Any] = None,
) -> float:
    model.train()
    spec_augment.train()
    total_loss = 0.0
    num_batches = 0
    optimizer.zero_grad()

    for step, batch in enumerate(dataloader):
        waveforms = batch["waveforms"].to(device, non_blocking=True)
        waveform_lengths = batch["waveform_lengths"].to(device, non_blocking=True)
        targets = batch["tokens"].to(device, non_blocking=True)
        target_lengths = batch["token_lengths"].to(device, non_blocking=True)

        with torch.no_grad():
            mel = frontend(waveforms, lengths=waveform_lengths)
            mel = spec_augment(mel)
            mel_lengths = torch.clamp(
                torch.div(waveform_lengths, frontend.hop_length, rounding_mode="floor") + 1,
                max=mel.size(1),
            )

        with torch.amp.autocast(device_type="cuda" if device.type == "cuda" else "cpu", enabled=use_amp):
            log_probs, out_lens = model(mel, input_lengths=mel_lengths)
            loss = model.compute_loss(log_probs, targets, out_lens, target_lengths)
            loss = loss / grad_accum_steps

        if torch.isfinite(loss):
            if scaler is not None:
                scaler.scale(loss).backward()
            else:
                loss.backward()

            total_loss += loss.item() * grad_accum_steps
            num_batches += 1

        if (step + 1) % grad_accum_steps == 0:
            if scaler is not None:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
                scaler.step(optimizer)
                scaler.update()
            else:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
                optimizer.step()
            optimizer.zero_grad()
            if scheduler is not None:
                scheduler.step()

    return total_loss / max(1, num_batches)


@torch.no_grad()
def evaluate(
    model: ConformerCTC,
    dataloader: DataLoader,
    frontend: AudioFrontend,
    decoder: CTCDecoder,
    device: torch.device,
) -> dict:
    model.eval()
    frontend.eval()
    total_loss = 0.0
    num_batches = 0
    all_refs = []
    all_hyps = []

    for batch in dataloader:
        waveforms = batch["waveforms"].to(device, non_blocking=True)
        waveform_lengths = batch["waveform_lengths"].to(device, non_blocking=True)
        targets = batch["tokens"].to(device, non_blocking=True)
        target_lengths = batch["token_lengths"].to(device, non_blocking=True)
        raw_transcripts = batch["transcripts"]

        mel = frontend(waveforms, lengths=waveform_lengths)
        mel_lengths = torch.clamp(
            torch.div(waveform_lengths, frontend.hop_length, rounding_mode="floor") + 1,
            max=mel.size(1),
        )

        log_probs, out_lens = model(mel, input_lengths=mel_lengths)
        loss = model.compute_loss(log_probs, targets, out_lens, target_lengths)

        if torch.isfinite(loss):
            total_loss += loss.item()
            num_batches += 1

        for i in range(log_probs.size(0)):
            T_i = out_lens[i].item()
            pred_text = decoder.decode_logits(log_probs[i, :T_i])
            all_hyps.append(pred_text)
            all_refs.append(raw_transcripts[i])

    wer_res = compute_wer(all_refs, all_hyps)
    cer_res = compute_cer(all_refs, all_hyps)

    return {
        "val_loss": total_loss / max(1, num_batches),
        "wer": wer_res["wer"],
        "cer": cer_res["cer"],
        "sample_ref": all_refs[0] if all_refs else "",
        "sample_hyp": all_hyps[0] if all_hyps else "",
    }


def train(
    train_manifest: str,
    val_manifest: str,
    checkpoint_dir: str = "checkpoints/compact_conformer",
    num_epochs: int = 25,
    batch_size: int = 16,
    lr: float = 8e-4,
    d_model: int = 144,
    n_heads: int = 4,
    num_layers: int = 8,
    grad_accum_steps: int = 2,
    use_amp: bool = True,
    resume: bool = False,
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== Starting Training on {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}) ===")

    ckpt_dir = Path(checkpoint_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load or initialize tokenizer
    vocab_path = ckpt_dir / "vocab.json"
    if vocab_path.exists():
        tokenizer = CharTokenizer.load(vocab_path)
    else:
        tokenizer = CharTokenizer()
        tokenizer.save(vocab_path)
    print(f"Tokenizer: vocab size = {tokenizer.vocab_size} tokens")

    # 2. Datasets & Loaders
    train_dataset = ASRDataset.from_manifest(train_manifest, tokenizer=tokenizer)
    val_dataset = ASRDataset.from_manifest(val_manifest, tokenizer=tokenizer)
    print(f"Loaded {len(train_dataset)} train samples, {len(val_dataset)} val samples.")

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=asr_collate_fn,
        num_workers=0,  # Windows safe default
        pin_memory=torch.cuda.is_available(),
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=asr_collate_fn,
        num_workers=0,
    )

    # 3. Model Architecture
    model = ConformerCTC(
        in_channels=80,
        vocab_size=tokenizer.vocab_size,
        d_model=d_model,
        n_heads=n_heads,
        num_layers=num_layers,
        conv_kernel_size=31,
        dropout=0.1,
    ).to(device)

    param_count = model.parameter_count
    print(f"Model architecture: d_model={d_model}, layers={num_layers}, heads={n_heads}")
    print(f"Total parameters: {param_count:,} (~{param_count * 4 / (1024**2):.2f} MB FP32)")

    # 4. Optimizer, Scheduler, AMP Scaler
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4, betas=(0.9, 0.98))
    total_steps = len(train_loader) * num_epochs // grad_accum_steps
    warmup_steps = int(0.1 * total_steps)

    def lr_lambda(current_step: int):
        if current_step < warmup_steps:
            return float(current_step) / float(max(1, warmup_steps))
        progress = float(current_step - warmup_steps) / float(max(1, total_steps - warmup_steps))
        return max(0.05, 0.5 * (1.0 + math.cos(math.pi * progress)))

    import math
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_lambda)
    scaler = torch.amp.GradScaler("cuda") if (use_amp and device.type == "cuda") else None

    frontend = AudioFrontend().to(device)
    spec_augment = SpecAugment(freq_mask_param=15, time_mask_param=35, num_freq_masks=2, num_time_masks=2)
    decoder = CTCDecoder(tokenizer)

    best_val_cer = 1.0
    start_epoch = 1
    if resume and (ckpt_dir / "latest_model.pt").exists():
        print(f"Resuming training from {ckpt_dir / 'latest_model.pt'}...")
        ckpt = torch.load(ckpt_dir / "latest_model.pt", map_location=device)
        model.load_state_dict(ckpt["state_dict"])
        if "optimizer" in ckpt:
            try:
                optimizer.load_state_dict(ckpt["optimizer"])
                # The command-line learning rate must remain authoritative
                # when fine-tuning an older checkpoint.
                for group in optimizer.param_groups:
                    group["lr"] = lr
            except Exception:
                pass
        if "scheduler" in ckpt:
            try:
                scheduler.load_state_dict(ckpt["scheduler"])
            except Exception:
                pass
        start_epoch = ckpt.get("epoch", 0) + 1
        best_val_cer = ckpt.get("best_val_cer", best_val_cer)
        print(f"Resumed from epoch {start_epoch - 1}")

    print("\n" + "=" * 70)
    print(f"{'Epoch':<8}{'Train Loss':<14}{'Val Loss':<12}{'Val WER':<12}{'Val CER':<10}{'Time (s)':<10}")
    print("=" * 70)

    for epoch in range(start_epoch, start_epoch + num_epochs):
        t0 = time.time()
        train_loss = train_epoch(
            model=model,
            dataloader=train_loader,
            frontend=frontend,
            spec_augment=spec_augment,
            optimizer=optimizer,
            device=device,
            use_amp=use_amp,
            scaler=scaler,
            grad_accum_steps=grad_accum_steps,
            scheduler=scheduler,
        )
        epoch_sec = time.time() - t0

        val_metrics = evaluate(
            model=model,
            dataloader=val_loader,
            frontend=frontend,
            decoder=decoder,
            device=device,
        )

        print(
            f"{epoch:02d}/{num_epochs:02d}   "
            f"{train_loss:<14.4f}"
            f"{val_metrics['val_loss']:<12.4f}"
            f"{val_metrics['wer']*100:<11.1f}%"
            f"{val_metrics['cer']*100:<9.1f}%"
            f"{epoch_sec:<10.1f}"
        )

        if epoch % 3 == 0 or epoch == num_epochs:
            print(f"  [Ref]: '{val_metrics['sample_ref']}'")
            print(f"  [Hyp]: '{val_metrics['sample_hyp']}'")

        if val_metrics["cer"] < best_val_cer:
            best_val_cer = val_metrics["cer"]
            model.save_checkpoint(
                ckpt_dir / "best_model.pt",
                optimizer=optimizer,
                scheduler=scheduler,
                epoch=epoch,
                loss=val_metrics["val_loss"],
                best_val_cer=best_val_cer,
            )

        model.save_checkpoint(
            ckpt_dir / "latest_model.pt",
            optimizer=optimizer,
            scheduler=scheduler,
            epoch=epoch,
            loss=val_metrics["val_loss"],
            best_val_cer=best_val_cer,
        )

    print("\nTraining completed! Best checkpoint saved to:", (ckpt_dir / "best_model.pt").resolve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Compact Conformer-CTC ASR")
    parser.add_argument("--train_manifest", required=True, help="Path to training manifest JSON")
    parser.add_argument("--val_manifest", required=True, help="Path to validation manifest JSON")
    parser.add_argument("--checkpoint_dir", default="checkpoints/compact_conformer")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=8e-4)
    parser.add_argument("--d_model", type=int, default=144)
    parser.add_argument("--layers", type=int, default=8)
    parser.add_argument("--heads", type=int, default=4)
    parser.add_argument("--grad_accum", type=int, default=2)
    parser.add_argument("--no_amp", action="store_true")
    parser.add_argument("--resume", action="store_true", help="Resume from latest_model.pt if available")

    args = parser.parse_args()
    train(
        train_manifest=args.train_manifest,
        val_manifest=args.val_manifest,
        checkpoint_dir=args.checkpoint_dir,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        d_model=args.d_model,
        num_layers=args.layers,
        n_heads=args.heads,
        grad_accum_steps=args.grad_accum,
        use_amp=not args.no_amp,
        resume=args.resume,
    )
