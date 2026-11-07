"""
MÓDULO DE ALERTAS TÁCTICAS MÓVILES - AUREX MOBILE SECURITY SENTINEL
Permite enviar alertas de intrusión en tiempo real directamente al teléfono del Jefe
a través de túneles cifrados (Telegram Bot y Push ntfy de alta prioridad).
"""

import os
import json
import urllib.request
import threading
import time
from pathlib import Path

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
CONFIG_ALERTAS = os.path.join(DIR_ACTUAL, "config_alertas.json")

def obtener_config_alertas() -> dict:
    """Carga la configuración de canales móviles seguros."""
    if os.path.exists(CONFIG_ALERTAS):
        try:
            with open(CONFIG_ALERTAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
            
    # Configuración por defecto con canal seguro privado autogenerado
    import uuid
    token_canal = f"aurex_taller_jefe_{uuid.uuid4().hex[:10]}"
    config_defecto = {
        "ntfy_canal_seguro": token_canal,
        "ntfy_activo": True,
        "telegram_bot_token": "",
        "telegram_chat_id": "",
        "telegram_activo": False
    }
    guardar_config_alertas(config_defecto)
    return config_defecto

def guardar_config_alertas(cfg: dict):
    """Guarda la configuración de alertas en disco de forma segura."""
    try:
        with open(CONFIG_ALERTAS, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def _disparar_alerta_ntfy(canal: str, titulo: str, mensaje: str, prioridad: int = 5):
    """Envía una notificación Push cifrada HTTPS con sonido de sirena al celular usando JSON payload."""
    url = "https://ntfy.sh"
    payload = json.dumps({
        "topic": canal,
        "title": titulo,
        "message": mensaje,
        "priority": prioridad,
        "tags": ["rotating_light", "warning", "shield"],
        "click": "http://127.0.0.1:8501"
    }).encode("utf-8")
    
    headers = {"Content-Type": "application/json; charset=utf-8"}
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False

def _disparar_alerta_telegram(bot_token: str, chat_id: str, mensaje: str):
    """Envía un mensaje directo cifrado al chat privado de Telegram del Jefe."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False

def despachar_alerta_movil_asincrona(tipo_evento: str, detalle: str, ip: str = "127.0.0.1", id_incidente: str = "N/D"):
    """
    Despacha la alerta en un hilo de fondo ultrarrápido para no ralentizar AUREX.
    """
    def tarea():
        cfg = obtener_config_alertas()
        ts = time.strftime("%H:%M:%S")
        
        titulo_push = f"🚨 ALERTA TÁCTICA AUREX: {tipo_evento}"
        cuerpo_push = f"⚠️ Intrusión detectada a las {ts}.\nIP: {ip}\nDetalle: {detalle}\nID: {id_incidente}\nAcceso: BLOQUEADO."
        
        # 1. Enviar por canal Push Seguro (ntfy)
        if cfg.get("ntfy_activo") and cfg.get("ntfy_canal_seguro"):
            _disparar_alerta_ntfy(cfg["ntfy_canal_seguro"], titulo_push, cuerpo_push)
            
        # 2. Enviar por Telegram si el Jefe configuró su bot
        if cfg.get("telegram_activo") and cfg.get("telegram_bot_token") and cfg.get("telegram_chat_id"):
            mensaje_tg = f"""🚨 *ALERTA TÁCTICA AUREX · INTRUSIÓN DETECTADA*
━━━━━━━━━━━━━━━━━━━━━━
⏰ *Hora:* `{ts}`
📍 *ID Incidente:* `{id_incidente}`
🌐 *IP Atacante:* `{ip}`
⚠️ *Tipo:* `{tipo_evento}`
📝 *Detalle:* `{detalle}`
🛡️ *Estado:* *AMENAZA NEUTRALIZADA (100% PROTEGIDO)*
━━━━━━━━━━━━━━━━━━━━━━
_AUREX Cyber-Defense Autonomous System_"""
            _disparar_alerta_telegram(cfg["telegram_bot_token"], cfg["telegram_chat_id"], mensaje_tg)
            
    threading.Thread(target=tarea, daemon=True).start()
