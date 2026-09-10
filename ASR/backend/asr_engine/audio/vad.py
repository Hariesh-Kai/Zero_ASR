"""
Voice Activity Detection (VAD) Module.
Lightweight frame-based energy and zero-crossing detector with adaptive noise floor tracking
and hangover smoothing for real-time speech boundary detection.
"""

import math
from typing import List, Tuple


class EnergyVAD:
    """
    Lightweight, dependency-free Voice Activity Detector.
    Uses Short-Time Energy (STE) and Zero-Crossing Rate (ZCR) with an adaptive background noise floor.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        frame_ms: int = 20,
        energy_threshold_multiplier: float = 2.5,
        min_speech_duration_ms: int = 100,
        min_silence_duration_ms: int = 300,
    ):
        self.sample_rate = sample_rate
        self.frame_size = int(sample_rate * (frame_ms / 1000.0))
        self.energy_multiplier = energy_threshold_multiplier
        self.min_speech_frames = int(min_speech_duration_ms / frame_ms)
        self.min_silence_frames = int(min_silence_duration_ms / frame_ms)

        # Adaptive noise floor state
        self.noise_floor = 1e-5
        self.alpha = 0.95  # Noise tracking adaptation rate

    def compute_frame_energy(self, frame: List[float]) -> float:
        """Computes Root Mean Square (RMS) energy of an audio frame."""
        if not frame:
            return 0.0
        sum_sq = sum(x * x for x in frame)
        return math.sqrt(sum_sq / len(frame))

    def compute_zcr(self, frame: List[float]) -> float:
        """Computes normalized Zero Crossing Rate of an audio frame."""
        if len(frame) < 2:
            return 0.0
        crossings = sum(1 for i in range(1, len(frame)) if (frame[i] >= 0) != (frame[i - 1] >= 0))
        return crossings / (len(frame) - 1)

    def is_speech_chunk(self, chunk: List[float]) -> bool:
        """
        Determines if a single chunk of audio contains speech.
        Updates running noise floor when silence is observed.
        """
        energy = self.compute_frame_energy(chunk)
        threshold = max(self.noise_floor * self.energy_multiplier, 1e-4)

        if energy > threshold:
            return True
        else:
            # Adaptively track silence background noise
            self.noise_floor = self.alpha * self.noise_floor + (1.0 - self.alpha) * energy
            return False

    def get_speech_segments(
        self, samples: List[float]
    ) -> List[Tuple[int, int]]:
        """
        Splits a continuous 1D audio waveform into speech segment intervals (start_sample, end_sample).
        Applies hangover smoothing to avoid cutting off word tails.
        """
        num_frames = len(samples) // self.frame_size
        if num_frames == 0:
            return []

        frame_decisions = []
        for i in range(num_frames):
            frame = samples[i * self.frame_size : (i + 1) * self.frame_size]
            frame_decisions.append(self.is_speech_chunk(frame))

        # Apply hangover and smoothing
        speech_segments: List[Tuple[int, int]] = []
        in_speech = False
        speech_start = 0
        silence_count = 0

        for i, is_speech in enumerate(frame_decisions):
            if is_speech:
                if not in_speech:
                    in_speech = True
                    speech_start = max(0, (i - 1) * self.frame_size)
                silence_count = 0
            else:
                if in_speech:
                    silence_count += 1
                    if silence_count >= self.min_silence_frames:
                        in_speech = False
                        speech_end = min(len(samples), (i + 1) * self.frame_size)
                        # Ensure segment is longer than minimum speech duration
                        if (speech_end - speech_start) >= (self.min_speech_frames * self.frame_size):
                            speech_segments.append((speech_start, speech_end))

        # Handle final trailing segment if audio ended during speech
        if in_speech:
            speech_segments.append((speech_start, len(samples)))

        return speech_segments
