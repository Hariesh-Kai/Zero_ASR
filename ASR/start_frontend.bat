@echo off
title ASR React Frontend
echo ===================================================
echo Starting ASR React Frontend (Vite Dev Server)...
echo ===================================================
cd /d "%~dp0frontend"
call npm.cmd run dev
pause
