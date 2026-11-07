import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

OLD_SECTION = '''    # ── BANCO DE PRUEBAS RÁPIDAS DEL GEMELO DIGITAL ──
    with st.expander("🧪 Pruebas Rápidas del Gemelo Digital (1 Clic)", expanded=True):
        st.markdown("**Comandos listos para interactuar con el Gemelo Digital:**")
        c_p3d_1, c_p3d_2 = st.columns(2)
        with c_p3d_1:
            if st.button("🦾 Cargar Brazo Robótico 6-DOF con Gripper", use_container_width=True, key="btn_p_brazo"):
                st.session_state["modelo_gemelo_actual"] = "brazo"
        with c_p3d_2:
            if st.button("⚙️ Cargar Actuador Servo-Industrial (Rodamiento 608ZZ)", use_container_width=True, key="btn_p_actuador"):
                st.session_state["modelo_gemelo_actual"] = "actuador"

    # Procesar orden de texto si fue enviada
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
            st.rerun()

    modelo_key = st.session_state.get("modelo_gemelo_actual", "brazo")

    # Controles superiores de telemetría
    col_mod_sel, col_stat = st.columns([2, 1])
    with col_mod_sel:
        idx_radio = 0 if modelo_key == "brazo" else 1
        modo_3d_sel = st.radio(
            "Mecanismo en Banco de Pruebas:",
            ["🦾 Brazo Robótico Articulado 6-DOF con Pinza (Gripper)", "⚙️ Actuador Robótico Servo-Industrial"],
            index=idx_radio,
            horizontal=True,
            key="radio_gemelo_mecanismo"
        )
        modelo_key = "brazo" if "Brazo" in modo_3d_sel else "actuador"
        st.session_state["modelo_gemelo_actual"] = modelo_key'''

NEW_SECTION = '''    # ── BANCO DE PRUEBAS RÁPIDAS DEL GEMELO DIGITAL ──
    with st.expander("🧪 Pruebas Rápidas del Gemelo Digital (1 Clic)", expanded=True):
        st.markdown("**Comandos listos para interactuar con el Gemelo Digital en 3D:**")
        c_p3d_1, c_p3d_2, c_p3d_3 = st.columns(3)
        with c_p3d_1:
            if st.button("🦾 Brazo Robótico 6-DOF", use_container_width=True, key="btn_p_brazo"):
                st.session_state["modelo_gemelo_actual"] = "brazo"
        with c_p3d_2:
            if st.button("⚙️ Actuador Servo 608ZZ", use_container_width=True, key="btn_p_actuador"):
                st.session_state["modelo_gemelo_actual"] = "actuador"
        with c_p3d_3:
            if st.button("🧪 Sensores 3D (TDS + OLED)", use_container_width=True, key="btn_p_sensores"):
                st.session_state["modelo_gemelo_actual"] = "sensores"

    # Procesar orden de texto si fue enviada
    if submit_3d and orden_3d_escrita.strip():
        o_3d_l = orden_3d_escrita.strip().lower()
        if any(b in o_3d_l for b in ["brazo", "arm", "gripper", "pinza", "articulad"]):
            st.session_state["modelo_gemelo_actual"] = "brazo"
            st.success("🦾 Protocolo AUREX: Brazo Robótico 6-DOF desplegado en el banco de pruebas 3D.")
        elif any(a in o_3d_l for a in ["actuador", "rotor", "estator", "rodamiento", "608zz"]):
            st.session_state["modelo_gemelo_actual"] = "actuador"
            st.success("⚙️ Protocolo AUREX: Actuador Servo-Industrial desplegado en el banco de pruebas 3D.")
        elif any(s in o_3d_l for s in ["sensor", "sensores", "tds", "oled", "calidad de agua", "calidad del agua", "sonar", "ultrason", "hc-sr04", "esp32"]):
            st.session_state["modelo_gemelo_actual"] = "sensores"
            st.success("🧪 Protocolo AUREX: Banco de Sensores 3D (Sonda TDS Titanio, Pantalla OLED, HC-SR04 y ESP32) desplegado en 3D interactivo.")
        else:
            st.warning("⚠️ No se reconoció un mecanismo 3D. Pruebe con 'brazo robótico', 'actuador' o 'sensores en 3d'.")

    modelo_key = st.session_state.get("modelo_gemelo_actual", "brazo")

    # Controles superiores de telemetría con 3 modelos
    col_mod_sel, col_stat = st.columns([2, 1])
    with col_mod_sel:
        mecanismos_opciones = [
            "🦾 Brazo Robótico 6-DOF con Pinza",
            "⚙️ Actuador Servo-Industrial",
            "🧪 Sensores 3D (TDS + OLED + HC-SR04)"
        ]
        if modelo_key == "brazo":
            idx_radio = 0
        elif modelo_key == "actuador":
            idx_radio = 1
        else:
            idx_radio = 2

        modo_3d_sel = st.radio(
            "Mecanismo / Banco en Escenario 3D:",
            mecanismos_opciones,
            index=idx_radio,
            horizontal=True,
            key="radio_gemelo_mecanismo"
        )
        if "Brazo" in modo_3d_sel:
            modelo_key = "brazo"
        elif "Actuador" in modo_3d_sel:
            modelo_key = "actuador"
        else:
            modelo_key = "sensores"
        st.session_state["modelo_gemelo_actual"] = modelo_key'''

if OLD_SECTION in content:
    content = content.replace(OLD_SECTION, NEW_SECTION)
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.py successfully upgraded to 3-model 3D Gemelo Digital!")
else:
    print("OLD_SECTION not found in app.py")

import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] app.py syntax check PASSED 100%!")
else:
    print("[ERROR] Syntax error in app.py:\n", res.stderr)
