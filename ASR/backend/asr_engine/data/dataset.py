"""
ASR Dataset and Dynamic Batch Collation Module.
Handles variable-length audio, dynamic padding, target tokenization, and noise augmentation.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Union, Tuple, Any
import json
import torch
from torch.utils.data import Dataset
import torchaudio

from asr_engine.tokenizer.char_tokenizer import CharTokenizer
from asr_engine.tokenizer.romanizer import romanize_tamil, is_tamil_script


@dataclass
class ASRItem:
    audio_path: str
    transcript: str
    language: str = "en"  # "en" or "ta"
    speaker_id: Optional[str] = None


class ASRDataset(Dataset):
    """
    Standard ASR Dataset reading from a manifest list or JSON.
    """

    def __init__(
        self,
        items: List[ASRItem],
        tokenizer: CharTokenizer,
        target_sample_rate: int = 16000,
        max_duration_seconds: float = 15.0,
        min_duration_seconds: float = 0.5,
    ):
        self.items = items
        self.tokenizer = tokenizer
        self.target_sample_rate = target_sample_rate
        self.max_samples = int(max_duration_seconds * target_sample_rate)
        self.min_samples = int(min_duration_seconds * target_sample_rate)

    @classmethod
    def from_manifest(cls, manifest_path: Union[str, Path], tokenizer: CharTokenizer) -> "ASRDataset":
        """
        Loads dataset from a JSON manifest file formatted as:
        [
          {"audio_path": "...", "transcript": "...", "language": "en"},
          {"audio_path": "...", "transcript": "...", "language": "ta"}
        ]
        """
        manifest_path = Path(manifest_path)
        base_dir = manifest_path.parent
        with open(manifest_path, "r", encoding="utf-8") as f:
            raw_items = json.load(f)

        items = []
        for row in raw_items:
            duration = row.get("duration")
            if duration is not None and not 0.5 <= duration <= 15.0:
                continue

            path = Path(row["audio_path"])
            if not path.is_absolute():
                path = base_dir / path
            elif not path.exists():
                # Handle repository reorganization (e.g., data/ moved into backend/data/)
                alt_str = str(path).replace("K:\\ASR\\data", "K:\\ASR\\backend\\data").replace("K:/ASR/data", "K:/ASR/backend/data")
                if Path(alt_str).exists():
                    path = Path(alt_str)

            # Pre-romanize Tamil if in Tamil script
            transcript = row["transcript"]
            lang = row.get("language", "en")
            if lang == "ta" and is_tamil_script(transcript):
                transcript = romanize_tamil(transcript)

            items.append(
                ASRItem(
                    audio_path=str(path),
                    transcript=transcript,
                    language=lang,
                    speaker_id=row.get("speaker_id"),
                )
            )

        return cls(items=items, tokenizer=tokenizer)

    def __len__(self) -> int:
        return len(self.items)

    def load_audio(self, path: str) -> torch.Tensor:
        """Loads and converts audio to 16kHz mono using soundfile."""
        from asr_engine.audio.io import load_audio
        waveform, _ = load_audio(path, target_sample_rate=self.target_sample_rate)
        return waveform

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        item = self.items[idx]
        waveform = self.load_audio(item.audio_path)

        # Do not truncate audio while retaining the original transcript: that
        # creates targets which cannot be aligned by CTC. Duration filtering is
        # performed during manifest preparation.

        # Tokenize target
        token_ids = self.tokenizer.encode(item.transcript)

        return {
            "waveform": waveform,
            "waveform_len": waveform.shape[0],
            "token_ids": torch.tensor(token_ids, dtype=torch.long),
            "token_len": len(token_ids),
            "raw_transcript": item.transcript,
            "language": item.language,
        }


def asr_collate_fn(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Collate function to batch audio waveforms and token sequences with dynamic padding.
    """
    # Sort batch by audio length descending for compute efficiency
    batch = sorted(batch, key=lambda x: x["waveform_len"], reverse=True)

    max_audio_len = max(x["waveform_len"] for x in batch)
    max_token_len = max(x["token_len"] for x in batch)
    batch_size = len(batch)

    padded_waveforms = torch.zeros(batch_size, max_audio_len, dtype=torch.float32)
    audio_lengths = torch.zeros(batch_size, dtype=torch.long)

    padded_tokens = torch.zeros(batch_size, max_token_len, dtype=torch.long)
    token_lengths = torch.zeros(batch_size, dtype=torch.long)

    raw_transcripts = []
    languages = []

    for i, item in enumerate(batch):
        w = item["waveform"]
        t = item["token_ids"]

        padded_waveforms[i, : len(w)] = w
        audio_lengths[i] = len(w)

        padded_tokens[i, : len(t)] = t
        token_lengths[i] = len(t)

        raw_transcripts.append(item["raw_transcript"])
        languages.append(item["language"])

    return {
        "waveforms": padded_waveforms,
        "waveform_lengths": audio_lengths,
        "tokens": padded_tokens,
        "token_lengths": token_lengths,
        "transcripts": raw_transcripts,
        "languages": languages,
    }
