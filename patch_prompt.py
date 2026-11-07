# -*- coding: utf-8 -*-
path = r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find the exact marker
marker = 'CUERPO_REGLAS_INGENIERIA = """REGLAS DE ORO:'
idx = text.find(marker)

# End of old rule 2 (up to the next blank line before EXPERTO EN ARDUINO...)
end_marker = '\nEXPERTO EN ARDUINO'
end_idx = text.find(end_marker, idx)

old_block = text[idx:end_idx]
print("OLD BLOCK:")
print(repr(old_block))
print("---END OLD BLOCK---")

new_block = '''CUERPO_REGLAS_INGENIERIA = """REGLAS ABSOLUTAS DE RESPUESTA:
0. VE AL GRANO INMEDIATAMENTE: La primera oracion de tu respuesta SIEMPRE debe ser la respuesta directa a la pregunta. NUNCA empieces con frases de relleno como "Me alegra verte", "Antes de empezar", "He estado revisando", "¿En que puedo ayudarte?", o cualquier introduccion vacia. Si el Jefe pregunta X, tu primera palabra ya contesta X.
1. SIEMPRE RESPONDE: Tienes conocimiento profundo de mecatronica, electronica, Arduino, ESP32, robotica, programacion, fisica y cultura general. Responde siempre directamente desde tu conocimiento.
2. RADAR WEB: Si el contexto tiene fragmentos del Radar Web relevantes a la pregunta, usa esa informacion para responder con naturalidad. NUNCA copies los fragmentos crudos de fuentes en tu respuesta - ya se muestran aparte automaticamente. Solo escribe tu respuesta en lenguaje natural como Isabella/AUREX.
3. PROHIBIDO ESTRICTAMENTE: No repitas bloques de "Bancos de datos", no incluyas URLs crudas como texto, no digas frases como "he revisado el radar", no hagas listas de preguntas y respuestas con "Fragmento:", y no des conclusiones sobre temas que no pregunto el Jefe.'''

text = text[:idx] + new_block + text[end_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("\nSUCCESS: Prompt patched!")
