import sys

ruta = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\escudo_seguridad.py"
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

soc_funcion = '''def renderizar_soc_multidispositivo():
    """Centro de Monitoreo y Ciberdefensa de Empresas y Dispositivos de Clientes."""
    from soc_tactico import obtener_nodos, emitir_orden_defensa, registrar_nodo_nuevo, reportar_incidente_remoto
    st.markdown("### 🌐 Red de Dispositivos y Empresas Protegidas (SOC Remoto)")
    st.caption("AUREX actúa como escudo centralizado Zero-Trust: defiende clientes y bases de datos sin exponer los datos del taller.")
    
    nodos = obtener_nodos()
    
    # Laboratorio de Simulación Táctica
    with st.expander("🧪 Simular Ataques en Tiempo Real a Clientes"):
        st.markdown("Pon a prueba cómo reacciona AUREX y tu celular cuando un cliente externo está sufriendo un ataque:")
        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            if st.button("🔥 Simular Ataque SQL a Base de Datos", key="btn_sim_sql"):
                from centinela_cliente import simular_ataque_contra_base_de_datos
                simular_ataque_contra_base_de_datos(ip_atacante="185.220.101.5", vector="SQL_INJECTION_BRUTEFORCE")
                st.toast("🚨 ¡Alerta de ataque despachada a tu celular y registrada en el SOC!", icon="⚠️")
                st.rerun()
        with col_s2:
            if st.button("⚡ Simular Intento de Ransomware a Terminal", key="btn_sim_nmap"):
                reportar_incidente_remoto(
                    id_nodo="WS-CONTABILIDAD-02",
                    tipo_ataque="ESC_PUERTOS_Y_RANSOMWARE_SUSPECT",
                    ip_atacante="45.154.255.89",
                    detalle="Escaneo masivo de puertos e intento de ejecución de script no firmado.",
                    token_seguridad=nodos.get("WS-CONTABILIDAD-02", {}).get("token_seguridad", "")
                )
                st.toast("🚨 Alerta despachada a tu celular", icon="🚨")
                st.rerun()

    # Mostrar lista de nodos protegidos
    for id_nodo, info in nodos.items():
        estado = info.get("estado", "SEGURO")
        color_borde = "#ef4444" if estado == "BAJO_ATAQUE" else "#10b981"
        icono_estado = "🔴" if estado == "BAJO_ATAQUE" else "🟢"
        
        with st.container():
            st.markdown(f"""
            <div style="border: 2px solid {color_borde}; border-radius: 10px; padding: 12px; margin-bottom: 12px; background: rgba(15, 23, 42, 0.65);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; font-size: 1.05rem; color: #f8fafc;">{icono_estado} {info.get('nombre')}</span>
                    <span style="font-size: 0.8rem; background: {'#7f1d1d' if estado == 'BAJO_ATAQUE' else '#064e3b'}; padding: 3px 8px; border-radius: 6px; color: {'#fca5a5' if estado == 'BAJO_ATAQUE' else '#6ee7b7'}; font-weight: bold;">{estado}</span>
                </div>
                <div style="font-size: 0.82rem; color: #94a3b8; margin-top: 4px;">
                    <b>Tipo:</b> {info.get('tipo')} | <b>IP:</b> {info.get('ip_local')} | <b>ID:</b> <code>{id_nodo}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if estado == "BAJO_ATAQUE":
                amenaza = info.get("amenaza_actual", {})
                st.error(f"🚨 **¡AMENAZA EN CURSO!** Vector: `{amenaza.get('tipo')}` | IP Atacante: `{amenaza.get('ip_atacante')}`\\n\\n*Detalle:* {amenaza.get('detalle')}")
                
                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1:
                    if st.button("🚫 Bloquear IP en Cliente", key=f"btn_block_{id_nodo}"):
                        emitir_orden_defensa(id_nodo, "BLOQUEAR_IP", {"ip": amenaza.get("ip_atacante")})
                        st.success(f"🛡️ Contraorden despachada: IP {amenaza.get('ip_atacante')} bloqueada.")
                with col_c2:
                    if st.button("🔒 Congelar BD (Modo Seguro)", key=f"btn_freeze_{id_nodo}"):
                        emitir_orden_defensa(id_nodo, "CONGELAR_BD")
                        st.warning("💾 Base de datos puesta en modo READ ONLY.")
                with col_c3:
                    if st.button("🟢 Restaurar a Seguro", key=f"btn_restore_{id_nodo}"):
                        emitir_orden_defensa(id_nodo, "RESTAURAR_SEGURO")
                        st.toast("✅ Nodo restablecido a estado seguro.", icon="🟢")
                        st.rerun()
                        
    st.divider()
'''

target = "def renderizar_panel_ciberdefensa_policial():\n    \"\"\"Muestra el Centro de Incidentes y Generador de Informes Policiales dentro de AUREX.\"\"\"\n    st.subheader(\"🛡️ Centro de Ciberdefensa & Informes Periciales\")\n    st.caption(\"Auditoría forense digital con sellado SHA-256 e informes periciales listos para la Policía de Ciberdelitos.\")\n    renderizar_seccion_alertas_moviles()"

replacement = soc_funcion + target + "\n    renderizar_soc_multidispositivo()"

if target not in contenido:
    print("ERROR: Target no encontrado")
    sys.exit(1)

contenido = contenido.replace(target, replacement, 1)

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print("SOC MULTIDISPOSITIVO INTEGRADO CON EXITO")
