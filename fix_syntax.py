ruta = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\escudo_seguridad.py"
with open(ruta, "r", encoding="utf-8") as f:
    contenido = f.read()

target = """            for n in neut[:3]:
                st.info(f"⚡ **{n.get('ts')}** · Vector: `{n.get('vector')}` | IP Atacante: `{n.get('ip_atacante')}`

*Respuesta Automática:* `{n.get('accion_autonoma')}` -> **{n.get('resultado')}**")"""

replacement = """            for n in neut[:3]:
                txt_alerta = f"⚡ **{n.get('ts')}** · Vector: `{n.get('vector')}` | IP Atacante: `{n.get('ip_atacante')}` - Respuesta: `{n.get('accion_autonoma')}` -> **{n.get('resultado')}**"
                st.info(txt_alerta)"""

if target in contenido:
    contenido = contenido.replace(target, replacement, 1)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print("FIX LINEAS 499-503 APLICADO")
else:
    print("TARGET NO ENCONTRADO, buscando alternativo...")
    # Intento con split
    lineas = contenido.splitlines()
    for i, l in enumerate(lineas):
        if "st.info(f\"⚡ **{n.get('ts')}**" in l:
            lineas[i] = "                txt_alerta = f\"⚡ **{n.get('ts')}** · Vector: `{n.get('vector')}` | IP Atacante: `{n.get('ip_atacante')}` - Respuesta: `{n.get('accion_autonoma')}` -> **{n.get('resultado')}**\""
            lineas[i+1] = "                st.info(txt_alerta)"
            lineas[i+2] = ""
            break
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
    print("FIX ALTERNATIVO APLICADO")
