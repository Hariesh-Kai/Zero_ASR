"""
End-to-End Conformer-CTC Speech Recognition Model.
Combines 4x 2D Subsampler, Causal Conformer Blocks, and Linear CTC projection head.
Supports non-autoregressive parallel training, dynamic padding, and chunk-by-chunk streaming inference.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path

from asr_engine.model.conformer import Conv2dSubsampler, ConformerBlock


class ConformerCTC(nn.Module):
    """
    Compact Streaming Conformer-CTC ASR Model.
    """

    def __init__(
        self,
        in_channels: int = 80,
        vocab_size: int = 32,
        d_model: int = 144,
        n_layers: int = 6,
        n_heads: int = 4,
        conv_kernel_size: int = 15,
        ffn_expansion: int = 4,
        dropout: float = 0.1,
        num_layers: Optional[int] = None,
    ):
        super().__init__()
        if num_layers is not None:
            n_layers = num_layers
        self.in_channels = in_channels
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.n_layers = n_layers
        self.n_heads = n_heads
        self.conv_kernel_size = conv_kernel_size
        self.ffn_expansion = ffn_expansion
        self.dropout = dropout

        # 1. 4x Subsampling Module (25ms window, 10ms hop -> 40ms frame resolution)
        self.subsampler = Conv2dSubsampler(in_channels=in_channels, out_channels=d_model)

        # 2. Conformer Encoder Layers
        self.layers = nn.ModuleList([
            ConformerBlock(
                d_model=d_model,
                n_heads=n_heads,
                conv_kernel_size=conv_kernel_size,
                ffn_expansion=ffn_expansion,
                dropout=dropout,
            )
            for _ in range(n_layers)
        ])

        # 3. Final CTC Projection Head
        self.head = nn.Linear(d_model, vocab_size)

        # 4. Standard CTC Loss (zero_infinity prevents gradient explosion on rare alignment glitches)
        self.ctc_loss = nn.CTCLoss(blank=0, zero_infinity=True, reduction="mean")

    @property
    def parameter_count(self) -> int:
        """Returns total number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def forward(
        self,
        x: torch.Tensor,
        input_lengths: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Forward pass for complete audio utterance or training batch.
        x: (batch, time, in_channels)
        input_lengths: (batch,) tensor of original frame counts before subsampling
        Returns:
          log_probs: (batch, time // 4, vocab_size)
          output_lengths: (batch,) post-subsampling frame counts
        """
        # Subsampling: (b, t, f) -> (b, t // 4, d_model)
        x = self.subsampler(x)

        if input_lengths is not None:
            out_lens = self.subsampler.get_out_lens(input_lengths)
            out_lens = torch.clamp(out_lens, min=1, max=x.size(1))
        else:
            out_lens = None

        # Pass through Conformer blocks
        for layer in self.layers:
            x, _ = layer(x, cache=None)

        # CTC projection
        logits = self.head(x)
        log_probs = F.log_softmax(logits, dim=-1)

        return log_probs, out_lens

    def forward_chunk(
        self,
        chunk_x: torch.Tensor,
        layer_caches: Optional[List[Any]] = None,
    ) -> Tuple[torch.Tensor, List[Any]]:
        """
        Forward pass for real-time streaming audio chunks.
        chunk_x: (batch, chunk_time, in_channels)
        layer_caches: List of layer state tuples from previous chunk
        """
        # Note: Subsampling 2D conv across chunks is simplest when chunk sizes are multiples of 4 frames (e.g. 16 frames = 160ms)
        x = self.subsampler(chunk_x)

        new_caches = []
        for i, layer in enumerate(self.layers):
            cache_i = layer_caches[i] if layer_caches is not None else None
            x, new_c = layer(x, cache=cache_i)
            new_caches.append(new_c)

        logits = self.head(x)
        log_probs = F.log_softmax(logits, dim=-1)
        return log_probs, new_caches

    def compute_loss(
        self,
        log_probs: torch.Tensor,
        targets: torch.Tensor,
        input_lengths: torch.Tensor,
        target_lengths: torch.Tensor,
    ) -> torch.Tensor:
        """
        Computes CTC Loss.
        PyTorch CTC expects log_probs shape: (time, batch, vocab_size)
        """
        # (batch, time, vocab) -> (time, batch, vocab)
        lp = log_probs.transpose(0, 1)
        loss = self.ctc_loss(lp, targets, input_lengths, target_lengths)
        return loss

    def save_checkpoint(
        self,
        path: Path,
        optimizer: Optional[torch.optim.Optimizer] = None,
        scheduler: Optional[Any] = None,
        epoch: int = 0,
        loss: float = 0.0,
        best_val_cer: Optional[float] = None,
    ) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint = {
            "epoch": epoch,
            "loss": loss,
            "state_dict": self.state_dict(),
            "config": {
                "in_channels": self.in_channels,
                "vocab_size": self.vocab_size,
                "d_model": self.d_model,
                "n_layers": self.n_layers,
                "n_heads": self.n_heads,
                "conv_kernel_size": self.conv_kernel_size,
                "ffn_expansion": self.ffn_expansion,
                "dropout": self.dropout,
            }
        }
        if optimizer is not None:
            checkpoint["optimizer"] = optimizer.state_dict()
        if scheduler is not None:
            checkpoint["scheduler"] = scheduler.state_dict()
        if best_val_cer is not None:
            checkpoint["best_val_cer"] = best_val_cer
        torch.save(checkpoint, path)

    @classmethod
    def load_from_checkpoint(cls, path: Path, device: torch.device = torch.device("cpu")) -> "ConformerCTC":
        checkpoint = torch.load(path, map_location=device)
        config = checkpoint.get("config", {})
        state_dict = checkpoint["state_dict"]

        # Infer kernel size dynamically from weights if omitted in older configs
        if "conv_kernel_size" not in config:
            for k, v in state_dict.items():
                if "conv.dw_conv.weight" in k:
                    config["conv_kernel_size"] = v.shape[-1]
                    break

        model = cls(**config)
        model.load_state_dict(state_dict)
        model.to(device)
        return model
