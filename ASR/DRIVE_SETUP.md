# Google Drive Storage Setup

Use Google Drive for the LibriSpeech dataset, manifests, and CPU training
checkpoints when local disk space is limited.

## Recommended: Google Colab

Google Colab has built-in Google Drive support and is the most reliable option
for this project.

1. Upload or clone the `ASR` project in Colab.
2. Run:

```python
from google.colab import drive
drive.mount('/content/drive')
```

3. Create a project folder in Drive:

```bash
mkdir -p /content/drive/MyDrive/Zero_ASR/data
mkdir -p /content/drive/MyDrive/Zero_ASR/checkpoints/compact_conformer
mkdir -p /content/drive/MyDrive/Zero_ASR/checkpoints/cpu_finetune
```

4. Put these files in the Drive source checkpoint folder:

```text
/content/drive/MyDrive/Zero_ASR/checkpoints/compact_conformer/latest_model.pt
/content/drive/MyDrive/Zero_ASR/checkpoints/compact_conformer/vocab.json
```

5. Download the dataset directly into Drive. The project script normally writes
under the repository, so for Drive storage use a Drive data directory and build
manifests whose `audio_path` values point to that directory. A simple approach
is:

```bash
cd /content/drive/MyDrive/Zero_ASR
python /content/ASR/backend/prepare_data.py
```

If the script is run from the cloned project, edit its `DATA_DIR` location for
that Colab copy before downloading, or download/extract LibriSpeech into:

```text
/content/drive/MyDrive/Zero_ASR/data/librispeech/
```

The archive should also be stored there if you want to resume extraction:

```text
/content/drive/MyDrive/Zero_ASR/data/train-clean-100.tar.gz
```

6. Run the isolated five-epoch CPU trainer with all large paths on Drive:

```bash
cd /content/ASR
python backend/train_cpu_increment.py \
  --train_manifest /content/drive/MyDrive/Zero_ASR/data/manifests/librispeech_train100.json \
  --val_manifest /content/drive/MyDrive/Zero_ASR/data/manifests/librispeech_val.json \
  --source_model_dir /content/drive/MyDrive/Zero_ASR/checkpoints/compact_conformer \
  --checkpoint_dir /content/drive/MyDrive/Zero_ASR/checkpoints/cpu_finetune
```

Repeat the same command for each additional five-epoch increment.

## Alternative: rclone On Linux

Use this only on a Linux machine or container where FUSE mounts are permitted.
This current VS Code container does not have `rclone` or `fusermount3`
available, so it cannot be mounted here without additional system setup.

Install rclone and FUSE:

```bash
sudo apt update
sudo apt install -y rclone fuse3
```

Configure Google Drive interactively:

```bash
rclone config
```

Choose:

```text
n                 New remote
name: gdrive
Storage: Google Drive
```

Open the browser authorization URL, sign in to the Google account containing
the Drive folder, approve access, and finish the configuration. The OAuth
refresh token is stored in the local rclone configuration. Never commit or
share that file.

Test access:

```bash
rclone lsd gdrive:
```

Mount the project folder:

```bash
mkdir -p "$HOME/gdrive"
rclone mount gdrive:Zero_ASR "$HOME/gdrive" \
  --vfs-cache-mode full \
  --dir-cache-time 30s \
  --daemon
```

Then use paths such as:

```text
$HOME/gdrive/data/manifests/librispeech_train100.json
$HOME/gdrive/checkpoints/compact_conformer
$HOME/gdrive/checkpoints/cpu_finetune
```

Run training:

```bash
cd /workspaces/Zero_ASR/ASR
source venv/bin/activate
python backend/train_cpu_increment.py \
  --train_manifest "$HOME/gdrive/data/manifests/librispeech_train100.json" \
  --val_manifest "$HOME/gdrive/data/manifests/librispeech_val.json" \
  --source_model_dir "$HOME/gdrive/checkpoints/compact_conformer" \
  --checkpoint_dir "$HOME/gdrive/checkpoints/cpu_finetune"
```

Unmount when finished:

```bash
fusermount3 -u "$HOME/gdrive"
```

## What Is Needed

- A Google account with enough Drive storage for LibriSpeech and checkpoints.
- Permission to create or use a Drive folder.
- Google OAuth authorization for Colab or rclone.
- A mounted Drive path visible to Python.
- Manifests whose `audio_path` values point to audio files visible through that
  mounted path.

No API key or password should be sent to the coding agent. Complete the Google
login directly in the browser or terminal authorization flow.

## Important Limitation

Google Drive is cloud storage, not a local filesystem. Training directly over a
Drive mount can be slow, especially for thousands of audio files. Colab with a
Drive mount is the recommended route. For best performance, copy a working
subset or cached dataset to the machine running training, while keeping
checkpoints on Drive.
