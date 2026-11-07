"""
DESPLEGADOR INTELIGENTE DE AUREX (CONTROL DE INSTANCIA ÚNICA)
- Si AUREX ya está abierto en otra ventana, NO abre pestañas nuevas; simplemente trae la ventana existente al frente.
- Si no está abierto, arranca Ollama, Streamlit y abre la ventana en modo aplicación de escritorio.
"""

import os
import sys
import time
import socket
import subprocess

PROYECTO_DIR = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local"
URL_AUREX = "http://localhost:8501"

def enfocar_ventana_existente() -> bool:
    """
    Comprueba si ya hay una ventana de AUREX abierta.
    Si existe, la trae al frente inmediatamente sin abrir duplicados.
    """
    cmd = '''
    $ws = New-Object -ComObject Wscript.Shell
    if ($ws.AppActivate("AUREX · Sistema Táctico Personal") -or $ws.AppActivate("AUREX TACTICAL") -or $ws.AppActivate("AUREX")) {
        exit 0
    } else {
        exit 1
    }
    '''
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
        )
        return (res.returncode == 0)
    except Exception:
        return False

def esta_puerto_activo(puerto=8501) -> bool:
    """Verifica si el servidor local está respondiendo."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.4)
            s.connect(("127.0.0.1", puerto))
            return True
    except Exception:
        return False

def lanzar_aurex():
    # 1. Si ya está la ventana abierta, traerla al frente y no hacer nada más
    if enfocar_ventana_existente():
        print("[AUREX] La ventana ya estaba abierta. Se ha traído al frente sin duplicar.")
        return

    # 2. Iniciar Ollama con protección de VRAM para RTX 3050 (6GB)
    os.environ["OLLAMA_MAX_LOADED_MODELS"] = "1"
    os.environ["OLLAMA_NUM_PARALLEL"] = "1"
    try:
        cmd_ollama = 'set OLLAMA_MAX_LOADED_MODELS=1 && set OLLAMA_NUM_PARALLEL=1 && start /b ollama serve'
        subprocess.Popen(cmd_ollama, shell=True)
    except Exception:
        pass

    # 3. Iniciar servidor Streamlit si no está activo
    if not esta_puerto_activo(8501):
        print("[AUREX] Iniciando núcleo de Streamlit en segundo plano...")
        cmd_streamlit = f'cd /d "{PROYECTO_DIR}" && start /b streamlit run app.py --server.headless=true --server.address=0.0.0.0 --server.maxUploadSize=4096'
        subprocess.Popen(cmd_streamlit, shell=True)
        
        # Esperar hasta que el puerto 8501 responda (máximo 12 segundos)
        for _ in range(24):
            time.sleep(0.5)
            if esta_puerto_activo(8501):
                break

    # 4. Abrir en Chrome (Modo App / Ventana independiente sin barras de navegador)
    print("[AUREX] Desplegando interfaz en primer plano...")
    # Intentar modo app de Chrome (ventana dedicada limpia estilo JARVIS)
    cmd_chrome = f'start chrome --app="{URL_AUREX}"'
    os.system(cmd_chrome)

    # 5. Asegurar foco activo al frente
    time.sleep(1.2)
    enfocar_ventana_existente()

if __name__ == "__main__":
    lanzar_aurex()
