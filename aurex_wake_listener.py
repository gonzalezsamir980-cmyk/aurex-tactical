"""
AUREX WAKE WORD LISTENER - SISTEMA DE ESCUCHA CONTINUA EN SEGUNDO PLANO
Monitorea el micrófono en segundo plano consumiendo 0% de CPU en silencio.
Cuando el Jefe dice 'AUREX', despliega automáticamente la consola táctica en pantalla.
"""

import os
import sys
import time
import socket
import tempfile
import wave
import subprocess
import threading
import winsound
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

PROYECTO_DIR = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local"
MODELO_WHISPER = "tiny"
SAMPLE_RATE = 16000

print("=" * 60)
print("       AUREX BACKGROUND LISTENER - INGENIERO SENIOR")
print("          Esperando palabra clave táctica: 'AUREX'")
print("=" * 60)

# ── 1. BUSCADOR INTELIGENTE DE MICRÓFONO WDM-KS ─────────────
def buscar_microfono():
    """Localiza el micrófono WDM-KS (Device 19 Realtek) que funciona en esta máquina."""
    try:
        devs = sd.query_devices()
        candidatos = []
        for i, d in enumerate(devs):
            if d.get("hostapi") == 3 and d.get("max_input_channels", 0) > 0:
                sr = int(d.get("default_samplerate", 44100))
                candidatos.append((i, sr, min(2, d["max_input_channels"]), d["name"]))
        
        # Probar y medir RMS
        mejores = []
        for idx, sr, ch, nom in candidatos:
            try:
                data = sd.rec(int(sr * 0.25), samplerate=sr, channels=ch, dtype="float32", device=idx)
                sd.wait()
                mono = np.mean(data, axis=1) if data.ndim > 1 else data.flatten()
                rms = float(np.sqrt(np.mean(mono ** 2)))
                mejores.append((rms, idx, sr, ch, nom))
            except Exception:
                continue
                
        if mejores:
            # Priorizar Device 19 (Mic Array) o el de mayor señal
            mejores.sort(key=lambda x: (1 if "array" in x[4].lower() else 0, x[0]), reverse=True)
            return mejores[0][1], mejores[0][2], mejores[0][3]
    except Exception as e:
        print(f"Error detectando micro: {e}")
    # Fallback por defecto a Device 19
    return 19, 44100, 2

# ── 2. COMPROBADOR DE SERVICIO Y APERTURA DE INTERFAZ ───────
def esta_streamlit_activo(puerto=8501):
    """Verifica si el servidor web de Streamlit ya está corriendo en el puerto 8501."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect(("127.0.0.1", puerto))
            return True
    except Exception:
        return False

def desplegar_interfaz_aurex():
    """Inicia Ollama y Streamlit si están apagados, y abre Chrome al frente de la pantalla."""
    print("\n⚡ [AUREX WAKE DETECTADO]: Desplegando interfaz táctica para el Jefe...")
    
    # 1. Beep táctico estilo Iron Man / Reactor Arc
    try:
        winsound.Beep(900, 90)
        winsound.Beep(1400, 140)
    except Exception:
        pass

    # 2. Iniciar Ollama si no está activo
    try:
        subprocess.Popen("start /b ollama serve", shell=True)
    except Exception:
        pass

    # 3. Iniciar Streamlit si no está activo
    if not esta_streamlit_activo(8501):
        print("  -> Iniciando servidor Streamlit de AUREX...")
        cmd_app = f'cd /d "{PROYECTO_DIR}" && start /b streamlit run app.py --server.headless=true'
        subprocess.Popen(cmd_app, shell=True)
        time.sleep(2.5)

    # 4. Abrir Google Chrome en primer plano
    url = "http://localhost:8501"
    subprocess.Popen(f'start chrome "{url}"', shell=True)

    # 5. Forzar la ventana de Chrome al frente con PowerShell Wscript
    def _enfocar():
        time.sleep(1.2)
        try:
            cmd = '$ws = New-Object -ComObject Wscript.Shell; $ws.AppActivate("Chrome")'
            subprocess.run(["powershell", "-NoProfile", "-Command", cmd],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    threading.Thread(target=_enfocar, daemon=True).start()

# ── 3. BUCLE PRINCIPAL DE ESCUCHA CONTINUA ───────────────────
def iniciar_escucha():
    mic_idx, sr_nat, mic_nom = buscar_microfono()
    print(f"🎙️ Micrófono táctico enlazado: [{mic_idx}] sr={sr_nat}")
    print("🧠 Cargando modelo neuronal ultraligero de detección...")
    
    try:
        modelo = WhisperModel(MODELO_WHISPER, device="cpu", compute_type="int8", cpu_threads=2)
    except Exception as e:
        print(f"Error cargando Whisper: {e}")
        return

    print("🟢 SISTEMA EN ESPERA: Diga en voz alta 'AUREX' para abrir su consola táctica...\n")

    chunk_duracion = 1.6 # segundos de análisis
    chunk_muestras = int(chunk_duracion * sr_nat)

    while True:
        try:
            # Grabar bloque de audio
            audio = sd.rec(chunk_muestras, samplerate=sr_nat, channels=1, dtype="float32", device=mic_idx)
            sd.wait()
            audio_mono = audio.flatten()

            # Medir nivel RMS de energía de voz
            rms = float(np.sqrt(np.mean(audio_mono ** 2)))
            
            # Si hay silencio o poco ruido, continuar sin procesar (0% consumo CPU)
            if rms < 0.008:
                time.sleep(0.04)
                continue

            # Si detectó voz con suficiente energía, resamplear a 16kHz para Whisper
            if sr_nat != SAMPLE_RATE:
                ratio = max(1, sr_nat // SAMPLE_RATE)
                n = len(audio_mono) - (len(audio_mono) % ratio)
                audio_16k = np.mean(audio_mono[:n].reshape(-1, ratio), axis=1)
            else:
                audio_16k = audio_mono

            # Guardar WAV temporal ultrarrápido
            muestras_int = (audio_16k * 32767).astype("int16")
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                ruta_wav = tmp.name
            with wave.open(ruta_wav, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(muestras_int.tobytes())

            # Transcripción instantánea con Whisper tiny
            segmentos, _ = modelo.transcribe(
                ruta_wav,
                language="es",
                beam_size=1,
                initial_prompt="AUREX, Aurex, áurex, asistente, mecatrónica, activa aurex."
            )
            texto = " ".join(s.text for s in segmentos).lower().strip()

            try:
                os.remove(ruta_wav)
            except Exception:
                pass

            # Comprobar si pronunció la palabra clave 'Aurex'
            palabras_clave = ["aurex", "áurex", "aurek", "aurecs", "aure", "abre aurex", "inicia aurex"]
            coincide = any(w in texto for w in palabras_clave)

            if coincide:
                print(f"🎯 [DETECCIÓN POSITIVA]: Transcripción='{texto}' (RMS={rms:.4f})")
                desplegar_interfaz_aurex()
                # Pausa de seguridad de 6 segundos para evitar re-disparos con el eco
                time.sleep(6.0)
            else:
                if len(texto) > 1:
                    # Voz detectada que no era la palabra clave
                    pass

        except Exception as e:
            time.sleep(1.0)

if __name__ == "__main__":
    iniciar_escucha()
