"""
Fix 3: Add 'despliega', 'desplegar', 'gemelo digital', 'twin' to es_peticion_diagrama
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

OLD_DIAG = '''es_peticion_diagrama = (not es_pregunta_o_consulta) and any(k in orden_l for k in [
                    "diagrama", "conexion", "conexi\u00f3n", "cableado", "wiring", "esquema",
                    "esquem\u00e1tico", "circuito", "pinout", "conectar", "haz un diagrama",
                    "haz el diagrama", "muestra el diagrama", "visualiza", "anatomy",
                    "despiece", "isometric", "isom\u00e9tric", "mecanismo", "m\u00e1quina", "maquina", "rig",
                    "holograma", "3d", "desarmar", "desensambl", "ensambl", "hiro", "stark",
                    "big hero", "pelicula", "pel\u00edcula", "ray'''

# Just add new keywords at the end of the list
OLD_PELICULAS = '"hiro", "stark",\n                    "big hero", "pelicula", "pel\u00edcula"'
NEW_PELICULAS = '"hiro", "stark",\n                    "big hero", "pelicula", "pel\u00edcula", "despliega", "desplegar", "gemelo digital", "twin", "vista 3d"'

if OLD_PELICULAS in content:
    content = content.replace(OLD_PELICULAS, NEW_PELICULAS)
    print('[FIX 3] es_peticion_diagrama UPDATED - added despliega/desplegar/gemelo digital')
else:
    print('[FIX 3] WARNING: target not found')
    idx = content.find('"hiro", "stark"')
    if idx >= 0:
        print('Context:', content[idx:idx+200])

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
import subprocess
result = subprocess.run(['python', '-m', 'py_compile', 'app.py'], capture_output=True, text=True)
if result.returncode == 0:
    print('[OK] app.py syntax OK')
else:
    print('[ERROR] syntax error:', result.stderr)
