import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Update tab definitions at line ~1365 ──
OLD_TABS = '''tab_memoria, tab_sensores, tab_vision = st.tabs([
    "💬 Taller de Ingeniería & Artifacts",
    "🔌 Fichas Visuales de Sensores y Pinouts",
    "👁️ Visión Táctica (Diagramas, Planos y Páginas)"
])'''

NEW_TABS = '''tab_memoria, tab_imagenes, tab_gemelo_3d, tab_vision = st.tabs([
    "💬 Taller Táctico & Chat",
    "📸 Generador de Imágenes de Sensores",
    "🦾 Gemelo Digital (Físico + 3D)",
    "👁️ Visor Óptico & Video"
])'''

if OLD_TABS in content:
    content = content.replace(OLD_TABS, NEW_TABS)
    print("[OK] Tab definitions updated to 4 clean tabs")
else:
    print("[ERROR] OLD_TABS not found")

# ── 2. Replace tab_sensores with tab_imagenes and add tab_gemelo_3d ──
OLD_TAB_SENSORES = '''# ═════════════════════════════════════════════════════════════
#  PESTAÑA 2: CATÁLOGO VISUAL DE SENSORES Y PINOUTS
# ═════════════════════════════════════════════════════════════
with tab_sensores:
    st.subheader("🔌 Banco Visual de Sensores, Actuadores y Microcontroladores")
    st.caption("Fichas técnicas de alta resolución, distribución exacta de pines (Pinout), voltajes operativos y directivas de seguridad para prototipado.")
    
    col_filtro, col_search = st.columns([1, 2])
    with col_filtro:
        categorias = ["Todos", "Sensores de Distancia", "Sensores Ambientales", "Actuadores y Motores", "Controladores de Potencia", "Microcontroladores y SoCs", "Interfaces y Pantallas"]
        cat_sel = st.selectbox("Filtrar por subsistema:", categorias)
    with col_search:
        termino = st.text_input("🔍 Buscar componente por nombre o código (ej: HC-SR04, ESP32, L298N, Servo):", "").strip().lower()
        
    sensores_a_mostrar = []
    for k, v in CATALOGO_SENSORES.items():
        if cat_sel != "Todos" and v.get("categoria") != cat_sel:
            continue
        if termino:
            coincide = (termino in k) or (termino in v["nombre"].lower()) or (termino in v.get("descripcion", "").lower())
            if not coincide:
                continue
        sensores_a_mostrar.append(v)
        
    st.markdown(f"**Componentes indexados ({len(sensores_a_mostrar)}):**")
    if sensores_a_mostrar:
        for s in sensores_a_mostrar:
            renderizar_tarjeta_sensor(s)
    else:
        st.info("No se encontraron sensores con ese filtro. Pruebe con 'HC-SR04', 'ESP32', 'DHT11' o 'Servo'.")'''

NEW_TAB_IMAGENES_Y_3D = '''# ═════════════════════════════════════════════════════════════
#  PESTAÑA 2: GENERADOR & GALERÍA DE IMÁGENES DE SENSORES
# ═════════════════════════════════════════════════════════════
with tab_imagenes:
    st.subheader("📸 Generador & Galería Visual de Componentes Mecatrónicos")
    st.caption("Sección dedicada exclusivamente a generar y visualizar imágenes de alta fidelidad, planos vectoriales de pines (Pinouts) y fichas de taller.")
    
    st.markdown("**⚡ Generación Directa de Sensores:**")
    c_b1, c_b2, c_b3, c_b4 = st.columns(4)
    with c_b1:
        if st.button("💧 Nivel de Flotador (Boya)", use_container_width=True, key="btn_flot"):
            st.session_state["filtro_sensor_manual"] = "flotador"
    with c_b2:
        if st.button("🧪 Calidad del Agua TDS", use_container_width=True, key="btn_tds"):
            st.session_state["filtro_sensor_manual"] = "tds"
    with c_b3:
        if st.button("🦇 Ultrasónico HC-SR04", use_container_width=True, key="btn_hcsr04"):
            st.session_state["filtro_sensor_manual"] = "hc-sr04"
    with c_b4:
        if st.button("🦾 Servomotores SG90 / MG996R", use_container_width=True, key="btn_servos"):
            st.session_state["filtro_sensor_manual"] = "servo"

    col_filtro, col_search = st.columns([1, 2])
    with col_filtro:
        categorias = ["Todos", "Sensores de Nivel y Líquidos", "Sensores Químicos y Calidad de Líquidos", "Sensores de Distancia", "Sensores Ambientales", "Actuadores y Motores", "Controladores de Potencia", "Microcontroladores y SoCs", "Interfaces y Pantallas"]
        cat_sel = st.selectbox("Filtrar por subsistema:", categorias, key="cat_sel_imagenes")
    with col_search:
        valor_def = st.session_state.get("filtro_sensor_manual", "")
        termino = st.text_input("🔍 Escriba el componente para generar su imagen y ficha (ej: flotador, calidad del agua, esp32, dht11):", value=valor_def, key="txt_search_imagenes").strip().lower()
        if termino != valor_def and "filtro_sensor_manual" in st.session_state:
            del st.session_state["filtro_sensor_manual"]
        
    sensores_a_mostrar = []
    for k, v in CATALOGO_SENSORES.items():
        if cat_sel != "Todos" and v.get("categoria") != cat_sel:
            continue
        if termino:
            coincide = (termino in k) or (termino in v["nombre"].lower()) or (termino in v.get("descripcion", "").lower())
            if not coincide:
                continue
        sensores_a_mostrar.append(v)
        
    st.markdown(f"**Imágenes y Fichas Técnicas Activas ({len(sensores_a_mostrar)}):**")
    if sensores_a_mostrar:
        for s in sensores_a_mostrar:
            renderizar_tarjeta_sensor(s)
    else:
        st.info("No se encontraron sensores con ese filtro. Pruebe con 'flotador', 'calidad del agua', 'hc-sr04', 'esp32' o 'servo'.")

# ═════════════════════════════════════════════════════════════
#  PESTAÑA 3: GEMELO DIGITAL (OBJETO FÍSICO REAL ↔ MODELO 3D)
# ═════════════════════════════════════════════════════════════
with tab_gemelo_3d:
    st.subheader("🦾 Gemelo Digital: Objeto Físico Real ↔ Modelo 3D Holográfico")
    st.caption("Laboratorio táctico interactivo permanente. Inspección de tolerancias ISO, despiece 3D sincronizado y comparación directa con el prototipo de taller.")

    col_mod_sel, col_stat = st.columns([2, 1])
    with col_mod_sel:
        modo_3d_sel = st.radio(
            "Seleccionar Mecanismo Mecatrónico:",
            ["🦾 Brazo Robótico Articulado 6-DOF con Pinza (Gripper)", "⚙️ Actuador Robótico Servo-Industrial"],
            horizontal=True,
            key="radio_gemelo_mecanismo"
        )
    with col_stat:
        st.markdown("""
        <div style="background:#0f172a; border:1px solid #0284c7; border-radius:8px; padding:10px 14px; font-size:0.85rem; color:#38bdf8;">
            <b>🛰️ Estado del Gemelo Digital:</b> EN LÍNEA<br>
            <span style="color:#94a3b8;">Rotación Dual Sincronizada · PBR Taller ↔ Holograma</span>
        </div>
        """, unsafe_allow_html=True)

    modelo_key = "brazo" if "Brazo" in modo_3d_sel else "actuador"
    import importlib
    import plantillas.holograma_3d
    importlib.reload(plantillas.holograma_3d)
    from plantillas.holograma_3d import generar_laboratorio_holografico_3d
    raw_lab_html = generar_laboratorio_holografico_3d(modelo_inicial=modelo_key)
    clean_lab_html = raw_lab_html.replace("```html", "").replace("```", "").strip()
    st.components.v1.html(clean_lab_html, height=760, scrolling=False)'''

if OLD_TAB_SENSORES in content:
    content = content.replace(OLD_TAB_SENSORES, NEW_TAB_IMAGENES_Y_3D)
    print("[OK] Tab 2 (Imágenes) and Tab 3 (Gemelo Digital Físico+3D) successfully integrated!")
else:
    print("[ERROR] OLD_TAB_SENSORES not found")

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Syntax check
import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] app.py syntax check PASSED 100%!")
else:
    print("[ERROR] Syntax error in app.py:\n", res.stderr)
