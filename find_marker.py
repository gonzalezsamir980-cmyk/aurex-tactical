# -*- coding: utf-8 -*-
path = r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find and replace the CUERPO_REGLAS_INGENIERIA start
marker = 'CUERPO_REGLAS_INGENIERIA = """REGLAS DE ORO:'
idx = text.find(marker)
if idx < 0:
    print("MARKER NOT FOUND")
else:
    print(f"Found at index {idx}")
    print(repr(text[idx:idx+300]))
