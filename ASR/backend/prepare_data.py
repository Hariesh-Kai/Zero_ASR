import sys
import os
import ssl
import json
import time
import tarfile
import urllib.request
from pathlib import Path

# Force UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Bypass SSL hostname mismatch for openslr.org CDN
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

LIBRISPEECH_BASE = "https://www.openslr.org/resources/12"

SPLITS = {
    "train-clean-100": {
        "url": f"{LIBRISPEECH_BASE}/train-clean-100.tar.gz",
        "size_gb": 6.3,
    },
    "dev-clean": {
        "url": f"{LIBRISPEECH_BASE}/dev-clean.tar.gz",
        "size_gb": 0.34,
    },
}

DATA_DIR = Path(__file__).resolve().parent / "data"
LIBRISPEECH_DIR = DATA_DIR / "librispeech"
MANIFEST_DIR = DATA_DIR / "manifests"
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
LIBRISPEECH_DIR.mkdir(parents=True, exist_ok=True)


def _progress_hook(downloaded, block_size, total_size):
    if total_size > 0:
        pct = downloaded * block_size / total_size * 100
        mb = downloaded * block_size / (1024 ** 2)
        total_mb = total_size / (1024 ** 2)
        print(f"\r  {pct:.1f}%  {mb:.1f} / {total_mb:.1f} MB", end="", flush=True)


def download_split(name: str, info: dict):
    archive_path = DATA_DIR / f"{name}.tar.gz"
    extract_dir = LIBRISPEECH_DIR / "LibriSpeech" / name

    if extract_dir.exists() and any(extract_dir.rglob("*.flac")):
        print(f"[{name}] Already extracted at {extract_dir}. Skipping download.")
        return True

    if not archive_path.exists():
        print(f"\n[{name}] Downloading {info['size_gb']:.1f} GB from OpenSLR...")
        print(f"  URL: {info['url']}")
        start = time.time()
        try:
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_ctx))
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(info["url"], archive_path, reporthook=_progress_hook)
            elapsed = time.time() - start
            print(f"\n  Downloaded in {elapsed:.0f}s ({info['size_gb'] * 1024 / elapsed:.1f} MB/s)")
        except Exception as e:
            print(f"\n  ERROR downloading: {e}")
            if archive_path.exists():
                archive_path.unlink()
            return False
    else:
        print(f"[{name}] Archive already exists at {archive_path}. Extracting...")

    print(f"[{name}] Extracting archive to {LIBRISPEECH_DIR}...")
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(LIBRISPEECH_DIR)
        print(f"[{name}] Extraction complete.")
    except Exception as e:
        print(f"  ERROR extracting: {e}")
        return False

    return True


def build_manifest(split_name: str, output_path: Path, limit: int = None):
    """
    Walks a LibriSpeech split directory and builds a JSON manifest.
    Each entry: {audio_path, transcript, language, speaker_id, duration}
    """
    split_dir = LIBRISPEECH_DIR / "LibriSpeech" / split_name
    if not split_dir.exists():
        print(f"  ERROR: {split_dir} does not exist. Cannot build manifest.")
        return 0

    items = []
    for trans_file in sorted(split_dir.rglob("*.trans.txt")):
        speaker_dir = trans_file.parent
        with open(trans_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ", 1)
                if len(parts) != 2:
                    continue
                utterance_id, transcript = parts
                audio_path = speaker_dir / f"{utterance_id}.flac"
                if not audio_path.exists():
                    continue
                transcript = transcript.lower().strip()

                # Fast duration estimate from file size (FLAC @ ~16kHz mono ~≈ 1 MB/min)
                size_bytes = audio_path.stat().st_size
                est_duration = size_bytes / (16000 * 2)  # rough FLAC estimate

                items.append({
                    "audio_path": str(audio_path.resolve()).replace("\\", "\\\\"),
                    "transcript": transcript,
                    "language": "en",
                    "speaker_id": utterance_id.split("-")[0],
                    "duration": round(est_duration, 3),
                })

    # Sort by duration ascending (helps with efficient batching)
    items.sort(key=lambda x: x["duration"])

    if limit:
        items = items[:limit]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"  Built manifest: {output_path.name} — {len(items)} utterances")
    return len(items)


def main():
    print("=" * 60)
    print("Antigravity ASR — Data Preparation")
    print("=" * 60)

    # Step 1: Download missing splits
    for split_name, info in SPLITS.items():
        ok = download_split(split_name, info)
        if not ok and split_name == "train-clean-100":
            print("\nWARNING: Could not download train-clean-100.")
            print("Training will use dev-clean only (limited accuracy).")

    # Step 2: Build manifests
    print("\n--- Building Manifests ---")

    train_100_dir = LIBRISPEECH_DIR / "LibriSpeech" / "train-clean-100"
    dev_clean_dir = LIBRISPEECH_DIR / "LibriSpeech" / "dev-clean"

    if train_100_dir.exists():
        total = build_manifest(
            "train-clean-100",
            MANIFEST_DIR / "librispeech_train100.json",
        )
        # Val split: use dev-clean
        build_manifest(
            "dev-clean",
            MANIFEST_DIR / "librispeech_val.json",
        )
        print(f"\n[SUCCESS] train-clean-100 manifest ready: {total} utterances (~100 hours)")
        print(f"  Training manifest: {MANIFEST_DIR / 'librispeech_train100.json'}")
        print(f"  Validation manifest: {MANIFEST_DIR / 'librispeech_val.json'}")
    else:
        print("\n[Fallback] train-clean-100 not available. Using dev-clean only.")
        # Split dev-clean 90/10
        dev_items_path = MANIFEST_DIR / "librispeech_dev_all.json"
        build_manifest("dev-clean", dev_items_path)
        with open(dev_items_path, "r") as f:
            all_items = json.load(f)

        split_idx = int(len(all_items) * 0.9)
        train_items = all_items[:split_idx]
        val_items = all_items[split_idx:]

        train_path = MANIFEST_DIR / "librispeech_train.json"
        val_path = MANIFEST_DIR / "librispeech_val.json"
        with open(train_path, "w") as f:
            json.dump(train_items, f, indent=2)
        with open(val_path, "w") as f:
            json.dump(val_items, f, indent=2)
        print(f"  Train: {len(train_items)}, Val: {len(val_items)} (from dev-clean split)")


if __name__ == "__main__":
    main()
