"""
CTC Decoding Module.
Provides fast Greedy Argmax Decoding with CTC blank collapsing and streaming state management.
"""

from typing import Dict, List, Tuple, Any, Union
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

    def decode_beam(self, logits, beam_width: int = 10) -> str:
        """Decode CTC log-probabilities with language-model-free beam search."""
        import torch

        log_probs = logits.detach().float().cpu() if isinstance(logits, torch.Tensor) else torch.as_tensor(logits, dtype=torch.float32)
        beams: Dict[Tuple[int, ...], Tuple[float, float]] = {(): (0.0, float("-inf"))}

        for frame in log_probs:
            next_beams: Dict[Tuple[int, ...], Tuple[float, float]] = {}
            top_ids = torch.topk(frame, k=min(beam_width, frame.numel())).indices.tolist()
            for prefix, (p_blank, p_nonblank) in beams.items():
                prefix_total = torch.logaddexp(torch.tensor(p_blank), torch.tensor(p_nonblank)).item()
                for token_id in top_ids:
                    token_score = frame[token_id].item()
                    if token_id == self.blank_id:
                        old_blank, old_nonblank = next_beams.get(prefix, (float("-inf"), float("-inf")))
                        next_beams[prefix] = (
                            torch.logaddexp(torch.tensor(old_blank), torch.tensor(prefix_total + token_score)).item(),
                            old_nonblank,
                        )
                        continue

                    extended_prefix = prefix + (token_id,)
                    if prefix and prefix[-1] == token_id:
                        old_blank, old_nonblank = next_beams.get(prefix, (float("-inf"), float("-inf")))
                        next_beams[prefix] = (
                            old_blank,
                            torch.logaddexp(
                                torch.tensor(old_nonblank),
                                torch.tensor(p_nonblank + token_score),
                            ).item(),
                        )
                        old_blank, old_nonblank = next_beams.get(extended_prefix, (float("-inf"), float("-inf")))
                        extend_score = p_blank + token_score
                    else:
                        old_blank, old_nonblank = next_beams.get(extended_prefix, (float("-inf"), float("-inf")))
                        extend_score = prefix_total + token_score
                    next_beams[extended_prefix] = (
                        old_blank,
                        torch.logaddexp(torch.tensor(old_nonblank), torch.tensor(extend_score)).item(),
                    )

            beams = dict(sorted(next_beams.items(), key=lambda item: max(item[1]), reverse=True)[:beam_width])

        best_prefix = max(
            beams,
            key=lambda prefix: torch.logaddexp(torch.tensor(beams[prefix][0]), torch.tensor(beams[prefix][1])).item(),
        )
        return self.tokenizer.decode(list(best_prefix))


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
