import sys

ruta = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\escudo_seguridad.py"
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

target = '''    with tab_ntfy:
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
            st.link_button("🌐 Abrir Canal en Navegador", f"https://ntfy.sh/{canal}", use_container_width=True)'''

replacement = '''    with tab_ntfy:
        canal = cfg.get("ntfy_canal_seguro", "aurex_taller_jefe_a9e0603416")
        url_canal = f"https://ntfy.sh/{canal}"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={url_canal}"
        
        col_info, col_qr = st.columns([2, 1])
        with col_info:
            st.markdown(f"""
            **Tu Canal de Alerta:** `{canal}`  
            **Enlace Directo:** [{url_canal}]({url_canal})
            
            **Cómo activarlo en tu celular en 10 segundos:**
            - **Opción A (Con App gratuita):** Instala **ntfy** (Play Store o App Store), dale al botón **`+`**, escribe `{canal}` y toca Suscribirse.
            - **Opción B (Sin instalar nada):** Escanea el código QR de la derecha con tu cámara y toca *Suscribirse / Permitir notificaciones*.
            """)
        with col_qr:
            st.image(qr_url, caption="Escanea con tu cámara", width=160)
            
        col_ntfy1, col_ntfy2 = st.columns([1, 1])
        with col_ntfy1:
            if st.button("🚨 Probar Sirena en mi Teléfono Ahora", key="btn_test_ntfy", type="primary", use_container_width=True):
                despachar_alerta_movil_asincrona(
                    tipo_evento="PRUEBA_SISTEMA_TACTICO",
                    detalle="El Jefe Samir ha disparado una prueba de sirena desde AUREX.",
                    ip="127.0.0.1",
                    id_incidente="TEST-TACTICO-01"
                )
                st.success("📡 ¡Sirena táctica despachada a tu celular!")
                
        with col_ntfy2:
            st.link_button("🌐 Abrir Canal en Navegador", url_canal, use_container_width=True)'''

if target not in contenido:
    print("ERROR: target no encontrado")
    sys.exit(1)

contenido = contenido.replace(target, replacement, 1)

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print("ACTUALIZACION DE CODIGO QR Y GUIA APLICADA")
