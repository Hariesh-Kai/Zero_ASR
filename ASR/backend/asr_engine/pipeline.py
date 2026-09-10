"""
Complete End-to-End ASR Pipeline.
Chains: AudioFrontend -> ConformerCTC Model -> CTCDecoder -> TextNormalizer.
"""

from pathlib import Path
from typing import Optional, Union, Dict, Any
import torch

from asr_engine.audio.frontend import AudioFrontend
from asr_engine.audio.vad import EnergyVAD
from asr_engine.model.ctc_model import ConformerCTC
from asr_engine.tokenizer.char_tokenizer import CharTokenizer
from asr_engine.decoding.ctc_decoder import CTCDecoder, StreamingCTCDecoder
from asr_engine.postprocess.normalizer import TextNormalizer
from asr_engine.tokenizer.romanizer import romanize_tamil, is_tamil_script


class ASRPipeline:
    """
    Unified speech recognition pipeline for English and Romanized Tamil.
    """

    def __init__(
        self,
        model: ConformerCTC,
        tokenizer: CharTokenizer,
        frontend: Optional[AudioFrontend] = None,
        normalizer: Optional[TextNormalizer] = None,
        vad: Optional[EnergyVAD] = None,
        device: Optional[torch.device] = None,
    ):
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.device = device
        self.model = model.to(device)
        self.model.eval()

        self.tokenizer = tokenizer
        self.frontend = (frontend or AudioFrontend()).to(device)
        self.decoder = CTCDecoder(tokenizer)
        self.normalizer = normalizer or TextNormalizer()
        self.vad = vad or EnergyVAD()

    @classmethod
    def load_from_dir(
        cls,
        model_dir: Union[str, Path],
        device: Optional[torch.device] = None,
    ) -> "ASRPipeline":
        """
        Loads trained pipeline assets (checkpoint + tokenizer) from directory.
        """
        model_dir = Path(model_dir)
        tokenizer_path = model_dir / "vocab.json"
        
        checkpoint_path = None
        for cand in ["best_model.pt", "latest_model.pt", "model.pt"]:
            if (model_dir / cand).exists():
                checkpoint_path = model_dir / cand
                break
        if checkpoint_path is None:
            raise FileNotFoundError(f"No valid checkpoint (.pt) found in {model_dir}")

        tokenizer = CharTokenizer.load(tokenizer_path)
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = ConformerCTC.load_from_checkpoint(checkpoint_path, device=device)
        return cls(model=model, tokenizer=tokenizer, device=device)

    def transcribe_waveform(
        self,
        waveform: torch.Tensor,
        mode: str = "transcription",
        apply_vad: bool = False,
        beam_width: int = 1,
    ) -> Dict[str, Any]:
        """
        Transcribes a 1D or 2D audio tensor sampled at 16kHz.
        waveform: shape (samples,) or (1, samples)
        mode: 'transcription' (verbatim) or 'clean' (disfluencies removed)
        """
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)

        # Optional VAD filtering to reject silence
        if apply_vad:
            samples_list = waveform.squeeze().cpu().tolist()
            speech_segments = self.vad.get_speech_segments(samples_list)
            if not speech_segments:
                return {
                    "raw_text": "",
                    "text": "",
                    "is_speech": False,
                }

        waveform = waveform.to(self.device)

        with torch.no_grad():
            # 1. Feature extraction
            mel_spec = self.frontend(waveform)  # (1, time, n_mels)

            # 2. Acoustic model forward pass
            log_probs, _ = self.model(mel_spec)  # (1, time // 4, vocab_size)

            # 3. CTC greedy decoding
            raw_text = (
                self.decoder.decode_beam(log_probs[0], beam_width=beam_width)
                if beam_width > 1
                else self.decoder.decode_logits(log_probs[0])
            )

            # 4. Handle Tamil script if model predicted any Unicode, or keep Romanized
            if is_tamil_script(raw_text):
                raw_text = romanize_tamil(raw_text)

            # 5. Text normalization and punctuation
            final_text = self.normalizer.process(raw_text, mode=mode)

        return {
            "raw_text": raw_text,
            "text": final_text,
            "is_speech": True,
        }
