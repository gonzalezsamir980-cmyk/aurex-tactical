"""
AUREX SOC TÁCTICO - CENTRO DE CIBERDEFENSA MULTI-DISPOSITIVO
Permite monitorear y defender servidores, bases de datos y computadoras de clientes
manteniendo a AUREX 100% blindado mediante una arquitectura Zero-Trust de aislamiento total.
"""

import os
import json
import time
import uuid
import hmac
import hashlib
from typing import Dict, List, Optional

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_NODOS = os.path.join(DIR_ACTUAL, "nodos_protegidos.json")
ARCHIVO_ORDENES = os.path.join(DIR_ACTUAL, "ordenes_defensa.json")
CLAVE_MAESTRA_SOC = "AUREX_ZERO_TRUST_DEFENSE_2026"

def inicializar_almacen_soc():
    """Garantiza la existencia de los registros de nodos y cola de órdenes."""
    if not os.path.exists(ARCHIVO_NODOS):
        # Demo inicial con 2 nodos simulados (Base de Datos Cliente y Servidor Taller)
        nodos_defecto = {
            "SRV-BD-CLIENTE-01": {
                "id": "SRV-BD-CLIENTE-01",
                "nombre": "Base de Datos ERP - Empresa Cliente Alfa",
                "tipo": "Base de Datos (MySQL / Postgres)",
                "ip_local": "192.168.1.150",
                "estado": "SEGURO",
                "ultimo_latido": time.strftime("%Y-%m-%d %H:%M:%S"),
                "amenaza_actual": None,
                "token_seguridad": hashlib.sha256(b"SRV-BD-CLIENTE-01_KEY").hexdigest()[:16]
            },
            "WS-CONTABILIDAD-02": {
                "id": "WS-CONTABILIDAD-02",
                "nombre": "Terminal Contabilidad - Cliente Beta",
                "tipo": "Estación Windows",
                "ip_local": "192.168.1.180",
                "estado": "SEGURO",
                "ultimo_latido": time.strftime("%Y-%m-%d %H:%M:%S"),
                "amenaza_actual": None,
                "token_seguridad": hashlib.sha256(b"WS-CONTABILIDAD-02_KEY").hexdigest()[:16]
            }
        }
        guardar_nodos(nodos_defecto)
        
    if not os.path.exists(ARCHIVO_ORDENES):
        with open(ARCHIVO_ORDENES, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

def obtener_nodos() -> Dict[str, dict]:
    """Carga los nodos protegidos registrados."""
    inicializar_almacen_soc()
    try:
        with open(ARCHIVO_NODOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def guardar_nodos(nodos: dict):
    """Persiste los nodos en disco."""
    try:
        with open(ARCHIVO_NODOS, "w", encoding="utf-8") as f:
            json.dump(nodos, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def registrar_nodo_nuevo(nombre: str, tipo: str, ip_local: str) -> dict:
    """Registra un nuevo dispositivo/servidor a proteger y le asigna un token criptográfico."""
    nodos = obtener_nodos()
    id_nodo = f"NODE-{uuid.uuid4().hex[:6].upper()}"
    token = hashlib.sha256(f"{id_nodo}:{CLAVE_MAESTRA_SOC}:{time.time()}".encode()).hexdigest()[:24]
    
    nuevo = {
        "id": id_nodo,
        "nombre": nombre.strip(),
        "tipo": tipo.strip(),
        "ip_local": ip_local.strip(),
        "estado": "SEGURO",
        "ultimo_latido": time.strftime("%Y-%m-%d %H:%M:%S"),
        "amenaza_actual": None,
        "token_seguridad": token
    }
    nodos[id_nodo] = nuevo
    guardar_nodos(nodos)
    return nuevo

def reportar_incidente_remoto(id_nodo: str, tipo_ataque: str, ip_atacante: str, detalle: str, token_seguridad: str) -> bool:
    """
    Función de entrada para el Centinela Cliente.
    Filtra con Zero-Trust: AUREX NO ejecuta nada, sólo registra datos estructurados y alerta al Jefe.
    """
    nodos = obtener_nodos()
    if id_nodo not in nodos:
        return False
        
    nodo = nodos[id_nodo]
    # Validación criptográfica básica de identidad
    if nodo.get("token_seguridad") != token_seguridad:
        return False
        
    nodo["estado"] = "BAJO_ATAQUE"
    nodo["ultimo_latido"] = time.strftime("%Y-%m-%d %H:%M:%S")
    nodo["amenaza_actual"] = {
        "tipo": tipo_ataque,
        "ip_atacante": ip_atacante,
        "detalle": detalle,
        "ts": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    guardar_nodos(nodos)
    
    # 1. Registrar en la caja negra forense de AUREX
    try:
        from escudo_seguridad import registrar_evento_seguridad
        registrar_evento_seguridad(
            f"ATAQUE_A_CLIENTE_{id_nodo}",
            f"Nodo '{nodo['nombre']}' ({nodo['tipo']}) bajo ataque por IP {ip_atacante}. Vector: {tipo_ataque}. Detalle: {detalle}",
            "CRÍTICA"
        )
    except Exception:
        pass
        
    # 2. Despachar sirena inmediata al teléfono del Jefe
    try:
        from alertas_movil import despachar_alerta_movil_asincrona
        despachar_alerta_movil_asincrona(
            tipo_evento=f"🚨 ATAQUE EN VIVO: {nodo['nombre']}",
            detalle=f"Vector: {tipo_ataque} | IP Atacante: {ip_atacante} | Dispositivo: {nodo['tipo']}",
            ip=ip_atacante,
            id_incidente=f"SOC-{id_nodo}"
        )
    except Exception:
        pass
        
    return True

def emitir_orden_defensa(id_nodo: str, accion: str, parametros: dict = None) -> dict:
    """
    El Jefe emite una contraorden de ciberdefensa hacia el cliente atacado.
    Acciones posibles:
    - 'BLOQUEAR_IP': Agrega regla de firewall en el cliente.
    - 'CONGELAR_BD': Pone la BD en modo READ ONLY / modo seguro.
    - 'AISLAR_RED': Corta conexiones no autorizadas en el cliente.
    - 'RESTAURAR_SEGURO': Vuelve a marcar el nodo en estado verde.
    """
    inicializar_almacen_soc()
    nodos = obtener_nodos()
    if id_nodo in nodos and accion == "RESTAURAR_SEGURO":
        nodos[id_nodo]["estado"] = "SEGURO"
        nodos[id_nodo]["amenaza_actual"] = None
        guardar_nodos(nodos)
        
    orden = {
        "id_orden": f"ORD-{uuid.uuid4().hex[:6].upper()}",
        "id_nodo": id_nodo,
        "accion": accion,
        "parametros": parametros or {},
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "estado": "PENDIENTE_EJECUCION"
    }
    
    try:
        with open(ARCHIVO_ORDENES, "r", encoding="utf-8") as f:
            ordenes = json.load(f)
    except Exception:
        ordenes = []
        
    ordenes.append(orden)
    with open(ARCHIVO_ORDENES, "w", encoding="utf-8") as f:
        json.dump(ordenes, f, indent=2, ensure_ascii=False)
        
    return orden

def obtener_ordenes_pendientes(id_nodo: str, token_seguridad: str) -> List[dict]:
    """El centinela remoto del cliente consulta si el Jefe ha enviado órdenes de defensa."""
    nodos = obtener_nodos()
    if id_nodo not in nodos or nodos[id_nodo].get("token_seguridad") != token_seguridad:
        return []
        
    try:
        with open(ARCHIVO_ORDENES, "r", encoding="utf-8") as f:
            ordenes = json.load(f)
    except Exception:
        return []
        
    pendientes = [o for o in ordenes if o.get("id_nodo") == id_nodo and o.get("estado") == "PENDIENTE_EJECUCION"]
    
    # Marcar como despachadas
    for o in pendientes:
        o["estado"] = "DESPACHADA_AL_CLIENTE"
        
    try:
        with open(ARCHIVO_ORDENES, "w", encoding="utf-8") as f:
            json.dump(ordenes, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
        
    return pendientes
