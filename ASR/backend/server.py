"""
FastAPI Server for ASR Engine.
Exposes REST and streaming endpoints to serve the Conformer-CTC speech recognition model to the React frontend.
Features:
- Dedicated K: drive temp folder (K:\\ASR\\temp)
- Auto-delete option with manual cleanup endpoints
- Universal audio decoding (soundfile + PyAV fallback for WebM/Opus/MP3/FLAC)
"""

import os
import sys
import time
import uuid
import shutil
from pathlib import Path
from typing import Optional, List

# Ensure backend root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import torch
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from asr_engine.pipeline import ASRPipeline
from asr_engine.audio.io import load_audio
from asr_engine.evaluation.metrics import compute_rtf
from asr_engine.tokenizer.romanizer import romanize_tamil, is_tamil_script

# Configured Temp directory on K: drive
TEMP_DIR = Path("K:/ASR/temp").resolve()
TEMP_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Lightweight ASR API",
    description="Offline Speech-to-Text API for English & Romanized Tamil",
    version="1.1.0",
)

# Enable CORS for React frontend (Vite default is http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline instance
pipeline: Optional[ASRPipeline] = None
device: Optional[torch.device] = None
checkpoint_path: Optional[Path] = None


@app.on_event("startup")
def startup_event():
    global pipeline, device, checkpoint_path

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    base_dir = Path(__file__).resolve().parent / "checkpoints"
    compact_dir = base_dir / "compact_conformer"
    if (compact_dir / "best_model.pt").exists() or (compact_dir / "latest_model.pt").exists() or (compact_dir / "model.pt").exists():
        ckpt_dir = compact_dir
    else:
        ckpt_dir = base_dir / "prototype"

    print(f"Loading ASR Pipeline from [{ckpt_dir}] on {device}...")
    pipeline = ASRPipeline.load_from_dir(ckpt_dir, device=device)
    checkpoint_path = ckpt_dir
    print(f"ASR Pipeline ready! Model parameters: {pipeline.model.parameter_count:,}")
    print(f"Temp directory configured at: {TEMP_DIR}")


@app.get("/api/info")
def get_info():
    """Returns model architecture and runtime hardware specs."""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model pipeline not initialized yet")

    is_cuda = device.type == "cuda"
    device_name = torch.cuda.get_device_name(0) if is_cuda else "CPU"

    # Count files in temp directory
    temp_files_count = len(list(TEMP_DIR.glob("*.*")))

    return {
        "status": "online",
        "device": device.type,
        "device_name": device_name,
        "parameters": pipeline.model.parameter_count,
        "vocab_size": len(pipeline.tokenizer),
        "supported_languages": ["English", "Tamil (Romanized Latin)"],
        "checkpoint": str(checkpoint_path.name if checkpoint_path else "unknown"),
        "temp_directory": str(TEMP_DIR),
        "temp_files_count": temp_files_count,
    }


@app.post("/api/reload")
def reload_pipeline():
    """Hot-reloads the latest model checkpoint into memory."""
    global pipeline, device, checkpoint_path
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    base_dir = Path(__file__).resolve().parent / "checkpoints"
    compact_dir = base_dir / "compact_conformer"
    if (compact_dir / "best_model.pt").exists() or (compact_dir / "latest_model.pt").exists() or (compact_dir / "model.pt").exists():
        ckpt_dir = compact_dir
    else:
        ckpt_dir = base_dir / "prototype"

    print(f"Reloading ASR Pipeline from [{ckpt_dir}] on {device}...")
    pipeline = ASRPipeline.load_from_dir(ckpt_dir, device=device)
    checkpoint_path = ckpt_dir
    return {
        "status": "reloaded",
        "checkpoint": str(ckpt_dir.name),
        "parameters": pipeline.model.parameter_count,
        "device": device.type,
    }


def _detect_audio_suffix(header_bytes: bytes, original_suffix: str) -> str:
    """Detects actual audio container format from magic bytes."""
    if header_bytes.startswith(b"\x1aE\xdf\xa3"):
        return ".webm"
    elif header_bytes.startswith(b"RIFF") and b"WAVE" in header_bytes[:16]:
        return ".wav"
    elif header_bytes.startswith(b"fLaC"):
        return ".flac"
    elif header_bytes.startswith(b"OggS"):
        return ".ogg"
    elif header_bytes.startswith(b"ID3") or header_bytes[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
        return ".mp3"
    return original_suffix if original_suffix else ".wav"


@app.post("/api/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    mode: str = Form("transcription"),        # "transcription" or "clean"
    auto_delete: bool = Form(True),           # Auto-delete temp audio file
):
    """
    Transcribes an uploaded audio file (.wav, .flac, .webm, .mp3, .ogg).
    Saves temporary file into K:\\ASR\\temp.
    If auto_delete=True, removes the temp file immediately after recognition.
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="ASR pipeline not loaded")

    # Read uploaded content
    content = await file.read()
    orig_suffix = Path(file.filename or "audio").suffix.lower()
    suffix = _detect_audio_suffix(content[:32], orig_suffix)

    # Generate unique filename in K:\ASR\temp
    unique_id = f"audio_{int(time.time())}_{uuid.uuid4().hex[:6]}{suffix}"
    tmp_path = TEMP_DIR / unique_id

    # Write content to K:\ASR\temp
    with open(tmp_path, "wb") as f:
        f.write(content)

    try:
        # Load and standardize audio to 16kHz mono tensor (soundfile + PyAV fallback)
        waveform, sr = load_audio(tmp_path, target_sample_rate=16000)
        duration_sec = len(waveform) / 16000.0

        t0 = time.perf_counter()
        result = pipeline.transcribe_waveform(waveform, mode=mode, apply_vad=False)
        latency_sec = time.perf_counter() - t0
        rtf = compute_rtf(duration_sec, latency_sec)

        # Detect primary language tag
        raw = result["raw_text"]
        is_tamil = any(word in raw for word in ["naan", "innaikku", "veettukku", "poren", "enakku", "adhu", "theriyadhu", "vanakkam", "nanba"])
        detected_lang = "Tamil (Romanized)" if is_tamil else "English"

        response_data = {
            "text": result["text"],
            "raw_text": result["raw_text"],
            "language": detected_lang,
            "mode": mode,
            "duration_sec": round(duration_sec, 3),
            "latency_ms": round(latency_sec * 1000, 1),
            "rtf": round(rtf, 4),
            "speedup": round(1.0 / max(1e-6, rtf), 1),
            "temp_file": str(tmp_path) if not auto_delete else None,
            "auto_deleted": auto_delete,
        }
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
    finally:
        if auto_delete and tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


@app.get("/api/temp")
def list_temp_files():
    """Lists all files currently stored in K:\\ASR\\temp."""
    files = []
    total_bytes = 0
    for p in sorted(TEMP_DIR.glob("*.*"), key=lambda x: x.stat().st_mtime, reverse=True):
        st = p.stat()
        total_bytes += st.st_size
        files.append({
            "name": p.name,
            "size_bytes": st.st_size,
            "size_kb": round(st.st_size / 1024, 1),
            "created_time": st.st_mtime,
            "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)),
            "path": str(p),
        })

    return {
        "directory": str(TEMP_DIR),
        "file_count": len(files),
        "total_files": len(files),
        "total_size_bytes": total_bytes,
        "total_size_mb": round(total_bytes / (1024 * 1024), 2),
        "files": files,
    }


@app.post("/api/clear_temp")
def clear_temp_folder():
    """Deletes all files in K:\\ASR\\temp."""
    deleted_count = 0
    for p in TEMP_DIR.glob("*.*"):
        try:
            p.unlink()
            deleted_count += 1
        except OSError:
            pass

    return {
        "message": f"Successfully cleared {deleted_count} files from {TEMP_DIR}",
        "deleted_count": deleted_count,
        "temp_directory": str(TEMP_DIR),
    }


@app.delete("/api/temp/{filename}")
def delete_single_temp_file(filename: str):
    """Deletes a specific file in K:\\ASR\\temp."""
    target = TEMP_DIR / filename
    if target.exists() and target.is_file():
        target.unlink()
        return {"deleted": filename}
    raise HTTPException(status_code=404, detail="File not found in temp directory")


class RomanizeRequest(BaseModel):
    text: str


@app.post("/api/romanize")
def preview_romanize(req: RomanizeRequest):
    """Utility endpoint to test phonetic Tamil transliteration directly."""
    romanized = romanize_tamil(req.text)
    return {
        "input": req.text,
        "is_tamil_unicode": is_tamil_script(req.text),
        "romanized": romanized,
    }


@app.get("/api/training/status")
def get_training_status():
    """Returns latest checkpoint info to check training progress."""
    base_dir = Path(__file__).resolve().parent / "checkpoints" / "compact_conformer"
    best = base_dir / "best_model.pt"
    latest = base_dir / "latest_model.pt"

    info = {"has_checkpoint": False, "epoch": 0, "loss": None, "checkpoint": None}
    for ckpt in [best, latest]:
        if ckpt.exists():
            try:
                import torch
                data = torch.load(ckpt, map_location="cpu")
                info = {
                    "has_checkpoint": True,
                    "epoch": data.get("epoch", 0),
                    "loss": round(data.get("loss", 0), 4),
                    "checkpoint": ckpt.name,
                    "size_mb": round(ckpt.stat().st_size / (1024**2), 1),
                    "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ckpt.stat().st_mtime)),
                }
                break
            except Exception:
                pass
    return info


@app.get("/api/samples")
def get_sample_phrases():
    """Returns demo audio phrases for testing the interface."""
    return [
        {
            "id": 1,
            "language": "English",
            "phrase": "I went to college yesterday and met my friend.",
            "mode_preview": "Transcription & Clean",
        },
        {
            "id": 2,
            "language": "Tamil (Romanized)",
            "phrase": "Naan innaikku veettukku poren.",
            "tamil_original": "நான் இன்னைக்கு வீட்டுக்கு போறேன்",
            "note": "Phonetic Romanization strictly preserving spoken Tamil without English translation",
        },
        {
            "id": 3,
            "language": "Tamil (Romanized)",
            "phrase": "Enakku adhu theriyadhu.",
            "tamil_original": "எனக்கு அது தெரியாது",
            "note": "Intervocalic voicing preserved ('adhu' instead of 'athu')",
        },
        {
            "id": 4,
            "language": "English (Disfluent Sample)",
            "phrase": "I um went went to college yesterday and uh met my friend.",
            "clean_expected": "I went to college yesterday and met my friend.",
            "note": "Demonstrates Clean Mode stutter & filler removal",
        },
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
