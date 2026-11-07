@echo off
title AUREX - Instalador Automatico en Nueva PC
chcp 65001 >nul
cls

echo ============================================================
echo      AUREX - PROTOCOLO DE DESPLIEGUE EN NUEVA COMPUTADORA
echo ============================================================
echo.
echo [1/3] Verificando Python y librerias...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Hubo un problema instalando las librerias. Verifique su conexion.
    pause
    exit /b
)

echo.
echo [2/3] Verificando modelos en Ollama...
ollama pull llama3.2:latest
ollama pull nomic-embed-text:latest
ollama pull qwen2.5vl:3b
ollama pull deepseek-r1:7b

echo.
echo [3/3] Desbloqueando puerto de red local (8501)...
netsh advfirewall firewall add rule name="AUREX_Server" dir=in action=allow protocol=TCP localport=8501 >nul 2>&1

echo.
echo ============================================================
echo   AUREX HA SIDO INSTALADO CON EXITO EN ESTA NUEVA PC
echo   Ya puede iniciar con: iniciar_aurex.bat
echo ============================================================
echo.
pause
