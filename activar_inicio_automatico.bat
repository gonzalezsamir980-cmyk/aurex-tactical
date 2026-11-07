@echo off
title AUREX - Protocolo de Inicio Automatico
color 0b
cd /d "%~dp0"
echo ========================================================
echo       CONFIGURANDO AUTO-APERTURA DIRECTA DE AUREX
echo ========================================================
echo.
echo [1/2] Limpiando tareas previas...
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AUREX_Wake_Word.vbs" >nul 2>&1
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AUREX_Auto_Inicio.vbs" >nul 2>&1

echo [2/2] Instalando auto-apertura directa en el Inicio de Windows...
copy /Y "%~dp0iniciar_aurex_automatico_al_arrancar.vbs" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AUREX_Auto_Inicio.vbs" >nul

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo  [EXITO] AUREX SE ABRIRA AUTOMATICAMENTE AL ENCENDER SU LAPTOP
    echo ========================================================
    echo  - Al iniciar sesion en Windows, el panel se abrira de inmediato.
    echo  - Sin necesidad de activacion por voz.
    echo  - Si ya esta abierto, traera la ventana al frente sin duplicar.
    echo.
    echo Desplegando AUREX ahora mismo en su pantalla...
    start "" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AUREX_Auto_Inicio.vbs"
) else (
    echo [ERROR] No se pudo copiar el archivo al inicio de Windows.
)
echo.
pause
