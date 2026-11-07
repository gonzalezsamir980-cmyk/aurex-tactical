@echo off
title AUREX - Probador de Wake Word en Vivo
color 0b
cd /d "%~dp0"
echo ========================================================
echo        PROBADOR DE ESCUCHA CONTINUA EN VIVO - AUREX
echo ========================================================
echo.
python aurex_wake_listener.py
pause
