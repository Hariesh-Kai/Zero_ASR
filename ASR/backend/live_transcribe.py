"""
Interactive Audio & Microphone Transcription CLI.
Transcribes spoken English and spoken Tamil:
- Supports Transcription Mode (verbatim) vs Clean Mode (stutters/fillers removed)
- Emits Romanized Latin Tamil, preserving original spoken Tamil without translating into English.
- Real-time RTF and latency measurement.
- Supports streaming chunk simulation.
"""

import sys
import time
import argparse
from pathlib import Path

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import torch
import torchaudio

from asr_engine.pipeline import ASRPipeline
from asr_engine.evaluation.metrics import compute_rtf
from asr_engine.decoding.ctc_decoder import StreamingCTCDecoder


def transcribe_file(
    audio_path: str,
    checkpoint_dir: str = "checkpoints/prototype",
    mode: str = "transcription",
    device_name: str = "auto",
    streaming: bool = False,
):
    path = Path(audio_path)
    if not path.exists():
        print(f"Error: File not found: {path}")
        return

    if device_name == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device_name)

    print(f"Loading ASR Pipeline from [{checkpoint_dir}] onto {device}...")
    pipeline = ASRPipeline.load_from_dir(checkpoint_dir, device=device)
    print(f"Model: {pipeline.model.parameter_count:,} parameters.")

    print(f"\nLoading audio: {path.name}...")
    from asr_engine.audio.io import load_audio
    waveform, sr = load_audio(path, target_sample_rate=16000)
    duration = len(waveform) / 16000.0

    print("=" * 60)
    print(f"Audio Duration: {duration:.2f} seconds")
    print(f"Post-processing Mode: [{mode.upper()}]")
    print("=" * 60)

    if not streaming:
        t0 = time.perf_counter()
        result = pipeline.transcribe_waveform(waveform, mode=mode, apply_vad=True)
        latency = time.perf_counter() - t0
        rtf = compute_rtf(duration, latency)

        print("\n--- Transcription Result ---")
        print(f"Output:   {result['text']}")
        print(f"Raw CTC:  {result['raw_text']}")
        print(f"Latency:  {latency * 1000:.1f} ms | RTF: {rtf:.4f} ({1.0/max(1e-6, rtf):.1f}x real-time)")
    else:
        print("\n--- Streaming Real-Time Simulation (160ms chunks) ---")
        streaming_decoder = StreamingCTCDecoder(pipeline.tokenizer)
        chunk_samples = 160 * 16  # 2560 samples = 160ms @ 16kHz
        total_samples = len(waveform)
        caches = None

        t0 = time.perf_counter()
        for start in range(0, total_samples, chunk_samples):
            end = min(total_samples, start + chunk_samples)
            chunk_audio = waveform[start:end]
            if len(chunk_audio) < 400:
                continue

            chunk_mel = pipeline.frontend(chunk_audio.unsqueeze(0).to(device))
            n_pad = (4 - (chunk_mel.size(1) % 4)) % 4
            if n_pad > 0:
                chunk_mel = torch.nn.functional.pad(chunk_mel, (0, 0, 0, n_pad))

            log_probs, caches = pipeline.model.forward_chunk(chunk_mel, caches)
            partial = streaming_decoder.process_chunk(log_probs[0])
            if partial:
                sys.stdout.write(f"\rPartial: {partial}   ")
                sys.stdout.flush()

        raw_final = streaming_decoder.finalize()
        latency = time.perf_counter() - t0
        final_processed = pipeline.normalizer.process(raw_final, mode=mode)
        print(f"\nFinal Transcript: {final_processed}")
        print(f"Total Streaming Processing Time: {latency * 1000:.1f} ms")


def record_and_transcribe(
    duration_seconds: float = 4.0,
    checkpoint_dir: str = "checkpoints/prototype",
    mode: str = "transcription",
):
    """
    Records live audio from the default microphone and transcribes it immediately.
    """
    try:
        import sounddevice as sd
    except ImportError:
        print("\nNote: 'sounddevice' is required for live microphone recording.")
        print("To enable live microphone input, run: pip install sounddevice")
        return

    sample_rate = 16000
    print(f"\n🎤 Recording for {duration_seconds:.1f} seconds... Speak now into your microphone!")
    audio_data = sd.rec(int(duration_seconds * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()
    print("Recording finished. Processing speech...")

    waveform = torch.from_numpy(audio_data.squeeze())
    temp_wav = Path("temp_record.wav")
    from asr_engine.audio.io import save_audio
    save_audio(temp_wav, waveform, sample_rate=sample_rate)
    transcribe_file(str(temp_wav), checkpoint_dir=checkpoint_dir, mode=mode)
    if temp_wav.exists():
        temp_wav.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASR Transcription CLI")
    parser.add_argument("--file", help="Path to audio file (.wav, .flac, .mp3)")
    parser.add_argument("--record", action="store_true", help="Record from microphone")
    parser.add_argument("--record_seconds", type=float, default=4.0, help="Microphone recording duration")
    parser.add_argument("--checkpoint", default="checkpoints/prototype", help="Path to checkpoint directory")
    parser.add_argument("--mode", choices=["transcription", "clean"], default="transcription", help="Post-processing mode")
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--streaming", action="store_true", help="Simulate streaming chunked inference")

    args = parser.parse_args()

    if args.record:
        record_and_transcribe(duration_seconds=args.record_seconds, checkpoint_dir=args.checkpoint, mode=args.mode)
    elif args.file:
        transcribe_file(
            audio_path=args.file,
            checkpoint_dir=args.checkpoint,
            mode=args.mode,
            device_name=args.device,
            streaming=args.streaming,
        )
    else:
        print("Please provide --file <path_to_audio> or --record to transcribe speech.")
        parser.print_help()
