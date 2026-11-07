import sys

ruta = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\escudo_seguridad.py"
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

seccion_movil = '''def renderizar_seccion_alertas_moviles():
    """Panel de configuración y prueba de alertas tácticas al teléfono del Jefe."""
    from alertas_movil import obtener_config_alertas, guardar_config_alertas, despachar_alerta_movil_asincrona
    cfg = obtener_config_alertas()
    
    st.markdown("### 📲 Alertas en tu Teléfono (ntfy & Telegram)")
    st.markdown("""
    Recibe alertas instantáneas en tu celular con sonido de sirena cuando alguien intente tocar AUREX o meter una clave incorrecta, incluso si estás fuera del taller.
    """)
    
    tab_ntfy, tab_telegram = st.tabs(["⚡ Notificación Push Directa (ntfy)", "🤖 Bot de Telegram"])
    
    with tab_ntfy:
        canal = cfg.get("ntfy_canal_seguro", "")
        st.markdown(f"""
        **Canal Táctico Privado Cifrado:**
        `https://ntfy.sh/{canal}`
        
        **Instrucciones rápidas para tu celular:**
        1. Descarga la app gratuita **ntfy** en tu teléfono (Play Store en Android o App Store en iPhone).
        2. Toca el botón **`+` (Suscribirse a tema)** y pega tu canal:
           `{canal}`
        3. ¡Listo! No requiere crear cuenta ni registrar correo.
        """)
        
        col_ntfy1, col_ntfy2 = st.columns([1, 1])
        with col_ntfy1:
            if st.button("🚨 Probar Sirena en mi Teléfono Ahora", key="btn_test_ntfy", type="primary", use_container_width=True):
                despachar_alerta_movil_asincrona(
                    tipo_evento="PRUEBA_SISTEMA_TACTICO",
                    detalle="El Jefe Samir ha disparado una prueba de alerta móvil desde el taller.",
                    ip="127.0.0.1",
                    id_incidente="TEST-TACTICO-01"
                )
                st.success("📡 Señal de sirena enviada a tu canal ntfy.")
                
        with col_ntfy2:
            st.link_button("🌐 Abrir Canal en Navegador", f"https://ntfy.sh/{canal}", use_container_width=True)
            
    with tab_telegram:
        st.caption("Conecta tu bot de Telegram personal para recibir informes de seguridad enriquecidos.")
        with st.form("form_config_tg"):
            t_token = st.text_input("Token de Bot de Telegram (de @BotFather):", value=cfg.get("telegram_bot_token", ""), type="password")
            t_chat = st.text_input("Tu Chat ID de Telegram:", value=cfg.get("telegram_chat_id", ""))
            t_activo = st.checkbox("Activar Alertas por Telegram", value=cfg.get("telegram_activo", False))
            
            btn_guardar_tg = st.form_submit_button("💾 Guardar Configuración Telegram", use_container_width=True)
            if btn_guardar_tg:
                cfg["telegram_bot_token"] = t_token.strip()
                cfg["telegram_chat_id"] = t_chat.strip()
                cfg["telegram_activo"] = t_activo
                guardar_config_alertas(cfg)
                st.toast("✅ Configuración de Telegram guardada", icon="💾")
                st.rerun()
                
        if cfg.get("telegram_activo") and cfg.get("telegram_bot_token") and cfg.get("telegram_chat_id"):
            if st.button("🚨 Probar Mensaje en Telegram", key="btn_test_tg", use_container_width=True):
                despachar_alerta_movil_asincrona(
                    tipo_evento="PRUEBA_TELEGRAM",
                    detalle="Prueba de enlace táctico con Telegram del Jefe completada.",
                    ip="127.0.0.1",
                    id_incidente="TEST-TG-01"
                )
                st.success("📡 Mensaje táctico de prueba despachado a Telegram.")
    st.divider()
'''

target = "def renderizar_panel_ciberdefensa_policial():\n    \"\"\"Muestra el Centro de Incidentes y Generador de Informes Policiales dentro de AUREX.\"\"\"\n    st.subheader(\"🛡️ Centro de Ciberdefensa & Informes Periciales\")\n    st.caption(\"Auditoría forense digital con sellado SHA-256 e informes periciales listos para la Policía de Ciberdelitos.\")"

replacement = seccion_movil + target + "\n    renderizar_seccion_alertas_moviles()"

if target not in contenido:
    print("ERROR: Target no encontrado")
    sys.exit(1)

contenido = contenido.replace(target, replacement, 1)

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print("PANEL MOVIL INTEGRADO CON EXITO")
