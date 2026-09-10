"""
Audio Frontend Processing Module.
Standardizes incoming audio from arbitrary microphones into a clean, normalized acoustic representation:
- 16 kHz Mono conversion
- Loudness / RMS normalization (-20 dBFS)
- 80-channel Log-Mel Spectrogram extraction
- Cepstral Mean & Variance Normalization (CMVN)
"""

import math
import torch
import torch.nn as nn
import torchaudio.transforms as T


class AudioFrontend(nn.Module):
    """
    Standardized Audio Frontend for multi-microphone normalization.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        n_mels: int = 80,
        n_fft: int = 400,       # 25ms @ 16kHz
        hop_length: int = 160,  # 10ms @ 16kHz
        f_min: float = 80.0,    # Cut low-frequency rumble
        f_max: float = 7600.0,  # Avoid high-frequency Nyquist edge distortion
    ):
        super().__init__()
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.hop_length = hop_length

        self.mel_spectrogram = T.MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=n_fft,
            win_length=n_fft,
            hop_length=hop_length,
            f_min=f_min,
            f_max=f_max,
            n_mels=n_mels,
            power=2.0,
            normalized=False,
            center=True,
            pad_mode="reflect",
        )

    def normalize_loudness(
        self,
        waveform: torch.Tensor,
        lengths: torch.Tensor = None,
        target_rms: float = 0.1,
    ) -> torch.Tensor:
        """
        Normalizes waveform to target RMS amplitude to handle different microphone sensitivities.
        Supports:
        - 1D: (samples,) -> returns (1, samples)
        - 2D: (batch, samples) -> normalized per sample
        - 3D: (batch, channels, samples) -> converted to mono (batch, samples)
        """
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        elif waveform.ndim == 3:
            # (batch, channels, samples) -> average across channels to make mono
            waveform = waveform.mean(dim=1)

        # Waveform is now guaranteed to be 2D: (batch, samples)
        if lengths is None:
            rms = torch.sqrt(torch.mean(waveform ** 2, dim=-1, keepdim=True) + 1e-8)
        else:
            lengths = lengths.to(waveform.device).clamp(min=1, max=waveform.size(-1))
            sample_positions = torch.arange(waveform.size(-1), device=waveform.device).unsqueeze(0)
            valid = sample_positions < lengths.unsqueeze(1)
            valid_waveform = waveform * valid
            rms = torch.sqrt(
                valid_waveform.pow(2).sum(dim=-1, keepdim=True) / lengths.unsqueeze(1) + 1e-8
            )
        scale = torch.where(rms > 1e-4, target_rms / rms, torch.ones_like(rms))
        scale = torch.clamp(scale, min=0.1, max=10.0)
        waveform = waveform * scale

        # Clip to [-1.0, 1.0] to prevent digital distortion
        waveform = torch.clamp(waveform, -1.0, 1.0)
        return waveform

    def apply_cmvn(self, mel_spec: torch.Tensor, lengths: torch.Tensor = None) -> torch.Tensor:
        """
        Applies Cepstral Mean and Variance Normalization (CMVN) across time frames.
        Shape: (batch, n_mels, time)
        """
        if lengths is None:
            mean = mel_spec.mean(dim=-1, keepdim=True)
            std = mel_spec.std(dim=-1, keepdim=True) + 1e-5
            return (mel_spec - mean) / std

        lengths = lengths.to(mel_spec.device).clamp(min=1, max=mel_spec.size(-1))
        frame_positions = torch.arange(mel_spec.size(-1), device=mel_spec.device).unsqueeze(0)
        valid = frame_positions < lengths.unsqueeze(1)
        valid_float = valid.unsqueeze(1).to(mel_spec.dtype)
        counts = lengths.view(-1, 1, 1).to(mel_spec.dtype)
        mean = (mel_spec * valid_float).sum(dim=-1, keepdim=True) / counts
        variance = ((mel_spec - mean) * valid_float).pow(2).sum(dim=-1, keepdim=True) / counts
        normalized = (mel_spec - mean) / torch.sqrt(variance + 1e-5)
        return normalized * valid_float

    def forward(
        self,
        waveform: torch.Tensor,
        lengths: torch.Tensor = None,
        apply_norm: bool = True,
    ) -> torch.Tensor:
        """
        Transforms raw audio waveform into normalized Log-Mel spectrogram.
        Returns tensor of shape: (batch, time, n_mels)
        """
        if apply_norm:
            waveform = self.normalize_loudness(waveform, lengths=lengths)
        elif waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        elif waveform.ndim == 3:
            waveform = waveform.mean(dim=1)

        if lengths is not None:
            lengths = torch.div(lengths, self.hop_length, rounding_mode="floor") + 1

        # Extract Mel power spectrogram: shape (batch, n_mels, time)
        mel = self.mel_spectrogram(waveform)

        # Log compression: log(mel + 1e-5)
        log_mel = torch.log(torch.clamp(mel, min=1e-5))

        # CMVN across time dimension
        norm_mel = self.apply_cmvn(log_mel, lengths=lengths)

        # Reshape to (batch, time, n_mels) for acoustic encoder
        norm_mel = norm_mel.transpose(1, 2)
        return norm_mel

