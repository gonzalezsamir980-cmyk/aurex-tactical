import sys

ruta = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\artifacts_helper.py"
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

target = """    # 1. Detectar si hay sensores para mostrar sus fichas técnicas
    sensores_detectados = buscar_sensores_en_texto(texto)
    if sensores_detectados:
        st.markdown("##### 🔌 Fichas Visuales y Diagramas de Componentes")
        for s in sensores_detectados:
            renderizar_tarjeta_sensor(s)"""

replacement = """    # 1. Detectar si hay sensores para mostrar sus fichas técnicas
    texto_l = texto.lower()
    es_seguridad_o_chat = any(k in texto_l for k in ["contraorden", "ciberdefensa", "firewall", "ip atacante", "incidente", "auditoría", "auditoria", "acceso concedido", "desbloquear"])
    if not es_seguridad_o_chat:
        sensores_detectados = buscar_sensores_en_texto(texto, permitir_fallback=False)
        # Solo mostrar sensores reales del catálogo de mecatrónica (nunca falsos procedimentales en el chat)
        sensores_reales = [s for s in sensores_detectados if s.get("categoria") != "Hardware y Componentes Tcticos Solicitados" and s.get("categoria") != "Hardware y Componentes Tácticos Solicitados"]
        if sensores_reales:
            st.markdown("##### 🔌 Fichas Visuales y Diagramas de Componentes")
            for s in sensores_reales:
                renderizar_tarjeta_sensor(s)"""

if target not in contenido:
    print("ERROR: Target no encontrado")
    sys.exit(1)

contenido = contenido.replace(target, replacement, 1)

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print("ARTIFACTS_HELPER FILTRADO CON EXITO")
