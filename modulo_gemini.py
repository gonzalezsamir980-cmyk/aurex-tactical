"""
MÓDULO DE INTEGRACIÓN GEMINI MULTIMODAL (VIDEO, IMÁGENES Y CEREBRO NUBE) - AUREX
Soporta claves de nueva generación vía Header X-goog-api-key y query param.
"""

import os
import urllib.request
import urllib.parse
import json
import base64

MODELOS_A_PROBAR = [
    "gemini-flash-latest",
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash-latest"
]

def _hacer_peticion_gemini(payload: dict, api_key: str, timeout: int = 40) -> str:
    """Envía la petición a Gemini probando tanto el Header oficial como el query param."""
    data_bytes = json.dumps(payload).encode("utf-8")
    ultimo_error = ""

    for modelo in MODELOS_A_PROBAR:
        for version in ["v1beta", "v1"]:
            # URL sin key si se manda por header, o con key como fallback
            url = f"https://generativelanguage.googleapis.com/{version}/models/{modelo}:generateContent"
            
            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": api_key
            }

            req = urllib.request.Request(url, data=data_bytes, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    return res_data["candidates"][0]["content"]["parts"][0]["text"]
            except urllib.error.HTTPError as e:
                # Si falla por header, intentar por URL param
                ultimo_error = f"HTTP {e.code}: {e.reason}"
                if e.code == 404 or e.code == 400:
                    try:
                        url_con_key = f"{url}?key={api_key}"
                        req2 = urllib.request.Request(url_con_key, data=data_bytes, headers={"Content-Type": "application/json"})
                        with urllib.request.urlopen(req2, timeout=timeout) as response2:
                            res_data2 = json.loads(response2.read().decode("utf-8"))
                            return res_data2["candidates"][0]["content"]["parts"][0]["text"]
                    except Exception:
                        pass
                continue
            except Exception as e:
                ultimo_error = str(e)
                continue

    return f"Jefe, anomalía al conectar con el satélite Gemini ({ultimo_error})."

def consultar_gemini_texto(prompt: str, api_key: str, modelo: str = None) -> str:
    """Envía una consulta de texto a Google Gemini."""
    if not api_key:
        return "Jefe, no se ha configurado la API Key de Gemini en el sistema."

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    return _hacer_peticion_gemini(payload, api_key, timeout=25)

def consultar_gemini_multimodal(prompt: str, archivo_bytes: bytes, mime_type: str, api_key: str, modelo: str = None) -> str:
    """Envía imágenes o videos a Google Gemini para su análisis técnico."""
    if not api_key:
        return "Jefe, se requiere la API Key de Gemini para el análisis audiovisual."

    datos_b64 = base64.b64encode(archivo_bytes).decode("utf-8")
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt if prompt else "Analiza detalladamente este contenido audiovisual para ingeniería."},
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": datos_b64
                    }
                }
            ]
        }]
    }
    return _hacer_peticion_gemini(payload, api_key, timeout=45)
