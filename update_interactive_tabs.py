import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ── Upgraded Tab 2: Generador de Imágenes con Barra de Órdenes & Pruebas Rápidas ──
TAB_IMAGENES_CODE = '''# ═════════════════════════════════════════════════════════════
#  PESTAÑA 2: GENERADOR & GALERÍA DE IMÁGENES DE SENSORES
# ═════════════════════════════════════════════════════════════
with tab_imagenes:
    st.subheader("📸 Generador & Galería Visual de Componentes Mecatrónicos")
    st.caption("Escriba cualquier sensor, actuador o módulo para generar instantáneamente su ficha táctica, foto de referencia y plano vectorial de pines (Pinout).")

    # ── BARRA DE PROMPT INTERACTIVA PARA PEDIR IMÁGENES ──
    with st.form("form_prompt_imagenes", clear_on_submit=False):
        c_input, c_btn = st.columns([5, 1])
        with c_input:
            orden_img_escrita = st.text_input(
                "💬 Escriba su orden visual a Isabella:",
                placeholder="Ejemplo: 'dame las imágenes del sensor de flotador y calidad de agua', 'muestra el servo sg90 y el esp32'...",
                key="input_orden_img_directa"
            )
        with c_btn:
            submit_img = st.form_submit_button("🚀 Generar", use_container_width=True)

    # ── BANCO DE PRUEBAS RÁPIDAS PARA EL JEFE (1 CLICK) ──
    with st.expander("🧪 Pruebas Rápidas de Imágenes (Haga clic para probar de inmediato)", expanded=True):
        st.markdown("**Copie o pulse sobre cualquier prueba para ver sus imágenes y diagramas de pines:**")
        cp1, cp2, cp3 = st.columns(3)
        with cp1:
            if st.button("💧 Sensores de Agua: Flotador + TDS", use_container_width=True, key="p_agua"):
                st.session_state["filtro_sensor_manual"] = "agua"
        with cp2:
            if st.button("🦇 Distancia & Servos: HC-SR04 + SG90", use_container_width=True, key="p_dist"):
                st.session_state["filtro_sensor_manual"] = "distancia"
        with cp3:
            if st.button("⚡ Cerebros & Drivers: ESP32 + L298N", use_container_width=True, key="p_power"):
                st.session_state["filtro_sensor_manual"] = "driver"

    # Procesar orden escrita si el usuario pulsó Generar
    sensores_resultado = []
    texto_a_buscar = ""
    if submit_img and orden_img_escrita.strip():
        texto_a_buscar = orden_img_escrita.strip().lower()
        sensores_resultado = buscar_sensores_en_texto(texto_a_buscar)
        if sensores_resultado:
            st.success(f"✅ Isabella: Generando fichas visuales para {len(sensores_resultado)} componente(s) detectado(s).")
        else:
            st.warning("⚠️ No se detectó un nombre exacto. Buscando coincidencias generales en el catálogo...")
    
    # Si no hubo submit de form, usar filtro o pruebas rápidas
    if not sensores_resultado:
        filtro_rapido = st.session_state.get("filtro_sensor_manual", "")
        if filtro_rapido == "agua":
            sensores_resultado = [CATALOGO_SENSORES.get("sensor-nivel-flotador"), CATALOGO_SENSORES.get("sensor-calidad-agua")]
        elif filtro_rapido == "distancia":
            sensores_resultado = [CATALOGO_SENSORES.get("hc-sr04"), CATALOGO_SENSORES.get("sg90"), CATALOGO_SENSORES.get("mg996r")]
        elif filtro_rapido == "driver":
            sensores_resultado = [CATALOGO_SENSORES.get("esp32"), CATALOGO_SENSORES.get("l298n"), CATALOGO_SENSORES.get("rele-5v")]
        elif texto_a_buscar:
            for k, v in CATALOGO_SENSORES.items():
                if (texto_a_buscar in k) or (texto_a_buscar in v["nombre"].lower()) or (texto_a_buscar in v.get("descripcion", "").lower()):
                    sensores_resultado.append(v)

    # Catálogo y filtro por categorías
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        categorias = ["Todos", "Sensores de Nivel y Líquidos", "Sensores Químicos y Calidad de Líquidos", "Sensores de Distancia", "Sensores Ambientales", "Actuadores y Motores", "Controladores de Potencia", "Microcontroladores y SoCs", "Interfaces y Pantallas"]
        cat_sel = st.selectbox("Filtrar por subsistema:", categorias, key="cat_sel_imagenes")
    with col_f2:
        termino_box = st.text_input("🔍 Filtro manual por texto:", value="", placeholder="Escriba para filtrar catálogo...", key="txt_box_filtro").strip().lower()

    if not sensores_resultado:
        for k, v in CATALOGO_SENSORES.items():
            if cat_sel != "Todos" and v.get("categoria") != cat_sel:
                continue
            if termino_box:
                if (termino_box not in k) and (termino_box not in v["nombre"].lower()) and (termino_box not in v.get("descripcion", "").lower()):
                    continue
            sensores_resultado.append(v)

    # Limpiar None si hubiese
    sensores_resultado = [s for s in sensores_resultado if s]

    st.markdown(f"**Fichas Visuales y Planos Técnicos ({len(sensores_resultado)}):**")
    if sensores_resultado:
        for s in sensores_resultado:
            renderizar_tarjeta_sensor(s)
    else:
        st.info("No se encontraron sensores. Pruebe con 'flotador', 'calidad del agua', 'hc-sr04', 'esp32' o 'servo'.")'''

# ── Upgraded Tab 3: Gemelo Digital con Barra de Órdenes & Pruebas Rápidas ──
TAB_GEMELO_CODE = '''# ═════════════════════════════════════════════════════════════
#  PESTAÑA 3: GEMELO DIGITAL (OBJETO FÍSICO REAL ↔ MODELO 3D)
# ═════════════════════════════════════════════════════════════
with tab_gemelo_3d:
    st.subheader("🦾 Gemelo Digital: Objeto Físico Real ↔ Modelo 3D Holográfico")
    st.caption("Laboratorio táctico interactivo permanente. Inspección de tolerancias ISO, despiece 3D sincronizado y comparación directa con el prototipo de taller.")

    # ── BARRA DE PROMPT INTERACTIVA PARA EL GEMELO DIGITAL ──
    with st.form("form_prompt_3d", clear_on_submit=False):
        c_in_3d, c_btn_3d = st.columns([5, 1])
        with c_in_3d:
            orden_3d_escrita = st.text_input(
                "💬 Comandar al Gemelo Digital en lenguaje natural:",
                placeholder="Ejemplo: 'despliega el brazo robótico 6-DOF', 'cambia al actuador industrial', 'desarmar mecanismo'...",
                key="input_orden_3d_directa"
            )
        with c_btn_3d:
            submit_3d = st.form_submit_button("⚡ Ejecutar", use_container_width=True)

    # ── BANCO DE PRUEBAS RÁPIDAS DEL GEMELO DIGITAL ──
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
        elif any(a in o_3d_l for a in ["actuador", "motor", "rotor", "estator", "rodamiento", "608zz"]):
            st.session_state["modelo_gemelo_actual"] = "actuador"
            st.success("⚙️ Protocolo AUREX: Actuador Servo-Industrial desplegado en el banco de pruebas.")

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
        st.session_state["modelo_gemelo_actual"] = modelo_key

    with col_stat:
        st.markdown("""
        <div style="background:#0f172a; border:1px solid #0284c7; border-radius:8px; padding:10px 14px; font-size:0.85rem; color:#38bdf8;">
            <b>🛰️ Telemetría del Gemelo:</b> EN LÍNEA · 60 FPS<br>
            <span style="color:#94a3b8;">Rotación Dual Sincronizada · PBR Taller ↔ Holograma</span>
        </div>
        """, unsafe_allow_html=True)

    import importlib
    import plantillas.holograma_3d
    importlib.reload(plantillas.holograma_3d)
    from plantillas.holograma_3d import generar_laboratorio_holografico_3d
    raw_lab_html = generar_laboratorio_holografico_3d(modelo_inicial=modelo_key)
    clean_lab_html = raw_lab_html.replace("```html", "").replace("```", "").strip()
    st.components.v1.html(clean_lab_html, height=760, scrolling=False)'''

# Locate where tab_imagenes starts
idx_tab_img = content.find('#  PESTAÑA 2: GENERADOR & GALERÍA DE IMÁGENES DE SENSORES')
idx_tab_vis = content.find('# ═════════════════════════════════════════════════════════════\n#  PESTAÑA 3: ÓPTICA TÁCTICA Y ANÁLISIS DE VIDEO')

if idx_tab_img >= 0 and idx_tab_vis >= 0:
    prefix = content[:idx_tab_img]
    suffix = content[idx_tab_vis:]
    new_content = prefix + TAB_IMAGENES_CODE + "\n\n" + TAB_GEMELO_CODE + "\n\n" + suffix
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully replaced Tab 2 and Tab 3 with prompt-enabled interactive versions!")
else:
    print(f"Indices: img={idx_tab_img}, vis={idx_tab_vis}")

import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] app.py syntax check PASSED 100%!")
else:
    print("[ERROR] Syntax error in app.py:\n", res.stderr)
