"""
Causal Conformer Encoder Module.
Implements:
- 4x Conv2D Subsampling
- Causal Depthwise-Separable Convolution
- Causal Multi-Head Self-Attention (with optional KV cache for chunk streaming)
- Macaron-style Feed-Forward Network
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, List


class Conv2dSubsampler(nn.Module):
    """
    Subsamples input Log-Mel spectrogram by 4x along time dimension using 2D Convolutions.
    Input: (batch, time, n_mels)
    Output: (batch, time // 4, d_model)
    """

    def __init__(self, in_channels: int = 80, out_channels: int = 144):
        super().__init__()
        # First conv: stride 2
        self.conv1 = nn.Conv2d(1, out_channels // 2, kernel_size=3, stride=2, padding=1)
        self.act1 = nn.SiLU()
        # Second conv: stride 2
        self.conv2 = nn.Conv2d(out_channels // 2, out_channels, kernel_size=3, stride=2, padding=1)
        self.act2 = nn.SiLU()

        # Project flattened frequency dimension to d_model
        freq_after_sub = in_channels // 4
        self.proj = nn.Linear(out_channels * freq_after_sub, out_channels)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        x: (batch, time, n_mels)
        """
        # (batch, time, n_mels) -> (batch, 1, time, n_mels)
        x = x.unsqueeze(1)
        x = self.act1(self.conv1(x))
        x = self.act2(self.conv2(x))

        # Shape: (batch, out_channels, time // 4, n_mels // 4)
        b, c, t, f = x.shape
        x = x.permute(0, 2, 1, 3).contiguous().view(b, t, c * f)
        x = self.proj(x)
        return x

    def get_out_lens(self, in_lens: torch.Tensor) -> torch.Tensor:
        """Computes exact time frame length after two stride-2 convolutions."""
        l1 = torch.div(in_lens - 1, 2, rounding_mode="floor") + 1
        l2 = torch.div(l1 - 1, 2, rounding_mode="floor") + 1
        return l2


class FeedForwardModule(nn.Module):
    """
    Macaron-style Feed-Forward Module with SiLU activation.
    """

    def __init__(self, d_model: int = 144, expansion_factor: int = 4, dropout: float = 0.1):
        super().__init__()
        d_ffn = d_model * expansion_factor
        self.ln = nn.LayerNorm(d_model)
        self.fc1 = nn.Linear(d_model, d_ffn)
        self.act = nn.SiLU()
        self.dropout1 = nn.Dropout(dropout)
        self.fc2 = nn.Linear(d_ffn, d_model)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        x = self.ln(x)
        x = self.fc1(x)
        x = self.act(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.dropout2(x)
        return residual + 0.5 * x


class CausalMultiHeadAttention(nn.Module):
    """
    Causal Multi-Head Self-Attention.
    Only attends to current and past positions for zero-latency streaming.
    Supports past Key/Value caching for chunked streaming inference.
    """

    def __init__(self, d_model: int = 144, n_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        assert self.head_dim * n_heads == d_model, "d_model must be divisible by n_heads"

        self.ln = nn.LayerNorm(d_model)
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        x: torch.Tensor,
        cache: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        x: (batch, time, d_model)
        cache: Optional tuple of (past_k, past_v)
        """
        residual = x
        x = self.ln(x)
        b, t, d = x.shape

        q = self.q_proj(x).view(b, t, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(b, t, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(b, t, self.n_heads, self.head_dim).transpose(1, 2)

        if cache is not None:
            past_k, past_v = cache
            k = torch.cat([past_k, k], dim=2)
            v = torch.cat([past_v, v], dim=2)
            new_cache = (k, v)
        else:
            new_cache = (k, v)

        k_len = k.shape[2]
        # Causal attention mask: queries at position i can only attend to keys <= (offset + i)
        q_len = t
        offset = k_len - q_len

        # Score computation: (b, n_heads, q_len, k_len)
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)

        # Apply causal mask
        # rows: 0 to q_len-1, cols: 0 to k_len-1
        # allowed if col <= offset + row
        q_pos = torch.arange(q_len, device=x.device).unsqueeze(1)
        k_pos = torch.arange(k_len, device=x.device).unsqueeze(0)
        causal_mask = k_pos > (q_pos + offset)
        scores = scores.masked_fill(causal_mask.unsqueeze(0).unsqueeze(0), float("-inf"))

        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)

        # Output context: (b, n_heads, q_len, head_dim) -> (b, q_len, d_model)
        context = torch.matmul(attn, v)
        context = context.transpose(1, 2).contiguous().view(b, q_len, d)
        out = self.out_proj(context)
        out = self.dropout(out)

        return residual + out, new_cache


class CausalConvModule(nn.Module):
    """
    Causal Depthwise-Separable 1D Convolution Module.
    Uses asymmetric left-padding so future context is strictly unseen.
    """

    def __init__(self, d_model: int = 144, kernel_size: int = 15, dropout: float = 0.1):
        super().__init__()
        self.kernel_size = kernel_size
        self.ln = nn.LayerNorm(d_model)

        # Pointwise Conv1: expansion factor 2 with Gated Linear Unit (GLU)
        self.pw_conv1 = nn.Conv1d(d_model, 2 * d_model, kernel_size=1)

        # 1D Depthwise Causal Conv
        self.dw_conv = nn.Conv1d(
            d_model,
            d_model,
            kernel_size=kernel_size,
            groups=d_model,
            padding=0,  # Manual causal padding handled in forward
        )
        self.bn = nn.GroupNorm(1, d_model)  # GroupNorm is stable across arbitrary batch/chunk sizes
        self.act = nn.SiLU()

        # Pointwise Conv2
        self.pw_conv2 = nn.Conv1d(d_model, d_model, kernel_size=1)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        x: torch.Tensor,
        conv_cache: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        x: (batch, time, d_model)
        conv_cache: (batch, d_model, kernel_size - 1)
        """
        residual = x
        x = self.ln(x)

        # (batch, time, d_model) -> (batch, d_model, time)
        x = x.transpose(1, 2)

        # Pointwise 1 + GLU
        x = self.pw_conv1(x)
        x = F.glu(x, dim=1)

        # Causal padding
        pad_len = self.kernel_size - 1
        if conv_cache is not None:
            x_padded = torch.cat([conv_cache, x], dim=-1)
        else:
            x_padded = F.pad(x, (pad_len, 0))

        # Next conv cache is the trailing pad_len frames
        new_conv_cache = x_padded[:, :, -pad_len:]

        # Depthwise Conv
        x = self.dw_conv(x_padded)
        x = self.bn(x)
        x = self.act(x)

        # Pointwise 2
        x = self.pw_conv2(x)
        x = self.dropout(x)

        # Transpose back: (batch, d_model, time) -> (batch, time, d_model)
        out = x.transpose(1, 2)
        return residual + out, new_conv_cache


class ConformerBlock(nn.Module):
    """
    A single Causal Conformer Block with Macaron-style FFNs, Causal Attention, and Causal Conv.
    """

    def __init__(
        self,
        d_model: int = 144,
        n_heads: int = 4,
        conv_kernel_size: int = 15,
        ffn_expansion: int = 4,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.ffn1 = FeedForwardModule(d_model, ffn_expansion, dropout)
        self.attn = CausalMultiHeadAttention(d_model, n_heads, dropout)
        self.conv = CausalConvModule(d_model, conv_kernel_size, dropout)
        self.ffn2 = FeedForwardModule(d_model, ffn_expansion, dropout)
        self.final_ln = nn.LayerNorm(d_model)

    def forward(
        self,
        x: torch.Tensor,
        cache: Optional[Tuple[Tuple[torch.Tensor, torch.Tensor], torch.Tensor]] = None,
    ) -> Tuple[torch.Tensor, Tuple[Tuple[torch.Tensor, torch.Tensor], torch.Tensor]]:
        attn_cache = cache[0] if cache is not None else None
        conv_cache = cache[1] if cache is not None else None

        x = self.ffn1(x)
        x, new_attn_cache = self.attn(x, cache=attn_cache)
        x, new_conv_cache = self.conv(x, conv_cache=conv_cache)
        x = self.ffn2(x)
        x = self.final_ln(x)

        return x, (new_attn_cache, new_conv_cache)
