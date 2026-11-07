import sys

ruta = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py"
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

target = """        # ── 1. EVALUAR COMANDOS TÁCTICOS DE CONTROL DE PC (J.A.R.V.I.S.) ──
        es_cmd_pc, respuesta_pc = detectar_y_ejecutar_comando_pc(orden)
        if es_cmd_pc:
            st.session_state.historial.append({
                "rol": "ia",
                "texto": respuesta_pc,
                "fuentes": []
            })
            st.session_state.ultimo_streaming = respuesta_pc
            st.rerun()"""

replacement = """        # ── 0.5. EVALUAR ÓRDENES DE CIBERDEFENSA TÁCTICA INALÁMBRICA / REMOTA ──
        try:
            from intervencion_autonoma import procesar_comando_tactico_ciberdefensa
            es_cmd_def, resp_def = procesar_comando_tactico_ciberdefensa(orden)
            if es_cmd_def:
                st.session_state.historial.append({
                    "rol": "ia",
                    "texto": resp_def,
                    "fuentes": []
                })
                st.session_state.ultimo_streaming = resp_def
                st.rerun()
        except Exception:
            pass

        # ── 1. EVALUAR COMANDOS TÁCTICOS DE CONTROL DE PC (J.A.R.V.I.S.) ──
        es_cmd_pc, respuesta_pc = detectar_y_ejecutar_comando_pc(orden)
        if es_cmd_pc:
            st.session_state.historial.append({
                "rol": "ia",
                "texto": respuesta_pc,
                "fuentes": []
            })
            st.session_state.ultimo_streaming = respuesta_pc
            st.rerun()"""

if target not in contenido:
    print("ERROR: Target no encontrado")
    sys.exit(1)

contenido = contenido.replace(target, replacement, 1)

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print("COMANDO DE CIBERDEFENSA CONECTADO A APP.PY CON EXITO")
