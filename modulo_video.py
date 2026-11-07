"""
AUREX — Módulo Táctico de Análisis y Asimilación de Video (Optimizado para Alta Velocidad)
========================================================================================
Optimizaciones activas:
  1. Whisper 'base' con int8 y 6 hilos CPU (~3x a 4x más veloz que 'small').
  2. Barra de progreso en tiempo real que avanza con cada frase transcrita.
  3. Modos tácticos: "⚡ Rápido (Audio + 4 Fotogramas)", "🎙️ Solo Audio/Clase (Ultrarrápido)", "👁️ Solo Visual".
  4. Redimensionamiento liviano de fotogramas a 512px para inferencia ultrarrápida en Qwen 2.5 VL.
"""

import os
import io
import wave
import tempfile
from pathlib import Path
from typing import List, Tuple, Dict, Any, Callable, Optional
from PIL import Image
import av
import ollama
from faster_whisper import WhisperModel


_MODELO_WHISPER_BASE = None

def cargar_whisper_base():
    """Carga y mantiene en memoria el modelo Whisper 'base' de alta velocidad."""
    global _MODELO_WHISPER_BASE
    if _MODELO_WHISPER_BASE is None:
        try:
            _MODELO_WHISPER_BASE = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=6)
        except Exception as e:
            print(f"[AUREX Video] Error cargando whisper base: {e}")
    return _MODELO_WHISPER_BASE


def formatear_segundos_a_tiempo(segundos: float) -> str:
    """Convierte segundos en formato mm:ss o hh:mm:ss."""
    seg = max(0, int(segundos))
    m, s = divmod(seg, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def extraer_audio_y_fotogramas(
    ruta_video: str,
    extraer_visual: bool = True,
    intervalo_segundos: float = 25.0,
    max_fotogramas: int = 4,
    *args,
    **kwargs
) -> Tuple[str, List[Dict[str, Any]], float]:
    """
    Abre un video usando PyAV y extrae:
      - Archivo temporal .wav a 16kHz mono para Whisper.
      - Fotogramas clave livianos (512px) solo si extraer_visual es True.
      - Duración estimada en segundos.
    """
    ruta_wav = ""
    fotogramas = []
    duracion_segundos = 0.0

    try:
        container = av.open(ruta_video)
        
        if container.duration:
            duracion_segundos = float(container.duration) / av.time_base
        
        audio_stream = next((s for s in container.streams if s.type == 'audio'), None)
        video_stream = next((s for s in container.streams if s.type == 'video'), None)

        # 1. Extraer pista sonora a 16kHz mono
        if audio_stream:
            fd_wav, ruta_wav = tempfile.mkstemp(suffix=".wav", prefix="aurex_vid_audio_")
            os.close(fd_wav)
            
            resampler = av.AudioResampler(format='s16', layout='mono', rate=16000)
            with wave.open(ruta_wav, 'wb') as wav_out:
                wav_out.setnchannels(1)
                wav_out.setsampwidth(2)
                wav_out.setframerate(16000)
                
                for frame in container.decode(audio_stream):
                    for rf in resampler.resample(frame):
                        wav_out.writeframes(rf.to_ndarray().tobytes())

        # 2. Extraer fotogramas clave solo si el modo lo solicita
        if video_stream and extraer_visual:
            container.seek(0)
            tiempo_siguiente = 0.0
            
            if duracion_segundos > 0:
                paso = max(intervalo_segundos, duracion_segundos / max_fotogramas)
            else:
                paso = intervalo_segundos

            for frame in container.decode(video_stream):
                tiempo_actual = float(frame.pts * video_stream.time_base) if frame.pts else 0.0
                if tiempo_actual >= tiempo_siguiente and len(fotogramas) < max_fotogramas:
                    img = frame.to_image()
                    # Reducir a 512px para que Qwen responda al instante
                    img.thumbnail((512, 512))
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=80)
                    
                    fotogramas.append({
                        "tiempo_seg": tiempo_actual,
                        "tiempo_str": formatear_segundos_a_tiempo(tiempo_actual),
                        "bytes": buf.getvalue(),
                        "pil_img": img
                    })
                    tiempo_siguiente += paso

        container.close()
    except Exception as e:
        print(f"[AUREX Video] Error extrayendo multimedia: {e}")

    return ruta_wav, fotogramas, duracion_segundos


def transcribir_audio_video(
    ruta_wav: str,
    modelo_whisper=None,
    callback_progreso: Optional[Callable[[float, float, float], None]] = None
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Transcribe el audio con Whisper 'base' informando el progreso en vivo.
    """
    if not ruta_wav or not os.path.exists(ruta_wav):
        return "", []

    if modelo_whisper is None:
        modelo_whisper = cargar_whisper_base()

    try:
        segmentos, info = modelo_whisper.transcribe(
            ruta_wav,
            beam_size=2,          # beam_size 2 es el doble de rápido que 5 con casi idéntica precisión
            language="es",
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        duracion_total = info.duration if info and info.duration else 1.0
        lineas_transcripcion = []
        lista_segmentos = []
        
        for seg in segmentos:
            t_inicio = formatear_segundos_a_tiempo(seg.start)
            t_fin = formatear_segundos_a_tiempo(seg.end)
            texto_limpio = seg.text.strip()
            
            if texto_limpio:
                lineas_transcripcion.append(f"[{t_inicio} -> {t_fin}] {texto_limpio}")
                lista_segmentos.append({
                    "inicio": seg.start,
                    "fin": seg.end,
                    "inicio_str": t_inicio,
                    "texto": texto_limpio
                })

            if callback_progreso and duracion_total > 0:
                pct = min(1.0, seg.end / duracion_total)
                callback_progreso(pct, seg.end, duracion_total)
        
        transcripcion_completa = "\n".join(lineas_transcripcion)
        return transcripcion_completa, lista_segmentos
    except Exception as e:
        print(f"[AUREX Video] Error en transcripción Whisper: {e}")
        return "", []


def analizar_fotogramas_con_qwen(
    fotogramas: List[Dict[str, Any]],
    modelo_vision: str = "qwen2.5vl:3b",
    callback_progreso: Optional[Callable[[int, int], None]] = None
) -> str:
    """
    Analiza fotogramas clave en Qwen 2.5 VL con respuestas rápidas y concretas.
    """
    if not fotogramas:
        return "Sin inspección visual de fotogramas."

    reportes_visuales = []
    total = len(fotogramas)

    for i, item in enumerate(fotogramas):
        if callback_progreso:
            callback_progreso(i + 1, total)
        try:
            resp = ollama.chat(
                model=modelo_vision,
                messages=[{
                    "role": "user",
                    "content": "Describe en máximo 2 oraciones qué componentes, diagramas, fórmulas o acciones técnicas se ven en este instante.",
                    "images": [item["bytes"]]
                }],
                options={"temperature": 0.2, "num_predict": 120}
            )
            descripcion = resp["message"]["content"].strip()
            reportes_visuales.append(f"- **Minuto [{item['tiempo_str']}]:** {descripcion}")
        except Exception as e:
            reportes_visuales.append(f"- **Minuto [{item['tiempo_str']}]:** (Fotograma analizado: {e})")

    return "\n".join(reportes_visuales)


def generar_sintesis_video_aurex(
    nombre_video: str,
    transcripcion: str,
    resumen_visual: str,
    pregunta_jefe: str,
    modelo_llm: str = "llama3.2:latest"
) -> str:
    """
    LLaMA 3.2 compila el informe técnico de ingeniería mecatrónica.
    """
    prompt = f"""Eres AUREX, Ingeniero Mecatrónico Senior.
Has analizado una grabación técnica o clase ({nombre_video}).

DATOS DEL VIDEO:
--------------------------------
CRÓNICA VISUAL (Qwen 2.5 VL):
{resumen_visual if resumen_visual else "Solo pista de audio o clase hablada."}

TRANSCRIPCIÓN CON MARCAS DE TIEMPO (Whisper):
{transcripcion if transcripcion else "Video sin voz/audio detectable."}
--------------------------------

DIRECTIVA DEL JEFE: {pregunta_jefe}

INSTRUCCIONES:
- Dirígete a él ÚNICAMENTE como "Jefe".
- Estructura tu respuesta así:
  ### 📌 Resumen Ejecutivo de la Grabación
  ### ⏱️ Momentos Clave y Desarrollo Técnico (cita los minutos como [01:23])
  ### ⚙️ Ecuaciones, Componentes o Mecanismos Mencionados
  ### 🎯 Respuesta Directa a la Pregunta del Jefe"""

    try:
        resp = ollama.chat(
            model=modelo_llm,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2, "num_predict": 2500}
        )
        return resp["message"]["content"].strip()
    except Exception as e:
        return f"Jefe, anomalía al compilar el análisis del video: {e}"


def asimilar_video_en_memoria_aurex(
    nombre_video: str,
    transcripcion: str,
    resumen_visual: str,
    docs_dir: str = "./documentos"
) -> str:
    """
    Guarda la transcripción y cronología del video en la carpeta de documentos
    para que la memoria RAG (ChromaDB) de AUREX lo aprenda permanentemente.
    """
    os.makedirs(docs_dir, exist_ok=True)
    nombre_base = Path(nombre_video).stem
    nombre_archivo_doc = f"Video_{nombre_base}_protocolo.txt"
    ruta_guardado = os.path.join(docs_dir, nombre_archivo_doc)

    contenido = f"""REGISTRO DE VIDEO ASIMILADO POR AUREX
====================================
Archivo de origen: {nombre_video}
Tipo: Clase técnica / Grabación aprendida por AUREX

CRÓNICA VISUAL DE FOTOGRAMAS:
{resumen_visual}

TRANSCRIPCIÓN COMPLETA CON MARCAS DE TIEMPO:
{transcripcion}
"""
    with open(ruta_guardado, "w", encoding="utf-8") as f:
        f.write(contenido)

    return ruta_guardado
