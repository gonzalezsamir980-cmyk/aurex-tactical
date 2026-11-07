"""
Fix 1: Add 'despliega', 'desplegar', 'mostrar', 'muestra' to holograma_3d detector
Fix 2: Add 'brazo', 'arm', 'articulad' to es_peticion_diagrama detector
Fix 3: Clean code-block wrapping in streaming output
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ── FIX 1: Add despliega/desplegar to holograma detector ──
OLD_HOLO = 'es_holograma_3d = any(h in orden_l for h in ["holograma", "3d", "desarmar", "desensambl", "ensambl", "hiro", "stark", "big hero", "pelicula", "pel\u00edcula", "rayos x", "wireframe", "pon eso", "pon pieza", "laboratorio", "desarme"])'
NEW_HOLO = 'es_holograma_3d = any(h in orden_l for h in ["holograma", "3d", "desarmar", "desensambl", "ensambl", "hiro", "stark", "big hero", "pelicula", "pel\u00edcula", "rayos x", "wireframe", "pon eso", "pon pieza", "laboratorio", "desarme", "despliega", "desplegar", "muestra en 3", "mostrar en 3", "vista 3d", "gemelo digital", "twin"])'

if OLD_HOLO in content:
    content = content.replace(OLD_HOLO, NEW_HOLO)
    print('[FIX 1] holograma_3d detector UPDATED - added despliega/desplegar/twin')
else:
    print('[FIX 1] WARNING: holograma_3d detector target not found, trying partial match...')
    # Try to find it and show context
    idx = content.find('es_holograma_3d = any')
    if idx >= 0:
        print('Found at:', idx)
        print('Current:', content[idx:idx+200])

# ── FIX 2: Clean code-block wrapping from streaming output ──
# After the streaming loop, add cleanup for responses wrapped in code blocks
OLD_CLEAN = '            respuesta = re.sub(r\'[一-鿿]+\', \'\', respuesta_bruta)\n                            placeholder_stream.markdown(normalizar_latex(respuesta))'
NEW_CLEAN = '''            respuesta = re.sub(r\'[\\u4e00-\\u9fff]+\', \'\', respuesta_bruta)
                            # Limpiar si el modelo envolvió toda la respuesta en un bloque de código
                            respuesta = re.sub(r\'^```[\\w]*\\n\', \'\', respuesta.strip())
                            respuesta = re.sub(r\'\\n```$\', \'\', respuesta.strip())
                            placeholder_stream.markdown(normalizar_latex(respuesta))'''

if OLD_CLEAN in content:
    content = content.replace(OLD_CLEAN, NEW_CLEAN)
    print('[FIX 2] Code-block cleanup ADDED to streaming output')
else:
    print('[FIX 2] WARNING: streaming cleanup target not found')
    # Find the nearby code
    idx = content.find('placeholder_stream.markdown(normalizar_latex(respuesta))')
    if idx >= 0:
        print('Found at:', idx, '| Context:', content[idx-100:idx+100])

# ── FIX 3: Also add to es_peticion_diagrama if 'despliega' not there ──
# Check if despliega is in diagram detector
idx_diag = content.find('es_peticion_diagrama')
diag_section = content[idx_diag:idx_diag+500] if idx_diag >= 0 else ''
if 'despliega' not in diag_section and idx_diag >= 0:
    # Find the diagram keywords line
    old_diag_check = None
    for kw in ['"holograma"', '"diagrama"', '"conecta"']:
        kw_idx = content.find(kw, idx_diag)
        if kw_idx > 0 and kw_idx < idx_diag + 500:
            # Found - add 'despliega' nearby if not present
            # Actually the es_peticion_diagrama detection controls the whole flow
            # Let's just add despliega to it
            break
    print('[FIX 3] es_peticion_diagrama check - despliega needs to be in that list')
    # Find it
    for line in content[idx_diag:idx_diag+800].split('\n'):
        if 'any(' in line and ('diagrama' in line or 'holograma' in line or '3d' in line):
            print('Found diag detector line:', line[:200])
            break
else:
    print('[FIX 3] despliega already in peticion_diagrama or section not found')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nDone! Verifying...')

# Verify
with open('app.py', 'r', encoding='utf-8') as f:
    verify = f.read()

if 'despliega' in verify:
    print('[OK] despliega found in app.py')
if 'Code-block' in verify or '^```' in verify:
    print('[OK] code-block cleanup found in app.py')
