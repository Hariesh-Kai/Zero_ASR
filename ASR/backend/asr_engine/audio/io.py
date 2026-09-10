"""
Audio I/O Utility.
Uses soundfile as primary high-speed decoder, with PyAV (FFmpeg) universal fallback
to guarantee seamless decoding of any format (.wav, .webm, .mp3, .ogg, .flac, .m4a, .aac).
"""

from pathlib import Path
from typing import Tuple, Union
import numpy as np
import soundfile as sf
import torch
import torchaudio.transforms as T


def _decode_with_av(file_path: Union[str, Path], target_sample_rate: int = 16000) -> Tuple[torch.Tensor, int]:
    """
    Universal audio decoder using PyAV (FFmpeg).
    Decodes webm, opus, ogg, mp3, m4a, mp4, etc. directly into float32 16kHz mono tensor.
    """
    import av
    container = av.open(str(file_path))
    audio_stream = next((s for s in container.streams if s.type == "audio"), None)
    if not audio_stream:
        container.close()
        raise ValueError(f"No audio stream found in: {file_path}")

    resampler = av.AudioResampler(format="flt", layout="mono", rate=target_sample_rate)
    chunks = []
    for frame in container.decode(audio_stream):
        for rf in resampler.resample(frame):
            chunks.append(rf.to_ndarray())
    container.close()

    if not chunks:
        return torch.zeros(0, dtype=torch.float32), target_sample_rate

    audio_arr = np.concatenate(chunks, axis=-1).squeeze()
    waveform = torch.from_numpy(audio_arr).float()
    return waveform, target_sample_rate


def load_audio(
    file_path: Union[str, Path],
    target_sample_rate: int = 16000,
) -> Tuple[torch.Tensor, int]:
    """
    Loads any audio file into a float32 PyTorch tensor (mono, 16kHz).
    Tries soundfile first; falls back to PyAV if format is not recognized.
    """
    path_str = str(file_path)

    try:
        data, sr = sf.read(path_str, dtype="float32")
        # If multi-channel, average down to mono
        if data.ndim == 2:
            data = np.mean(data, axis=-1)

        waveform = torch.from_numpy(data)

        # Resample if needed
        if sr != target_sample_rate:
            resampler = T.Resample(orig_freq=sr, new_freq=target_sample_rate)
            waveform = resampler(waveform)
            sr = target_sample_rate

        return waveform, sr
    except Exception as sf_err:
        # Fallback to PyAV for WebM / Opus / M4A / browser blobs
        try:
            return _decode_with_av(path_str, target_sample_rate=target_sample_rate)
        except Exception as av_err:
            raise RuntimeError(
                f"Failed to decode audio with soundfile ({sf_err}) and PyAV ({av_err})"
            )


def save_audio(
    file_path: Union[str, Path],
    waveform: torch.Tensor,
    sample_rate: int = 16000,
) -> None:
    """
    Saves a float32 PyTorch tensor to audio file using soundfile.
    """
    if isinstance(waveform, torch.Tensor):
        data = waveform.detach().cpu().squeeze().numpy()
    else:
        data = np.asarray(waveform).squeeze()

    sf.write(str(file_path), data, samplerate=sample_rate)
