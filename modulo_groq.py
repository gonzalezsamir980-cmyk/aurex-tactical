"""
MÓDULO DE INTEGRACIÓN GROQ CLOUD (HIPER-VELOCIDAD Y VISIÓN) - AUREX
Permite a AUREX usar los modelos más rápidos y potentes del mundo (Llama 3.3 70B y Llama 3.2 90B Vision).
"""

import urllib.request
import urllib.parse
import json
import base64

MODELO_TEXTO = "llama-3.3-70b-versatile"
MODELO_VISION = "llama-3.2-11b-vision-preview"

def consultar_groq_texto(prompt: str, api_key: str, modelo: str = MODELO_TEXTO) -> str:
    """Envía consultas de texto ultra rápidas a Groq Cloud."""
    if not api_key:
        return "Jefe, no se ha configurado la API Key de Groq en el sistema."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": modelo,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 4096
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Jefe, anomalía en el satélite Groq: {e}"

def consultar_groq_vision(prompt: str, imagen_bytes: bytes, mime_type: str, api_key: str) -> str:
    """Analiza imágenes técnicas con el modelo de visión de Groq a hipervelocidad."""
    if not api_key:
        return "Jefe, se requiere la API Key de Groq para la visión satelital."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    b64_img = base64.b64encode(imagen_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64_img}"

    payload = {
        "model": MODELO_VISION,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt if prompt else "Analiza detalladamente este circuito o diagrama para ingeniería."},
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url}
                    }
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 3000
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Jefe, fallo en el análisis táctico de visión con Groq: {e}"
