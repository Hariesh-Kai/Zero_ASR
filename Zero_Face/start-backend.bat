@echo off
echo =========================================
echo      Zero AI Assistant - Backend
echo =========================================
echo.
echo Installing/Updating dependencies...
venv\Scripts\python.exe -m pip install -r backend\requirements.txt
echo.
echo Starting FastAPI server on http://0.0.0.0:8000...
venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend
pause
