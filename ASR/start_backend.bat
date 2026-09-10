@echo off
title ASR Backend Server
echo ===================================================
echo Starting ASR Backend Server (FastAPI + GPU Conformer-CTC)...
echo ===================================================
cd /d "%~dp0backend"
"..\.venv\Scripts\python.exe" -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
pause
