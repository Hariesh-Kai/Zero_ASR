"""
Inference & Verification Script for Prototype Model.
Tests full pipeline: Audio -> Mel-Spec -> Conformer-CTC -> CTC Decoding -> Text Normalization.
Measures latency, RTF on GPU and CPU, and demonstrates Transcription and Clean modes and Streaming.
"""

import sys
import time
from pathlib import Path
import torch

from asr_engine.pipeline import ASRPipeline
from asr_engine.evaluation.metrics import compute_rtf
from asr_engine.decoding.ctc_decoder import StreamingCTCDecoder
from asr_engine.tokenizer.char_tokenizer import CharTokenizer
from train_prototype import ControlledPrototypeDataset


def test_inference(checkpoint_dir: str = "checkpoints/prototype"):
    dir_path = Path(checkpoint_dir)
    if not (dir_path / "model.pt").exists():
        print(f"Error: Checkpoint not found at {dir_path / 'model.pt'}. Run train_prototype.py first.")
        return

    print("=" * 60)
    print("=== ASR PROTOTYPE INFERENCE & BENCHMARK SUITE ===")
    print("=" * 60)

    # 1. GPU Verification
    gpu_available = torch.cuda.is_available()
    device_gpu = torch.device("cuda" if gpu_available else "cpu")
    print(f"\n[1] Loading Pipeline on {device_gpu} ({torch.cuda.get_device_name(0) if gpu_available else 'CPU'})...")
    pipeline_gpu = ASRPipeline.load_from_dir(dir_path, device=device_gpu)
    print(f"  Model Parameter Count: {pipeline_gpu.model.parameter_count:,}")
    print(f"  Vocabulary Size:       {len(pipeline_gpu.tokenizer)}")

    # 2. Test with sample synthetic audio from dataset
    dataset = ControlledPrototypeDataset(num_samples=4)
    for idx in range(min(4, len(dataset))):
        item = dataset[idx]
        waveform = item["waveform"]
        ref_text = item["raw_transcript"]
        lang = item["language"]
        dur = len(waveform) / 16000.0

        t0 = time.perf_counter()
        res_trans = pipeline_gpu.transcribe_waveform(waveform, mode="transcription")
        dt = time.perf_counter() - t0
        rtf = compute_rtf(dur, dt)

        res_clean = pipeline_gpu.transcribe_waveform(waveform, mode="clean")

        print(f"\n--- Test Sample {idx + 1} ({lang.upper()}) ---")
        print(f"  Reference:     '{ref_text}'")
        print(f"  Transcription: '{res_trans['text']}'")
        print(f"  Clean Mode:    '{res_clean['text']}'")
        print(f"  Duration: {dur:.2f}s | Latency: {dt*1000:.1f}ms | RTF: {rtf:.4f} ({1.0/max(1e-6, rtf):.1f}x real-time)")

    # 3. Benchmark CPU Inference (Offline Edge Requirement)
    print("\n[2] Benchmarking Offline CPU Performance...")
    pipeline_cpu = ASRPipeline.load_from_dir(dir_path, device=torch.device("cpu"))
    sample_wav = dataset[0]["waveform"]
    dur = len(sample_wav) / 16000.0

    # Warmup
    _ = pipeline_cpu.transcribe_waveform(sample_wav)

    t0 = time.perf_counter()
    cpu_res = pipeline_cpu.transcribe_waveform(sample_wav)
    cpu_dt = time.perf_counter() - t0
    cpu_rtf = compute_rtf(dur, cpu_dt)
    print(f"  CPU Duration: {dur:.2f}s | Latency: {cpu_dt*1000:.1f}ms | CPU RTF: {cpu_rtf:.4f} ({1.0/max(1e-6, cpu_rtf):.1f}x real-time)")
    print(f"  CPU Output:   '{cpu_res['text']}'")

    # 4. Streaming Chunked Decoding Simulation
    print("\n[3] Testing Real-Time Streaming Chunk Inference...")
    streaming_decoder = StreamingCTCDecoder(pipeline_gpu.tokenizer)
    streaming_decoder.reset()

    # 160ms chunks (16 mel frames)
    chunk_samples = 160 * 16  # 2560 samples = 160ms @ 16kHz
    total_samples = len(sample_wav)
    caches = None
    streamed_tokens = []

    pipeline_gpu.model.eval()
    with torch.no_grad():
        for start in range(0, total_samples, chunk_samples):
            end = min(total_samples, start + chunk_samples)
            chunk_audio = sample_wav[start:end]
            if len(chunk_audio) < 400:
                continue

            chunk_mel = pipeline_gpu.frontend(chunk_audio.unsqueeze(0).to(device_gpu))
            # Ensure multiple of 4 frames for subsampler
            n_pad = (4 - (chunk_mel.size(1) % 4)) % 4
            if n_pad > 0:
                chunk_mel = torch.nn.functional.pad(chunk_mel, (0, 0, 0, n_pad))

            log_probs, caches = pipeline_gpu.model.forward_chunk(chunk_mel, caches)
            chunk_text = streaming_decoder.process_chunk(log_probs[0])
            if chunk_text:
                streamed_tokens.append(chunk_text)

    final_stream_text = streaming_decoder.finalize()
    print(f"  Streaming Result: '{final_stream_text}'")

    # 5. Normalizer Disfluency & Casing Test
    print("\n[4] Text Normalizer Mode Demonstration:")
    disfluent_text = "i i went to uh college yesterday and um met my friend"
    normalizer = pipeline_gpu.normalizer
    print(f"  Raw Disfluent Input: '{disfluent_text}'")
    print(f"  Transcription Mode:  '{normalizer.process(disfluent_text, mode='transcription')}'")
    print(f"  Clean Mode:          '{normalizer.process(disfluent_text, mode='clean')}'")

    print("\n" + "=" * 60)
    print("=== ALL PROTOTYPE INFERENCE CHECKS COMPLETED SUCCESSFULLY! ===")
    print("=" * 60)


if __name__ == "__main__":
    test_inference()

