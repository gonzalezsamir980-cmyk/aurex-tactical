import sys

ruta = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\escudo_seguridad.py"
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

# 1. Actualizar registrar_evento_seguridad en verificar_clave_o_acertijo
target1 = """        registrar_evento_seguridad(
            "INTENTO_HACKEO_FUERZA_BRUTA", 
            f"Intento de intrusión con clave o respuesta no autorizada. Intento: '{intento[:3]}***'. Total fallos acumulados: {datos['intentos_fallidos']}", 
            "CRÍTICA"
        )
        return False"""

replacement1 = """        ev = registrar_evento_seguridad(
            "INTENTO_HACKEO_FUERZA_BRUTA", 
            f"Intento de intrusión con clave o respuesta no autorizada. Intento: '{intento[:3]}***'. Total fallos acumulados: {datos['intentos_fallidos']}", 
            "CRÍTICA"
        )
        try:
            from alertas_movil import despachar_alerta_movil_asincrona
            despachar_alerta_movil_asincrona(
                "INTENTO_HACKEO_FUERZA_BRUTA",
                f"Clave incorrecta introducida. Total intentos fallidos: {datos['intentos_fallidos']}",
                ip=ev.get("ip_atacante", "127.0.0.1"),
                id_incidente=ev.get("id_incidente", "N/D")
            )
        except Exception:
            pass
        return False"""

# 2. Actualizar detectar_prompt_injection
target2 = 'registrar_evento_seguridad("PROMPT_INJECTION_BLOQUEADO", f"Texto sospechoso interceptado: \'{patron}\' -> Motivo: {motivo}", "CRÍTICA")\n            return True, motivo'

replacement2 = '''ev = registrar_evento_seguridad("PROMPT_INJECTION_BLOQUEADO", f"Texto sospechoso interceptado: '{patron}' -> Motivo: {motivo}", "CRÍTICA")
            try:
                from alertas_movil import despachar_alerta_movil_asincrona
                despachar_alerta_movil_asincrona(
                    "PROMPT_INJECTION_BLOQUEADO",
                    f"Patron malicioso neutralizado en chat: '{patron}'. Motivo: {motivo}",
                    ip=ev.get("ip_atacante", "127.0.0.1"),
                    id_incidente=ev.get("id_incidente", "N/D")
                )
            except Exception:
                pass
            return True, motivo'''

if target1 not in contenido:
    print("ERROR: target1 no encontrado")
    sys.exit(1)

if target2 not in contenido:
    print("ERROR: target2 no encontrado")
    sys.exit(1)

contenido = contenido.replace(target1, replacement1, 1)
contenido = contenido.replace(target2, replacement2, 1)

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print("PARCHE 1 Y 2 APLICADOS CON EXITO")
