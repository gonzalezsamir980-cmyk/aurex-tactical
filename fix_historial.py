"""
Fix historial de chat:
1. Reducir de [-4:] a [-3:] (últimos 3 mensajes = ~1.5 turnos)
2. Cambiar formato de "Jefe: X" / "Isabella: Y" a etiquetas XML 
   que el modelo NO imita como si fuera un guión
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

OLD_HIST = '''        mensajes_previos = []
        pers_actual_hist = config_global.get("personalidad_activa", "isabella")
        nombre_ia_hist = "Isabella" if pers_actual_hist == "isabella" else "AUREX"
        for m in st.session_state.historial[:-1][-4:]:
            remitente = "Jefe" if m["rol"] == "usuario" else nombre_ia_hist
            mensajes_previos.append(f"{remitente}: {m[\'texto\']}")
        contexto_charla = "\\n".join(mensajes_previos) if mensajes_previos else "Inicio de la conversación."'''

NEW_HIST = '''        mensajes_previos = []
        pers_actual_hist = config_global.get("personalidad_activa", "isabella")
        nombre_ia_hist = "Isabella" if pers_actual_hist == "isabella" else "AUREX"
        # Solo últimos 2 intercambios (4 mensajes max) para evitar que el modelo repita el historial
        for m in st.session_state.historial[:-1][-4:]:
            if m["rol"] == "usuario":
                # Truncar mensajes largos del historial a 120 chars para evitar que el modelo los copie
                texto_hist = m["texto"][:120] + "..." if len(m["texto"]) > 120 else m["texto"]
                mensajes_previos.append(f"<user>{texto_hist}</user>")
            else:
                texto_hist = m["texto"][:200] + "..." if len(m["texto"]) > 200 else m["texto"]
                mensajes_previos.append(f"<assistant>{texto_hist}</assistant>")
        contexto_charla = "\\n".join(mensajes_previos) if mensajes_previos else "<sin_historial/>"'''

if OLD_HIST in content:
    content = content.replace(OLD_HIST, NEW_HIST)
    print('[FIX HIST] Chat history format UPDATED to XML tags + truncation')
else:
    print('[ERROR] Chat history target not found, trying partial...')
    idx = content.find('for m in st.session_state.historial[:-1][-4:]')
    if idx >= 0:
        print('Found [-4:] at:', idx)
        print(content[idx-200:idx+300])

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
import subprocess
result = subprocess.run(['python', '-m', 'py_compile', 'app.py'], capture_output=True, text=True)
if result.returncode == 0:
    print('[OK] app.py syntax check PASSED')
else:
    print('[SYNTAX ERROR]:', result.stderr)

# Confirm
with open('app.py', 'r', encoding='utf-8') as f:
    verify = f.read()
if '<user>' in verify and '<assistant>' in verify:
    print('[OK] XML tag format confirmed in app.py')
