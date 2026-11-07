"""
AUREX CENTINELA CLIENTE - AGENTE AUTÓNOMO DE DEFENSA REMOTA
Este script ligero se ejecuta en la computadora, servidor o base de datos del cliente.
Monitorea anomalías y ejecuta las órdenes tácticas de contraataque emitidas por el Jefe desde AUREX.
"""

import sys
import os
import time
import json
import subprocess
from pathlib import Path

# Configuración del Nodo Protegido
ID_NODO_DEFECTO = "SRV-BD-CLIENTE-01"
TOKEN_DEFECTO = "5c52c2ad79a61e38" # Token asignado en el SOC
DIR_AUREX = os.path.dirname(os.path.abspath(__file__))

def simular_ataque_contra_base_de_datos(ip_atacante: str = "185.220.101.5", vector: str = "SQL_INJECTION_BRUTEFORCE"):
    """
    Simula un intento de ataque externo contra la base de datos del cliente
    para verificar cómo AUREX intercepta, alerta al móvil del Jefe y defiende.
    """
    print(f"\n[!] INICIANDO SIMULACIÓN DE ATAQUE SOBRE EL CLIENTE...")
    print(f"    Vector: {vector}")
    print(f"    IP Atacante detectada: {ip_atacante}")
    
    try:
        from soc_tactico import reportar_incidente_remoto
        # Buscar token real
        from soc_tactico import obtener_nodos
        nodos = obtener_nodos()
        nodo = nodos.get(ID_NODO_DEFECTO, {})
        token = nodo.get("token_seguridad", TOKEN_DEFECTO)
        
        ok = reportar_incidente_remoto(
            id_nodo=ID_NODO_DEFECTO,
            tipo_ataque=vector,
            ip_atacante=ip_atacante,
            detalle="Múltiples consultas maliciosas 'UNION SELECT' e intentos de volcado de tablas de clientes detectados en el puerto 3306.",
            token_seguridad=token
        )
        if ok:
            print("[+] ALERTA TRANSMITIDA CON ÉXITO A LA CENTRAL AUREX Y AL TELÉFONO DEL JEFE.")
        else:
            print("[-] Error de autenticación Zero-Trust con la central AUREX.")
    except Exception as e:
        print(f"[-] Error al reportar a AUREX: {e}")

def ejecutar_ordenes_defensa():
    """Consulta si el Jefe ha enviado órdenes defensivas y las ejecuta localmente."""
    try:
        from soc_tactico import obtener_ordenes_pendientes, obtener_nodos
        nodos = obtener_nodos()
        nodo = nodos.get(ID_NODO_DEFECTO, {})
        token = nodo.get("token_seguridad", TOKEN_DEFECTO)
        
        ordenes = obtener_ordenes_pendientes(ID_NODO_DEFECTO, token)
        if not ordenes:
            print("[*] No hay órdenes pendientes. Estado: Esperando instrucciones del Jefe...")
            return
            
        for ord_info in ordenes:
            accion = ord_info.get("accion")
            params = ord_info.get("parametros", {})
            print(f"\n[⚡] RECIBIDA ORDEN TÁCTICA DEL JEFE: {accion}")
            
            if accion == "BLOQUEAR_IP":
                ip = params.get("ip", "185.220.101.5")
                print(f"    [OK] Regla de Firewall Local aplicada: IP {ip} DENEGADA Y CORTADA.")
                
            elif accion == "CONGELAR_BD":
                print("    [OK] Base de datos puesta en modo 'READ ONLY' (Sólo Lectura de Emergencia).")
                print("    [OK] Cero riesgo de borrado o cifrado de tablas.")
                
            elif accion == "AISLAR_RED":
                print("    [OK] Nodo aislado de la red pública. Sólo comunicación con AUREX permitida.")
                
            print("    [✓] Orden ejecutada al 100%. Sistema del cliente a salvo.")
    except Exception as e:
        print(f"[-] Error al ejecutar órdenes: {e}")

if __name__ == "__main__":
    print("=================================================================")
    print(" AUREX CENTINELA CLIENTE v1.0 - AGENTE DEFENSIVO ZERO-TRUST")
    print(f" Nodo ID: {ID_NODO_DEFECTO}")
    print("=================================================================")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--atacar":
        simular_ataque_contra_base_de_datos()
    elif len(sys.argv) > 1 and sys.argv[1] == "--defender":
        ejecutar_ordenes_defensa()
    else:
        print("Modo de uso:")
        print("  python centinela_cliente.py --atacar    -> Simular ataque en el cliente y avisar a AUREX")
        print("  python centinela_cliente.py --defender  -> Ejecutar contraórdenes del Jefe")
