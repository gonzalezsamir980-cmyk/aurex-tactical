"""
Fix: Añadir al prompt prohibición de frases de cierre tipo ChatGPT
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find REGLA 0 / VE AL GRANO block and add new rule about endings
OLD_RULE0 = 'VE AL GRANO INMEDIATAMENTE: La primera oracion de tu respuesta SIEMPRE debe ser la respuesta directa a la pregunta. NUNCA empieces con frases de relleno como "Me alegra verte", "Antes de empezar", "He estado revisando", "¿En que puedo ayudarte?", o cualquier introduccion vacia. Si el Jefe pregunta X, tu primera palabra ya contesta X.'

NEW_RULE0 = 'VE AL GRANO INMEDIATAMENTE: La primera oracion de tu respuesta SIEMPRE debe ser la respuesta directa a la pregunta. NUNCA empieces con frases de relleno como "Me alegra verte", "Antes de empezar", "He estado revisando", o cualquier introduccion vacia. Si el Jefe pregunta X, tu primera palabra ya contesta X.\n0b. SIN CIERRES DE CHATBOT: NUNCA termines con "Espero que esto te ayude", "¿Tienes alguna pregunta adicional?", "¿Hay algo mas en lo que pueda ayudarte?", "No dudes en preguntar" ni frases similares. Responde, da los datos, y para. El Jefe sabe que puede preguntar mas.'

if OLD_RULE0 in content:
    content = content.replace(OLD_RULE0, NEW_RULE0)
    print('[FIX CIERRE] Regla anti-cierre-ChatGPT AÑADIDA')
else:
    print('[ERROR] Regla 0 target not found')
    idx = content.find('VE AL GRANO')
    if idx >= 0:
        print('Found VE AL GRANO at:', idx)
        print(repr(content[idx:idx+300]))

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

import subprocess
result = subprocess.run(['python', '-m', 'py_compile', 'app.py'], capture_output=True, text=True)
if result.returncode == 0:
    print('[OK] syntax OK')
else:
    print('[ERROR]', result.stderr)

with open('app.py', 'r', encoding='utf-8') as f:
    v = f.read()
if 'SIN CIERRES DE CHATBOT' in v:
    print('[OK] Regla anti-cierre confirmada en app.py')
