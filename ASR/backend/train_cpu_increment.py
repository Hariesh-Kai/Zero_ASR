"""Run one small, isolated CPU fine-tuning increment.

This wrapper intentionally leaves the original GPU training script and
checkpoint directory untouched. Each invocation trains five more epochs and
stores the result in checkpoints/cpu_finetune.
"""

import argparse
import os
import shutil
from pathlib import Path

# Must be set before importing torch through train.py.
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from train import train


EPOCHS_PER_RUN = 5
DEFAULT_MODEL_DIR = Path(__file__).resolve().parent / "checkpoints" / "compact_conformer"
DEFAULT_CPU_DIR = Path(__file__).resolve().parent / "checkpoints" / "cpu_finetune"
DEFAULT_TRAIN_MANIFEST = Path(__file__).resolve().parent / "data" / "manifests" / "librispeech_train100.json"
DEFAULT_VAL_MANIFEST = Path(__file__).resolve().parent / "data" / "manifests" / "librispeech_val.json"


def initialize_cpu_checkpoint(source_dir: Path, cpu_dir: Path) -> None:
    """Seed the isolated CPU run from the existing model once."""
    cpu_dir.mkdir(parents=True, exist_ok=True)
    cpu_latest = cpu_dir / "latest_model.pt"
    source_latest = source_dir / "latest_model.pt"

    if cpu_latest.exists():
        return
    if not source_latest.exists():
        raise FileNotFoundError(f"Existing checkpoint not found: {source_latest}")

    shutil.copy2(source_latest, cpu_latest)
    source_vocab = source_dir / "vocab.json"
    cpu_vocab = cpu_dir / "vocab.json"
    if source_vocab.exists() and not cpu_vocab.exists():
        shutil.copy2(source_vocab, cpu_vocab)
    print(f"Seeded isolated CPU checkpoint from {source_latest}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run exactly five CPU fine-tuning epochs")
    parser.add_argument("--train_manifest", default=str(DEFAULT_TRAIN_MANIFEST))
    parser.add_argument("--val_manifest", default=str(DEFAULT_VAL_MANIFEST))
    parser.add_argument("--checkpoint_dir", default=str(DEFAULT_CPU_DIR))
    parser.add_argument(
        "--source_model_dir",
        default=str(DEFAULT_MODEL_DIR),
        help="Directory containing the initial latest_model.pt and vocab.json",
    )
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--grad_accum", type=int, default=4)
    parser.add_argument("--lr", type=float, default=0.0001)
    args = parser.parse_args()

    train_manifest = Path(args.train_manifest)
    val_manifest = Path(args.val_manifest)
    if not train_manifest.exists():
        raise FileNotFoundError(f"Training manifest not found: {train_manifest}")
    if not val_manifest.exists():
        raise FileNotFoundError(f"Validation manifest not found: {val_manifest}")

    cpu_dir = Path(args.checkpoint_dir)
    source_model_dir = Path(args.source_model_dir)
    initialize_cpu_checkpoint(source_model_dir, cpu_dir)

    print(f"Running {EPOCHS_PER_RUN} CPU epochs")
    print(f"Source checkpoints preserved in: {source_model_dir}")
    print(f"CPU checkpoints stored in: {cpu_dir}")

    train(
        train_manifest=str(train_manifest),
        val_manifest=str(val_manifest),
        checkpoint_dir=str(cpu_dir),
        num_epochs=EPOCHS_PER_RUN,
        batch_size=args.batch_size,
        lr=args.lr,
        d_model=144,
        n_heads=4,
        num_layers=6,
        grad_accum_steps=args.grad_accum,
        use_amp=False,
        resume=True,
    )


if __name__ == "__main__":
    main()
