with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

bad_str = '''                            respuesta = f"¡A sus órdenes, Jefe! Aquí tiene las **fichas tácticas, esquemas vectoriales de pines (pinouts) y especificaciones técnicas completas** del {nombres_txt}:

Puede consultar abajo los diagramas de cableado y directivas de taller para cada uno."'''

good_str = '''                            respuesta = f"""¡A sus órdenes, Jefe! Aquí tiene las **fichas tácticas, esquemas vectoriales de pines (pinouts) y especificaciones técnicas completas** del {nombres_txt}:

Puede consultar abajo los diagramas de cableado y directivas de taller para cada uno."""'''

if bad_str in content:
    content = content.replace(bad_str, good_str)
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed triple quotes in app.py!")
else:
    print("bad_str not found, trying regex...")
    import re
    content = re.sub(
        r'respuesta = f"¡A sus órdenes, Jefe!.*?"\n',
        r'respuesta = f"""¡A sus órdenes, Jefe! Aquí tiene las **fichas tácticas, esquemas vectoriales de pines (pinouts) y especificaciones técnicas completas** del {nombres_txt}:\\n\\nPuede consultar abajo los diagramas de cableado y directivas de taller para cada uno."""\n',
        content,
        flags=re.DOTALL
    )
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Regex replacement applied!")

import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] app.py syntax is 100% VALID!")
else:
    print("[ERROR] Syntax error:\n", res.stderr)
