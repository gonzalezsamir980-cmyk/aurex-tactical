import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

OLD_BLOCK = '''    # Procesar orden de texto si fue enviada
    if submit_3d and orden_3d_escrita.strip():
        o_3d_l = orden_3d_escrita.strip().lower()
        if any(b in o_3d_l for b in ["brazo", "arm", "gripper", "pinza", "articulad"]):
            st.session_state["modelo_gemelo_actual"] = "brazo"
            st.success("🦾 Protocolo AUREX: Brazo Robótico 6-DOF desplegado en el banco de pruebas.")
        elif any(a in o_3d_l for a in ["actuador", "motor", "rotor", "estator", "rodamiento", "608zz"]):
            st.session_state["modelo_gemelo_actual"] = "actuador"
            st.success("⚙️ Protocolo AUREX: Actuador Servo-Industrial desplegado en el banco de pruebas.")'''

NEW_BLOCK = '''    # Procesar orden de texto si fue enviada
    if submit_3d and orden_3d_escrita.strip():
        o_3d_l = orden_3d_escrita.strip().lower()
        if any(b in o_3d_l for b in ["brazo", "arm", "gripper", "pinza", "articulad"]):
            st.session_state["modelo_gemelo_actual"] = "brazo"
            st.success("🦾 Protocolo AUREX: Brazo Robótico 6-DOF desplegado en el banco de pruebas.")
        elif any(a in o_3d_l for a in ["actuador", "rotor", "estator", "rodamiento", "608zz"]):
            st.session_state["modelo_gemelo_actual"] = "actuador"
            st.success("⚙️ Protocolo AUREX: Actuador Servo-Industrial desplegado en el banco de pruebas.")
        else:
            # Si el usuario escribió nombres de sensores aquí en la pestaña 3D, generarlos de inmediato
            sensores_detectados_3d = buscar_sensores_en_texto(o_3d_l)
            if sensores_detectados_3d:
                st.session_state["sensores_mostrar_en_3d"] = sensores_detectados_3d
                st.success(f"📸 Isabella: ¡Fichas visuales generadas para {len(sensores_detectados_3d)} componente(s) solicitado(s)!")
            else:
                st.warning("⚠️ No se detectó comando 3D (Brazo/Actuador) ni sensores conocidos. Pruebe con 'cambia al actuador' o 'brazo robótico'.")

    # Renderizar sensores solicitados dentro del Gemelo Digital si hubiese
    sensores_en_3d = st.session_state.get("sensores_mostrar_en_3d", [])
    if sensores_en_3d:
        st.markdown(f"**Componentes mecatrónicos generados ({len(sensores_en_3d)}):**")
        for s in sensores_en_3d:
            renderizar_tarjeta_sensor(s)
        if st.button("❌ Ocultar Fichas de Sensores", key="btn_ocultar_sensores_3d"):
            del st.session_state["sensores_mostrar_en_3d"]
            st.rerun()'''

if OLD_BLOCK in content:
    content = content.replace(OLD_BLOCK, NEW_BLOCK)
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully patched app.py with cross-tab sensor generation in 3D tab!")
else:
    print("OLD_BLOCK not found")

import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] app.py syntax check PASSED 100%!")
else:
    print("[ERROR] Syntax error:\n", res.stderr)
