"""
CTC Decoding Module.
Provides fast Greedy Argmax Decoding with CTC blank collapsing and streaming state management.
"""

from typing import List, Tuple, Any, Union
from asr_engine.tokenizer.char_tokenizer import CharTokenizer


class CTCDecoder:
    """
    Greedy CTC Decoder for non-autoregressive acoustic frames.
    """

    def __init__(self, tokenizer: CharTokenizer):
        self.tokenizer = tokenizer
        self.blank_id = tokenizer.blank_id

    def decode_greedy_ids(self, frame_ids: List[int]) -> List[int]:
        """
        Collapses consecutive duplicate tokens and eliminates CTC blanks.
        Example: [0, 5, 5, 0, 5, 2, 2, 0] -> [5, 5, 2]
        """
        collapsed: List[int] = []
        prev = -1
        for tid in frame_ids:
            if tid != prev:
                if tid != self.blank_id:
                    collapsed.append(tid)
                prev = tid
        return collapsed

    def decode_tokens(self, frame_ids: List[int]) -> str:
        """
        Takes raw frame-level argmax IDs and produces decoded string.
        """
        clean_ids = self.decode_greedy_ids(frame_ids)
        return self.tokenizer.decode(clean_ids)

    def decode_logits(self, logits) -> str:
        """
        Convenience method taking a 2D tensor or numpy array of shape (T, Vocab)
        and returning the decoded string.
        """
        # Can accept torch.Tensor, numpy array, or nested list
        try:
            import torch
            if isinstance(logits, torch.Tensor):
                frame_ids = torch.argmax(logits, dim=-1).cpu().tolist()
                return self.decode_tokens(frame_ids)
        except ImportError:
            pass

        try:
            import numpy as np
            if isinstance(logits, np.ndarray):
                frame_ids = np.argmax(logits, axis=-1).tolist()
                return self.decode_tokens(frame_ids)
        except ImportError:
            pass

        # Fallback list of lists
        frame_ids = [max(range(len(row)), key=lambda i: row[i]) for row in logits]
        return self.decode_tokens(frame_ids)


class StreamingCTCDecoder:
    """
    Stateful streaming CTC decoder that maintains boundary context across audio chunks.
    """

    def __init__(self, tokenizer: CharTokenizer):
        self.decoder = CTCDecoder(tokenizer)
        self.reset()

    def reset(self):
        """Reset internal streaming state."""
        self.last_token_id = -1
        self.committed_tokens: List[int] = []

    def process_chunk(self, chunk_logits: Any) -> str:
        """
        Process a chunk of logits/log_probs (time, vocab) and return the updated partial transcript.
        """
        try:
            import torch
            if isinstance(chunk_logits, torch.Tensor):
                frame_ids = torch.argmax(chunk_logits, dim=-1).cpu().tolist()
                return self.update(frame_ids)
        except ImportError:
            pass

        try:
            import numpy as np
            if isinstance(chunk_logits, np.ndarray):
                frame_ids = np.argmax(chunk_logits, axis=-1).tolist()
                return self.update(frame_ids)
        except ImportError:
            pass

        if isinstance(chunk_logits, list):
            if chunk_logits and isinstance(chunk_logits[0], list):
                frame_ids = [max(range(len(row)), key=lambda i: row[i]) for row in chunk_logits]
            else:
                frame_ids = chunk_logits
            return self.update(frame_ids)

        raise TypeError(f"Unsupported chunk_logits type: {type(chunk_logits)}")

    def update(self, chunk_frame_ids: List[int]) -> str:
        """
        Process a new chunk of frame predictions and return current partial transcript.
        """
        for tid in chunk_frame_ids:
            if tid != self.last_token_id:
                if tid != self.decoder.blank_id:
                    self.committed_tokens.append(tid)
                self.last_token_id = tid

        return self.decoder.tokenizer.decode(self.committed_tokens)

    def finalize(self) -> str:
        """
        Finalize decoding for the utterance and return complete transcript.
        """
        text = self.decoder.tokenizer.decode(self.committed_tokens)
        self.reset()
        return text
