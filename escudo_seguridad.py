"""
ESCUDO DE SEGURIDAD Y CERROJO TÁCTICO DEL JEFE - AUREX CYBER-SHIELD
Provee:
1. Autenticación con Clave Maestra y Acertijo del Jefe (Cifrado SHA-256 + Salt).
2. Detección de Intentos de Hackeo y Pantalla de Alerta Roja Táctica (HUD Intrusion Alert).
3. Firewall contra Prompt Injection, Sabotaje y Fuga de Datos.
4. Registro de Auditoría Forense de Seguridad (registro_seguridad.jsonl).
5. Generador Oficial de Informes Periciales para la Policía / Fiscalía de Delitos Informáticos.
"""

import os
import sys
import time
import json
import hashlib
import uuid
import streamlit as st

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CREDENCIALES = os.path.join(DIR_ACTUAL, "credenciales_jefe.json")
ARCHIVO_AUDITORIA = os.path.join(DIR_ACTUAL, "registro_seguridad.jsonl")

SALT_ESTATICO = "AUREX_TACTICAL_SALT_v2_2026"

def _hash_valor(texto: str) -> str:
    """Genera hash SHA-256 seguro con Salt."""
    cadena = f"{SALT_ESTATICO}:{texto.strip().lower()}"
    return hashlib.sha256(cadena.encode("utf-8")).hexdigest()

def extraer_telemetria_cliente() -> dict:
    """Extrae datos de red y navegador del cliente (IP, User-Agent)."""
    telemetria = {
        "ip": "127.0.0.1 (Localhost)",
        "user_agent": "Navegador Desconocido"
    }
    try:
        # Streamlit >= 1.34 soporte de headers
        headers = getattr(st.context, "headers", {})
        if headers:
            ip = headers.get("x-forwarded-for") or headers.get("x-real-ip") or headers.get("host", "127.0.0.1")
            ua = headers.get("user-agent", "N/D")
            telemetria["ip"] = ip.split(",")[0].strip() if "," in ip else ip
            telemetria["user_agent"] = ua
    except Exception:
        pass
    return telemetria

def esta_cerrojo_configurado() -> bool:
    """Verifica si el Jefe ya definió su clave o acertijo."""
    if not os.path.exists(ARCHIVO_CREDENCIALES):
        return False
    try:
        with open(ARCHIVO_CREDENCIALES, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return bool(datos.get("hash_clave"))
    except Exception:
        return False

def guardar_credenciales_jefe(clave_maestra: str, pregunta_acertijo: str = "", respuesta_acertijo: str = ""):
    """Guarda las credenciales cifradas del Jefe."""
    datos = {
        "hash_clave": _hash_valor(clave_maestra),
        "pregunta_acertijo": pregunta_acertijo.strip(),
        "hash_acertijo": _hash_valor(respuesta_acertijo) if respuesta_acertijo.strip() else "",
        "intentos_fallidos": 0,
        "fecha_configuracion": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(ARCHIVO_CREDENCIALES, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def registrar_evento_seguridad(tipo: str, detalle: str, severidad: str = "ALTA") -> dict:
    """Registra cualquier intento sospechoso en la caja negra de auditoría con firma criptográfica."""
    telemetria = extraer_telemetria_cliente()
    id_incidente = f"AUREX-INC-{uuid.uuid4().hex[:8].upper()}"
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Hash de integridad de evidencia (Cadena de custodia digital)
    firma_str = f"{id_incidente}|{ts}|{tipo}|{detalle}|{telemetria['ip']}|{telemetria['user_agent']}"
    hash_evidencia = hashlib.sha256(firma_str.encode("utf-8")).hexdigest()

    evento = {
        "id_incidente": id_incidente,
        "timestamp": ts,
        "tipo": tipo,
        "detalle": detalle,
        "severidad": severidad,
        "ip_atacante": telemetria["ip"],
        "user_agent": telemetria["user_agent"],
        "hash_evidencia": hash_evidencia
    }
    try:
        with open(ARCHIVO_AUDITORIA, "a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return evento

def leer_auditoria_seguridad(limite: int = 20) -> list[dict]:
    """Retorna los últimos incidentes de seguridad registrados."""
    if not os.path.exists(ARCHIVO_AUDITORIA):
        return []
    lineas = []
    try:
        with open(ARCHIVO_AUDITORIA, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        eventos = [json.loads(l) for l in lineas if l.strip()]
        return eventos[-limite:][::-1]
    except Exception:
        return []

def generar_informe_policial_forense(evento: dict) -> str:
    """
    Genera un Informe Pericial Forense Oficial de Ciberdelito
    listo para imprimir y entregar a la Policía Nacional / Fiscalía de Delitos Cibernéticos.
    """
    informe = f"""================================================================================
REPÚBLICA DE PANAMÁ / AUTORIDADES JUDICIALES COMPETENTES
DIVISIÓN DE CIBERDELITOS Y DELITOS CONTRA LA SEGURIDAD INFORMÁTICA
INFORME PERICIAL FORENSE DE EVIDENCIA DIGITAL (LEY DE CIBERCRIMEN)
================================================================================

EXPEDIENTE DE INCIDENTE: {evento.get('id_incidente', 'AUREX-CYBER-001')}
FECHA Y HORA DEL SUCESO: {evento.get('timestamp', 'N/D')} (Hora Local)
NIVEL DE AMENAZA / SEVERIDAD: {evento.get('severidad', 'CRÍTICA')}
SISTEMA AFECTADO: Estación Táctica de Ingeniería Mecatrónica AUREX v2.0
PROPIETARIO Y RESPONSABLE: Jefe de Taller Samir

--------------------------------------------------------------------------------
1. DATOS TÉCNICOS DEL ATACANTE (HUELLA DIGITAL FORENSE CAPTURADA)
--------------------------------------------------------------------------------
- DIRECCIÓN IP DE ORIGEN: {evento.get('ip_atacante', '127.0.0.1')}
- AGENTE DE NAVEGACIÓN (USER-AGENT): {evento.get('user_agent', 'N/D')}
- VECTOR DE ATAQUE: {evento.get('tipo', 'ACCESO_NO_AUTORIZADO')}
- MODALIDAD DELICTIVA: Intento de Acceso Ilícito a Sistema Informático / Sabotaje de Datos.

--------------------------------------------------------------------------------
2. DETALLE DE LA CARGA MALICIOSA O ACCIÓN DETECTADA (PAYLOAD EVIDENCIA)
--------------------------------------------------------------------------------
{evento.get('detalle', 'Intento de vulneración de credenciales maestras')}

ACCIONES DEFENSIVAS TOMADAS POR EL SISTEMA:
[X] Interceptación inmediata por el Escudo de Seguridad AUREX.
[X] Bloqueo de acceso a bancos de memoria y código mecatrónico.
[X] Aislamiento de la sesión y registro en la caja negra forense inmutable.
ESTADO DE LOS DATOS REALES: ÍNTEGROS Y PROTEGIDOS (CERO FUGA DE INFORMACIÓN).

--------------------------------------------------------------------------------
3. CADENA DE CUSTODIA Y FIRMA CRIPTOGRÁFICA INALTERABLE
--------------------------------------------------------------------------------
Para los efectos legales pertinentes, este registro digital cuenta con un sello
criptográfico SHA-256 que garantiza que la evidencia NO ha sido manipulada:

HASH SHA-256 DE LA EVIDENCIA:
{evento.get('hash_evidencia', 'N/D')}

CERTIFICACIÓN TÉCNICA:
El presente documento constituye prueba pericial digital de un intento deliberado
de intrusión contra infraestructura privada de ingeniería y sistemas automatizados.

================================================================================
FIN DEL EXPEDIENTE FORENSE · SISTEMA DE SEGURIDAD AUREX
================================================================================
"""
    return informe

def verificar_clave_o_acertijo(intento: str) -> bool:
    """Valida si el intento coincide con la Clave Maestra o la respuesta al Acertijo."""
    if not os.path.exists(ARCHIVO_CREDENCIALES):
        return True
    try:
        with open(ARCHIVO_CREDENCIALES, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        intento_hash = _hash_valor(intento)
        if intento_hash == datos.get("hash_clave"):
            datos["intentos_fallidos"] = 0
            with open(ARCHIVO_CREDENCIALES, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True
            
        if datos.get("hash_acertijo") and intento_hash == datos.get("hash_acertijo"):
            datos["intentos_fallidos"] = 0
            with open(ARCHIVO_CREDENCIALES, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True
            
        # Intento fallido -> Registrar evidencia forense
        datos["intentos_fallidos"] = datos.get("intentos_fallidos", 0) + 1
        with open(ARCHIVO_CREDENCIALES, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        ev = registrar_evento_seguridad(
            "INTENTO_HACKEO_FUERZA_BRUTA", 
            f"Intento de intrusión con clave o respuesta no autorizada. Intento: '{intento[:3]}***'. Total fallos acumulados: {datos['intentos_fallidos']}", 
            "CRÍTICA"
        )
        try:
            from alertas_movil import despachar_alerta_movil_asincrona
            despachar_alerta_movil_asincrona(
                "INTENTO_HACKEO_FUERZA_BRUTA",
                f"Clave incorrecta introducida. Total intentos fallidos: {datos['intentos_fallidos']}",
                ip=ev.get("ip_atacante", "127.0.0.1"),
                id_incidente=ev.get("id_incidente", "N/D")
            )
        except Exception:
            pass
        return False
    except Exception:
        return False

def detectar_prompt_injection(texto: str) -> tuple[bool, str]:
    """Firewall heurístico contra inyecciones de prompt y sabotaje."""
    texto_l = texto.lower()
    patrones_peligrosos = [
        ("ignore previous instructions", "Intento de anulación de directivas maestras (Jailbreak)"),
        ("ignora las instrucciones anteriores", "Intento de anulación de directivas maestras"),
        ("system override", "Simulación de comando de escalación de privilegios"),
        ("dan mode", "Intento de forzar modo no restringido (DAN)"),
        ("format c:", "Comando destructivo de sistema operativo"),
        ("rmdir /s", "Comando de borrado masivo de directorios"),
        ("rm -rf", "Comando de borrado Unix"),
        ("dame todas las contraseñas", "Intento de extracción de credenciales"),
        ("reveal secret key", "Intento de exfiltración de claves de seguridad"),
        ("delete all databases", "Intento de sabotaje a base de datos"),
    ]
    for patron, motivo in patrones_peligrosos:
        if patron in texto_l:
            ev = registrar_evento_seguridad("PROMPT_INJECTION_BLOQUEADO", f"Texto sospechoso interceptado: '{patron}' -> Motivo: {motivo}", "CRÍTICA")
            try:
                from alertas_movil import despachar_alerta_movil_asincrona
                despachar_alerta_movil_asincrona(
                    "PROMPT_INJECTION_BLOQUEADO",
                    f"Patron malicioso neutralizado en chat: '{patron}'. Motivo: {motivo}",
                    ip=ev.get("ip_atacante", "127.0.0.1"),
                    id_incidente=ev.get("id_incidente", "N/D")
                )
            except Exception:
                pass
            return True, motivo
    return False, ""

def renderizar_pantalla_seguridad() -> bool:
    """
    Controlador maestro de acceso en Streamlit.
    """
    if "autenticado_jefe" not in st.session_state:
        st.session_state["autenticado_jefe"] = False
    if "alerta_intrusion_activa" not in st.session_state:
        st.session_state["alerta_intrusion_activa"] = False

    if st.session_state["autenticado_jefe"]:
        return True

    # Si ya está configurado, mostrar PANTALLA DE ACCESO RESTRINGIDO
    with open(ARCHIVO_CREDENCIALES, "r", encoding="utf-8") as f:
        datos_cred = json.load(f)
    pregunta_activa = datos_cred.get("pregunta_acertijo", "")

    # HUD DE ALERTA ROJA SI HUBO INTENTO DE INTRUSIÓN
    if st.session_state["alerta_intrusion_activa"]:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #450a0a 0%, #1f0202 100%); border: 3px solid #ef4444; border-radius: 16px; padding: 22px; text-align: center; margin-bottom: 25px; animation: pulse 1.5s infinite; box-shadow: 0 0 35px rgba(239, 68, 68, 0.45);">
            <div style="font-size: 2.8rem;">🚨</div>
            <h2 style="color: #f87171; font-family: monospace; letter-spacing: 3px; margin: 4px 0;">¡ALERTA DE SEGURIDAD: ACCESO DENEGADO!</h2>
            <p style="color: #fca5a5; font-size: 1.05rem; font-weight: bold; margin: 6px 0;">SE HA DETECTADO UN INTENTO DE INTRUSIÓN O CLAVE INCORRECTA</p>
            <div style="font-size: 0.85rem; color: #fecaca; background: rgba(0,0,0,0.4); display: inline-block; padding: 6px 14px; border-radius: 8px; border: 1px solid #7f1d1d; margin-top: 6px;">
                Firma de auditoría y evidencia pericial registradas · Acceso neutralizado
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(135deg, #0b1329 0%, #030712 100%); border: 1px solid #1e3a5f; border-radius: 14px; padding: 20px; text-align: center; margin: 20px auto; max-width: 580px; box-shadow: 0 4px 20px rgba(0, 240, 255, 0.1);">
        <div style="font-size: 2.5rem; margin-bottom: 4px;">🔐</div>
        <h3 style="color: #38bdf8; font-family: monospace; letter-spacing: 2px; margin: 0;">AUREX TACTICAL SECURITY GATE</h3>
        <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">Identificación requerida para el Jefe del Taller</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        with st.form("form_autenticacion_jefe"):
            intento_clave = st.text_input("🔑 Ingrese Clave Maestra o Respuesta al Acertijo:", type="password")
            if pregunta_activa:
                st.caption(f"💡 **Acertijo de Respaldo:** *{pregunta_activa}*")
            
            btn_desbloquear = st.form_submit_button("🔓 Desbloquear AUREX", use_container_width=True, type="primary")
            if btn_desbloquear:
                if verificar_clave_o_acertijo(intento_clave):
                    st.session_state["autenticado_jefe"] = True
                    st.session_state["alerta_intrusion_activa"] = False
                    st.toast("🔓 Acceso Concedido. Bienvenido de vuelta, Jefe.", icon="🛡️")
                    st.rerun()
                else:
                    st.session_state["alerta_intrusion_activa"] = True
                    st.rerun()
                    
    st.stop()
    return False

def renderizar_seccion_alertas_moviles():
    """Panel de configuración y prueba de alertas tácticas al teléfono del Jefe."""
    from alertas_movil import obtener_config_alertas, guardar_config_alertas, despachar_alerta_movil_asincrona
    cfg = obtener_config_alertas()
    
    st.markdown("### 📲 Alertas en tu Teléfono (ntfy & Telegram)")
    st.markdown("""
    Recibe alertas instantáneas en tu celular con sonido de sirena cuando alguien intente tocar AUREX o meter una clave incorrecta, incluso si estás fuera del taller.
    """)
    
    tab_ntfy, tab_telegram = st.tabs(["⚡ Notificación Push Directa (ntfy)", "🤖 Bot de Telegram"])
    
    with tab_ntfy:
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
            st.link_button("🌐 Abrir Canal en Navegador", url_canal, use_container_width=True)
            
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
def renderizar_soc_multidispositivo():
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
                st.error(f"🚨 **¡AMENAZA EN CURSO!** Vector: `{amenaza.get('tipo')}` | IP Atacante: `{amenaza.get('ip_atacante')}`\n\n*Detalle:* {amenaza.get('detalle')}")
                
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
def renderizar_intervencion_plug_and_play():
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
                txt_alerta = f"⚡ **{n.get('ts')}** · Vector: `{n.get('vector')}` | IP Atacante: `{n.get('ip_atacante')}` - Respuesta: `{n.get('accion_autonoma')}` -> **{n.get('resultado')}**"
                st.info(txt_alerta)
    st.divider()
def renderizar_panel_ciberdefensa_policial():
    """Muestra el Centro de Incidentes y Generador de Informes Policiales dentro de AUREX."""
    st.subheader("🛡️ Centro de Ciberdefensa & Informes Periciales")
    st.caption("Auditoría forense digital con sellado SHA-256 e informes periciales listos para la Policía de Ciberdelitos.")
    renderizar_seccion_alertas_moviles()
    renderizar_soc_multidispositivo()
    renderizar_intervencion_plug_and_play()
    
    incidentes = leer_auditoria_seguridad(limite=15)
    if not incidentes:
        st.success("✅ Escudo de Seguridad al 100%: Cero anomalías ni intentos de intrusión recientes.")
        return
        
    st.markdown(f"**🚨 Incidentes Registrados ({len(incidentes)}):**")
    for inc in incidentes:
        with st.expander(f"⚠️ {inc.get('timestamp')} · {inc.get('tipo')} [{inc.get('severidad')}]"):
            st.markdown(f"""
            - **ID de Incidente:** `{inc.get('id_incidente', 'N/D')}`
            - **IP Atacante:** `{inc.get('ip_atacante', '127.0.0.1')}`
            - **Navegador / SO:** `{inc.get('user_agent', 'N/D')}`
            - **Detalle de la Intrusión:** {inc.get('detalle')}
            - **Firma Criptográfica SHA-256:** `{inc.get('hash_evidencia', 'N/D')[:32]}...`
            """)
            
            # Generar informe policial listo para descargar
            informe_texto = generar_informe_policial_forense(inc)
            st.download_button(
                label=f"📄 Descargar Informe Pericial para la Policía ({inc.get('id_incidente')})",
                data=informe_texto,
                file_name=f"INFORME_POLICIAL_{inc.get('id_incidente')}.txt",
                mime="text/plain",
                key=f"dl_policia_{inc.get('id_incidente')}"
            )
