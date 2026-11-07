"""
MÓDULO DE INTEGRACIÓN GEMINI OFICIAL DINÁMICO (AUTO-DETECCIÓN DE MODELO) - AUREX
Detecta automáticamente los modelos activos en Google AI Studio (gemini-1.5-flash, gemini-2.0-flash, etc.)
y elimina cualquier error 404 de modelo.
"""

import os
import json
import urllib.request
import urllib.parse

MODELO_CACHE = None

def _limpiar_key(k: str) -> str:
    if not k:
        return ""
    return str(k).strip().strip('"').strip("'").strip()

def detectar_modelo_disponible(key: str) -> list[str]:
    """Consulta en vivo a Google qué modelos exactos tiene habilitados esta clave."""
    global MODELO_CACHE
    if MODELO_CACHE:
        return MODELO_CACHE

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AUREX-Tactical/2.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            modelos_validos = []
            for m in data.get("models", []):
                metodos = m.get("supportedGenerationMethods", [])
                if "generateContent" in metodos:
                    nom = m.get("name", "").replace("models/", "")
                    if nom:
                        modelos_validos.append(nom)
            
            # Priorizar los modelos Flash (más rápidos y estables)
            flashes = [m for m in modelos_validos if "flash" in m.lower() and "exp" not in m.lower()]
            otros = [m for m in modelos_validos if m not in flashes]
            candidatos = flashes + otros
            if candidatos:
                MODELO_CACHE = candidatos
                return candidatos
    except Exception:
        pass

    # Fallback predeterminado estándar
    return [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-2.0-flash",
        "gemini-pro"
    ]

def consultar_gemini_texto(prompt: str, api_key: str, modelo: str = None) -> str:
    """Envía la consulta a Google Gemini utilizando el modelo detectado dinámicamente."""
    key = _limpiar_key(api_key)
    if not key:
        return "Jefe, no se ha configurado la clave de Gemini en los Secrets."

    candidatos = detectar_modelo_disponible(key)
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    ultimo_error = ""

    for mod in candidatos[:5]:
        for ver in ["v1beta", "v1"]:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{mod}:generateContent?key={key}"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "AUREX-Tactical/2.0"
            }
            req = urllib.request.Request(url, data=data_bytes, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=25) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data["candidates"][0]["content"]["parts"][0]["text"]
            except urllib.error.HTTPError as e:
                try:
                    err_json = json.loads(e.read().decode("utf-8"))
                    msg = err_json.get("error", {}).get("message", e.reason)
                    ultimo_error = f"HTTP {e.code}: {msg}"
                except Exception:
                    ultimo_error = f"HTTP {e.code}: {e.reason}"
            except Exception as e:
                ultimo_error = str(e)

    return f"Jefe, anomalía al conectar con el satélite Gemini ({ultimo_error})."

def _hacer_peticion_gemini(payload: dict, api_key: str, timeout: int = 30) -> str:
    """Adaptador compatible para cualquier prompt o payload multimodal."""
    texto = ""
    try:
        texto = payload["contents"][0]["parts"][0]["text"]
    except Exception:
        texto = str(payload)
    return consultar_gemini_texto(texto, api_key)
