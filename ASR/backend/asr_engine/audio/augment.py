"""
Data Augmentation Module for ASR.
Implements:
- SpecAugment: Frequency Masking and Time Masking on Mel-Spectrograms
- Additive Noise Injection at randomized SNR levels
- Volume Perturbation and Clipping Simulation
"""

import math
import random
import torch
import torch.nn as nn
from typing import Optional, List


class SpecAugment(nn.Module):
    """
    SpecAugment (Park et al., 2019):
    Applies frequency and time masking directly to Log-Mel spectrograms.
    Input shape: (batch, time, freq)
    """

    def __init__(
        self,
        freq_mask_param: int = 15,
        time_mask_param: int = 35,
        n_freq_masks: int = 2,
        n_time_masks: int = 2,
        mask_value: float = 0.0,
        num_freq_masks: Optional[int] = None,
        num_time_masks: Optional[int] = None,
    ):
        super().__init__()
        if num_freq_masks is not None:
            n_freq_masks = num_freq_masks
        if num_time_masks is not None:
            n_time_masks = num_time_masks
        self.freq_mask_param = freq_mask_param
        self.time_mask_param = time_mask_param
        self.n_freq_masks = n_freq_masks
        self.n_time_masks = n_time_masks
        self.mask_value = mask_value

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (batch, time, freq)
        """
        if not self.training:
            return x

        batch, time_steps, n_freq = x.shape
        x_aug = x.clone()

        for b in range(batch):
            # Frequency masking
            for _ in range(self.n_freq_masks):
                f = random.randint(0, min(self.freq_mask_param, n_freq - 1))
                f0 = random.randint(0, n_freq - f)
                x_aug[b, :, f0 : f0 + f] = self.mask_value

            # Time masking
            for _ in range(self.n_time_masks):
                t = random.randint(0, min(self.time_mask_param, time_steps - 1))
                t0 = random.randint(0, time_steps - t)
                x_aug[b, t0 : t0 + t, :] = self.mask_value

        return x_aug


class AudioNoiseAugmentor:
    """
    Raw waveform noise augmentor.
    Injects synthetic white/pink/brown noise or recorded ambient noise at random SNR.
    """

    def __init__(self, min_snr_db: float = 5.0, max_snr_db: float = 25.0):
        self.min_snr_db = min_snr_db
        self.max_snr_db = max_snr_db

    def generate_synthetic_noise(self, length: int, noise_type: str = "pink") -> torch.Tensor:
        """Generates synthetic noise matching target length."""
        white = torch.randn(length)
        if noise_type == "white":
            return white
        # Simple IIR 1-pole filter for pink/fan-like noise approximation
        pink = torch.zeros(length)
        b0, b1 = 0.049922035, -0.095993537
        for i in range(1, length):
            pink[i] = 0.95 * pink[i - 1] + 0.05 * white[i]
        return pink

    def add_noise(
        self,
        clean_waveform: torch.Tensor,
        noise_waveform: Optional[torch.Tensor] = None,
        snr_db: Optional[float] = None,
    ) -> torch.Tensor:
        """
        Adds noise to clean waveform at target SNR (in dB).
        clean_waveform shape: (samples,) or (1, samples)
        """
        if snr_db is None:
            snr_db = random.uniform(self.min_snr_db, self.max_snr_db)

        clean_flat = clean_waveform.squeeze()
        length = clean_flat.shape[0]

        if noise_waveform is None:
            noise = self.generate_synthetic_noise(length, noise_type="pink").to(clean_waveform.device)
        else:
            noise = noise_waveform.squeeze().to(clean_waveform.device)
            # Repeat or slice noise to match audio length
            if noise.shape[0] < length:
                repeats = math.ceil(length / noise.shape[0])
                noise = noise.repeat(repeats)[:length]
            else:
                noise = noise[:length]

        # Calculate RMS powers
        clean_power = torch.mean(clean_flat ** 2) + 1e-8
        noise_power = torch.mean(noise ** 2) + 1e-8

        # Target noise power for desired SNR
        target_noise_power = clean_power / (10.0 ** (snr_db / 10.0))
        scale = torch.sqrt(target_noise_power / noise_power)

        noisy = clean_flat + scale * noise
        # Normalize/clamp to [-1.0, 1.0]
        max_val = torch.max(torch.abs(noisy))
        if max_val > 1.0:
            noisy = noisy / max_val

        return noisy.view_as(clean_waveform)
