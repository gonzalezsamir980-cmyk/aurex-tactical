"""
MÓDULO DE INTEGRACIÓN GROQ CLOUD (HIPER-VELOCIDAD Y RESILIENTE) - AUREX
Soporta Llama 3.3 70B y Llama 3.1 8B Instant con headers anti-bloqueo Cloudflare y fallback automático.
"""

import os
import json
import base64
import requests

MODELO_TEXTO = "llama-3.3-70b-versatile"
MODELO_RAPIDO = "llama-3.1-8b-instant"
MODELO_VISION = "llama-3.2-11b-vision-preview"

def _limpiar_key(key: str) -> str:
    """Elimina comillas, espacios y saltos de línea accidentales."""
    if not key:
        return ""
    return str(key).strip().strip('"').strip("'").strip()

def consultar_groq_texto(prompt: str, api_key: str, modelo: str = MODELO_TEXTO) -> str:
    """Envía consultas de texto ultra rápidas a Groq Cloud con reintentos y fallback."""
    key_limpia = _limpiar_key(api_key)
    if not key_limpia:
        return "Jefe, no se ha configurado la API Key de Groq en los Secrets del sistema."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key_limpia}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 AUREX-Tactical/2.0"
    }

    modelos_a_probar = [modelo, MODELO_RAPIDO, "mixtral-8x7b-32768"]
    ultimo_error = ""

    for mod in modelos_a_probar:
        payload = {
            "model": mod,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 4096
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                ultimo_error = f"HTTP Error {resp.status_code}: {resp.text[:180]}"
        except Exception as e:
            ultimo_error = str(e)

    # Si Groq falla por completo, intentar Gemini si existe GEMINI_API_KEY
    try:
        import streamlit as st
        gem_key = _limpiar_key(st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", ""))
        if gem_key:
            from modulo_gemini import _hacer_peticion_gemini
            res_gem = _hacer_peticion_gemini({"contents": [{"parts": [{"text": prompt}]}]}, gem_key)
            if res_gem:
                return res_gem
    except Exception:
        pass

    return f"Jefe, anomalía en el enlace con el satélite Groq ({ultimo_error}). Por favor verifique que su clave no tenga espacios."

def consultar_groq_vision(prompt: str, imagen_bytes: bytes, mime_type: str, api_key: str) -> str:
    """Analiza imágenes técnicas con el modelo de visión de Groq a hipervelocidad."""
    key_limpia = _limpiar_key(api_key)
    if not key_limpia:
        return "Jefe, se requiere la API Key de Groq para la visión satelital."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key_limpia}",
        "User-Agent": "AUREX-Tactical/2.0"
    }

    b64_img = base64.b64encode(imagen_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{b64_img}"

    payload = {
        "model": MODELO_VISION,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 2048
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        return f"Jefe, anomalía visual en Groq: HTTP {resp.status_code}"
    except Exception as e:
        return f"Jefe, anomalía visual en satélite Groq: {e}"
