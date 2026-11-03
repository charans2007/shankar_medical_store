@echo off
title Shankar Homoeo Stores - Local Server
cd /d "%~dp0"
echo ======================================================================
echo  Starting Shankar Homoeo Stores Local Server...
echo  Open in your browser: http://127.0.0.1:5000
echo  Press Ctrl+C to stop cleanly.
echo ======================================================================
.\venv\Scripts\python.exe app.py
pause
