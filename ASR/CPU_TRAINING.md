# CPU Incremental Training

This workflow continues the existing epoch-50 model on CPU without changing
the original GPU checkpoint directory.

## Storage

Original GPU checkpoints remain in:

```text
backend/checkpoints/compact_conformer/
```

CPU checkpoints are stored separately in:

```text
backend/checkpoints/cpu_finetune/
```

For Google Drive paths, see [DRIVE_SETUP.md](DRIVE_SETUP.md).

## Run Five Epochs

Activate the environment and prepare the LibriSpeech manifests first:

```bash
source venv/bin/activate
python backend/prepare_data.py
```

Run the isolated trainer:

```bash
python backend/train_cpu_increment.py
```

Every invocation trains exactly five additional epochs. The first run seeds
`cpu_finetune` from the original epoch-50 `latest_model.pt`; later runs resume
from the CPU checkpoint. Repeat the same command for each five-epoch increment.

For Drive-backed training, pass these options:

```bash
python backend/train_cpu_increment.py \
	--train_manifest /content/drive/MyDrive/Zero_ASR/data/manifests/librispeech_train100.json \
	--val_manifest /content/drive/MyDrive/Zero_ASR/data/manifests/librispeech_val.json \
	--source_model_dir /content/drive/MyDrive/Zero_ASR/checkpoints/compact_conformer \
	--checkpoint_dir /content/drive/MyDrive/Zero_ASR/checkpoints/cpu_finetune
```

The original GPU checkpoints are never overwritten by this script.
