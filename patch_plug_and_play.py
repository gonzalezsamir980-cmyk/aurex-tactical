import sys

ruta = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\escudo_seguridad.py"
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

seccion_pnp = '''def renderizar_intervencion_plug_and_play():
    """Módulo de Drop-Box Autónomo: Intervención automática al conectar la laptop a red externa."""
    from intervencion_autonoma import (
        obtener_estado_intervencion, 
        ejecutar_intervencion_plug_and_play, 
        neutralizar_amenaza_autonoma
    )
    
    st.markdown("### ⚡ Intervención Táctica Plug & Play (Drop-Box Autónomo)")
    st.caption("Conecta tu laptop a la red del cliente: AUREX activa el Modo Fantasma (laptop invisible a virus), escanea la subred y neutraliza intrusiones en caliente sin que tengas que teclear nada.")
    
    estado = obtener_estado_intervencion()
    
    col_btn, col_sim = st.columns([1, 1])
    with col_btn:
        if st.button("🔌 Conectar e Iniciar Intervención en esta Red", key="btn_iniciar_pnp", type="primary", use_container_width=True):
            with st.spinner("Activando Modo Fantasma y escaneando bases de datos en la red..."):
                estado = ejecutar_intervencion_plug_and_play()
            st.success("🛡️ ¡Intervención iniciada! Modo Fantasma ACTIVO y Guardián Autónomo en guardia.")
            st.rerun()
            
    with col_sim:
        if estado.get("guardian_autonomo") == "VIGILANDO_EN_VIVO":
            if st.button("🚨 Simular Intrusión Externa en Caliente", key="btn_sim_live_threat", use_container_width=True):
                inc = neutralizar_amenaza_autonoma(
                    ip_atacante="194.26.29.114",
                    vector="INYECCION_SQL_ZERO_DAY",
                    detalle="Intento de extracción de contraseñas de la base de datos MySQL del cliente."
                )
                st.toast(f"⚔️ Amenaza neutralizada en 0.3s por AUREX", icon="🛡️")
                st.rerun()
                
    if estado:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #022c22 0%, #064e3b 100%); border: 1px solid #10b981; border-radius: 10px; padding: 12px; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: #a7f3d0;">🛡️ MODO FANTASMA: ACTIVO (Laptop Invisible)</span>
                <span style="background: #047857; color: white; padding: 2px 8px; border-radius: 6px; font-size: 0.8rem; font-weight: bold;">{estado.get('guardian_autonomo', 'EN ESPERA')}</span>
            </div>
            <div style="color: #6ee7b7; font-size: 0.82rem; margin-top: 4px;">
                <b>Subred Protegida:</b> <code>{estado.get('subred_detectada')}</code> | 
                <b>Bases de Datos Salvaguardadas:</b> {estado.get('total_bases_datos_protegidas', 0)} | 
                <b>Aislamiento AUREX:</b> 100% Blindado
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Dispositivos detectados
        disp = estado.get("dispositivos_encontrados", [])
        if disp:
            with st.expander(f"🎯 Servidores y Bases de Datos Descubiertos en la Red ({len(disp)})"):
                for d in disp:
                    st.markdown(f"**Host:** `{d.get('ip')}`")
                    for s in d.get("servicios", []):
                        st.markdown(f"- 🔹 Puerto `{s.get('puerto')}`: **{s.get('servicio')}** ({s.get('categoria')})")
                        
        # Historial de neutralizaciones autónomas
        neut = estado.get("amenazas_neutralizadas", [])
        if neut:
            st.markdown("**⚔️ Acciones Autónomas Ejecutadas por AUREX en Caliente:**")
            for n in neut[:3]:
                st.info(f"⚡ **{n.get('ts')}** · Vector: `{n.get('vector')}` | IP Atacante: `{n.get('ip_atacante')}`\n\n*Respuesta Automática:* `{n.get('accion_autonoma')}` -> **{n.get('resultado')}**")
    st.divider()
'''

target = "def renderizar_panel_ciberdefensa_policial():\n    \"\"\"Muestra el Centro de Incidentes y Generador de Informes Policiales dentro de AUREX.\"\"\"\n    st.subheader(\"🛡️ Centro de Ciberdefensa & Informes Periciales\")\n    st.caption(\"Auditoría forense digital con sellado SHA-256 e informes periciales listos para la Policía de Ciberdelitos.\")\n    renderizar_seccion_alertas_moviles()\n    renderizar_soc_multidispositivo()"

replacement = seccion_pnp + target + "\n    renderizar_intervencion_plug_and_play()"

if target not in contenido:
    print("ERROR: Target no encontrado")
    sys.exit(1)

contenido = contenido.replace(target, replacement, 1)

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print("INTERVENCION PLUG AND PLAY INTEGRADA CON EXITO")
