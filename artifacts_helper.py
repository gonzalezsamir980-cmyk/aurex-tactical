"""
MÓDULO DE ARTIFACTS Y VISUALIZADOR DE CÓDIGO/DASHBOARDS AL ESTILO CLAUDE - AUREX
Permite renderizar:
- Dashboards interactivos HTML/JS en vivo dentro de la aplicación.
- Bloques de código reales de Arduino (.ino), ESP32 y Python listos para compilar.
- Tarjetas técnicas de sensores con imágenes reales y diagramas de conexión.
"""

import re
import streamlit as st
from sensores_data import buscar_sensores_en_texto, CATALOGO_SENSORES

def extraer_texto_hablado(texto_completo: str) -> str:
    """
    Elimina los bloques de código (```...```) para que la síntesis de voz masculina
    solo lea la explicación técnica natural y no se trabe dictando código crudo.
    """
    sin_codigo = re.sub(r'```[\s\S]*?```', '', texto_completo)
    lineas = [l.strip() for l in sin_codigo.split('\n') if l.strip()]
    texto_limpio = " ".join(lineas)
    
    if not texto_limpio.strip():
        return "Jefe, he generado el código y la arquitectura técnica completa en la pantalla. Puede revisarla y probarla a continuación."
    return texto_limpio

def extraer_bloques_codigo(texto: str):
    """
    Extrae todos los bloques de código markdown del mensaje.
    Soporta saltos de línea Windows (\r\n) y Unix (\n).
    Retorna una lista de tuplas: (lenguaje, codigo_str)
    """
    patron = r'```([a-zA-Z0-9_\-\+]*)[ \t]*\r?\n([\s\S]*?)```'
    coincidencias = re.findall(patron, texto)
    bloques = []
    for lang, code in coincidencias:
        lang_clean = lang.strip().lower()
        if not lang_clean:
            lang_clean = "texto"
        bloques.append((lang_clean, code.strip()))
    return bloques

def renderizar_tarjeta_sensor(sensor: dict):
    """
    Despliega una ficha visual táctica de un sensor con foto, pines y datos técnicos.
    """
    pines_html = "".join([
        f'<span style="background:#1e293b; color:{color}; padding:3px 8px; border-radius:4px; font-weight:bold; font-size:0.8rem; margin-right:6px; border:1px solid #334155;">'
        f'{pin}: <span style="color:#e2e8f0; font-weight:normal;">{desc}</span></span> '
        for pin, desc, color in sensor.get("pines", [])
    ])
    
    html = f"""
    <div style="
        background: linear-gradient(135deg, #0b1329 0%, #030712 100%);
        border: 1px solid #38bdf8;
        border-radius: 14px;
        padding: 16px;
        margin: 14px 0;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15);
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:8px; margin-bottom:12px;">
            <div>
                <span style="font-size:0.75rem; letter-spacing:1px; color:#38bdf8; text-transform:uppercase; font-weight:bold;">
                    {sensor.get('categoria', 'Componente')} · FICHA TÉCNICA
                </span>
                <h4 style="margin:2px 0 0 0; color:#f8fafc; font-size:1.15rem;">{sensor.get('nombre')}</h4>
            </div>
            <span style="background:#0284c7; color:#fff; font-size:0.75rem; padding:3px 8px; border-radius:12px; font-weight:bold;">
                {sensor.get('voltaje', '5V')}
            </span>
        </div>
        
        <div style="display:flex; gap:16px; flex-wrap:wrap;">
            <div style="flex:1; min-width:200px; max-width:260px; text-align:center; background:#0f172a; padding:10px; border-radius:10px; border:1px solid #1e293b;">
                {sensor.get('svg_diagrama', '')}
                <div style="font-size:0.72rem; color:#38bdf8; margin-top:5px; font-weight:bold; letter-spacing:0.5px;">📐 BLUEPRINT TÁCTICO & PINES</div>
                
            </div>
            
            <div style="flex:2; min-width:260px; font-size:0.9rem; line-height:1.5;">
                <p style="margin:0 0 8px 0; color:#cbd5e1;">{sensor.get('descripcion')}</p>
                
                <div style="margin:8px 0;">
                    <div style="font-size:0.75rem; color:#38bdf8; font-weight:bold; margin-bottom:4px;">🔌 MAPA DE PINES (PINOUT):</div>
                    <div style="display:flex; flex-wrap:wrap; gap:4px;">
                        {pines_html}
                    </div>
                </div>
                
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:10px; font-size:0.8rem; background:#0f172a; padding:8px 10px; border-radius:6px;">
                    <div><b style="color:#94a3b8;">Consumo:</b> <span style="color:#f1f5f9;">{sensor.get('consumo', 'N/D')}</span></div>
                    <div><b style="color:#94a3b8;">Protocolo:</b> <span style="color:#f1f5f9;">{sensor.get('protocolo', 'Digital')}</span></div>
                    <div style="grid-column: span 2;"><b style="color:#94a3b8;">Rango:</b> <span style="color:#f1f5f9;">{sensor.get('rango', 'N/D')}</span></div>
                </div>
                
                <div style="margin-top:10px; background:#451a03; border-left:3px solid #f59e0b; padding:6px 10px; border-radius:4px; font-size:0.78rem; color:#fde68a;">
                    ⚠️ <b>Directiva de Taller:</b> {sensor.get('advertencia')}
                </div>
            </div>
        </div>
    </div>
    """
    clean_html = "\n".join([line.strip() for line in html.split("\n") if line.strip()])
    st.markdown(clean_html, unsafe_allow_html=True)

def renderizar_artifacts_interactivos(texto: str, element_key_prefix: str = "art"):
    """
    Inspecciona si el texto contiene Dashboard HTML o código Arduino/ESP32
    y despliega los Artifacts interactivos de Claude en Streamlit.
    """
    bloques = extraer_bloques_codigo(texto)
    
    # 1. Detectar si hay sensores para mostrar sus fichas técnicas
    texto_l = texto.lower()
    es_seguridad_o_chat = any(k in texto_l for k in ["contraorden", "ciberdefensa", "firewall", "ip atacante", "incidente", "auditoría", "auditoria", "acceso concedido", "desbloquear"])
    if not es_seguridad_o_chat:
        sensores_detectados = buscar_sensores_en_texto(texto, permitir_fallback=False)
        # Solo mostrar sensores reales del catálogo de mecatrónica (nunca falsos procedimentales en el chat)
        sensores_reales = [s for s in sensores_detectados if s.get("categoria") != "Hardware y Componentes Tcticos Solicitados" and s.get("categoria") != "Hardware y Componentes Tácticos Solicitados"]
        if sensores_reales:
            st.markdown("##### 🔌 Fichas Visuales y Diagramas de Componentes")
            for s in sensores_reales:
                renderizar_tarjeta_sensor(s)

    # 2. Renderizar bloques de código especiales
    for i, (lang, codigo) in enumerate(bloques):
        # Caso A: Dashboard Web en HTML/JS (Artifact interactivo al estilo Claude)
        if lang in ["html", "htm"] or ("<html" in codigo.lower() or "<!doctype" in codigo.lower() or "canvas" in codigo.lower()):
            st.markdown(f"""
            <div style="background:#0f172a; border:2px solid #818cf8; border-radius:12px; padding:12px 16px; margin:14px 0 6px 0;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:1.3rem;">🚀</span>
                        <div>
                            <b style="color:#c7d2fe; font-size:1rem;">ARTIFACT TÁCTICO: DASHBOARD INTERACTIVO</b>
                            <div style="font-size:0.75rem; color:#94a3b8;">Vista en vivo interactiva impulsada por el motor de Claude Artifacts de AUREX</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            tab_vista, tab_codigo = st.tabs(["👁️ Vista Previa en Vivo (Interactivo)", "💻 Código Fuente HTML/JS"])
            with tab_vista:
                # Inyectar estilos responsive mínimos si no los tiene
                html_render = codigo
                st.components.v1.html(html_render, height=520, scrolling=True)
            with tab_codigo:
                st.code(codigo, language="html")
                st.download_button(
                    label="💾 Descargar Dashboard (HTML)",
                    data=codigo,
                    file_name=f"dashboard_aurex_{i+1}.html",
                    mime="text/html",
                    key=f"{element_key_prefix}_dl_html_{i}"
                )
                
        # Caso B: Código de Arduino / ESP32 (.ino / C++)
        elif lang in ["cpp", "c++", "c", "arduino", "ino"] or ("void setup" in codigo or "pinMode" in codigo):
            placa = "ESP32 / Arduino"
            if "esp32" in codigo.lower() or "wifi.h" in codigo.lower():
                placa = "ESP32 SoC (3.3V)"
            elif "uno" in codigo.lower() or "atmega" in codigo.lower():
                placa = "Arduino Uno / Nano (5V)"
                
            st.markdown(f"""
            <div style="background:#091e2b; border:1px solid #0284c7; border-radius:10px; padding:10px 14px; margin:12px 0 4px 0;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="color:#38bdf8; font-weight:bold; font-size:0.9rem;">
                        ⚡ CÓDIGO EMBEBIDO LISTO PARA COMPILAR · <code>{placa}</code>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.code(codigo, language="cpp")
            st.download_button(
                label="📥 Descargar Sketch (.ino) para Arduino IDE",
                data=codigo,
                file_name=f"proyecto_aurex_{i+1}.ino",
                mime="text/plain",
                key=f"{element_key_prefix}_dl_ino_{i}"
            )
            
        # Caso C: Scripts en Python
        elif lang in ["python", "py"]:
            st.markdown(f"""
            <div style="background:#0f172a; border:1px solid #10b981; border-radius:10px; padding:10px 14px; margin:12px 0 4px 0;">
                <span style="color:#34d399; font-weight:bold; font-size:0.9rem;">🐍 SCRIPT PYTHON DE TELEMETRÍA</span>
            </div>
            """, unsafe_allow_html=True)
            st.code(codigo, language="python")
            st.download_button(
                label="📥 Descargar Script (.py)",
                data=codigo,
                file_name=f"script_aurex_{i+1}.py",
                mime="text/x-python",
                key=f"{element_key_prefix}_dl_py_{i}"
            )
