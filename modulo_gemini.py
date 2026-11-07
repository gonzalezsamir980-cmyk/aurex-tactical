"""
MÓDULO DE INTEGRACIÓN GEMINI OFICIAL (ULTRA-RESILIENTE PARA NUBE) - AUREX
Usa la API oficial de Google Gemini (gemini-1.5-flash / gemini-2.0-flash).
"""

import os
import json
import urllib.request
import urllib.parse

def _limpiar_key(k: str) -> str:
    if not k:
        return ""
    return str(k).strip().strip('"').strip("'").strip()

def consultar_gemini_texto(prompt: str, api_key: str, modelo: str = "gemini-1.5-flash") -> str:
    """Envía consulta de texto a Google Gemini usando la ruta oficial de Google AI Studio."""
    key = _limpiar_key(api_key)
    if not key:
        return "Jefe, no se ha configurado la clave de Gemini en los Secrets."

    modelos = [modelo, "gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
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

    for mod in modelos:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={key}"
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
                err_body = e.read().decode("utf-8")
                ultimo_error = f"HTTP {e.code}: {err_body[:160]}"
            except Exception:
                ultimo_error = f"HTTP {e.code}: {e.reason}"
        except Exception as e:
            ultimo_error = str(e)

    return f"Jefe, anomalía al conectar con el satélite Gemini ({ultimo_error})."

def _hacer_peticion_gemini(payload: dict, api_key: str, timeout: int = 30) -> str:
    """Adaptador de compatibilidad para llamadas directas con payload."""
    key = _limpiar_key(api_key)
    if not key:
        return "Jefe, clave de Gemini no detectada."
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "AUREX-Tactical/2.0"
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data_bytes, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        try:
            return f"Jefe, detalle de Gemini: HTTP {e.code} - {e.read().decode('utf-8')[:160]}"
        except Exception:
            return f"Jefe, detalle de Gemini: HTTP {e.code}"
    except Exception as e:
        return f"Jefe, detalle de Gemini: {e}"
